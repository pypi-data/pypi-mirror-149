import platform

# if platform.system() == 'Linux':
#     import matplotlib as mpl
#     mpl.use('Agg')

import re, sys, os
from compactem.utils import cv_utils, utils, data_load as comm_utils_data_load
from compactem.core import dp
import math
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from scipy.stats import beta
import numpy as np
from hyperopt import fmin, tpe, hp, STATUS_OK
from hyperopt.fmin import generate_trials_to_calculate
import logging, pickle
import json
import datetime
from poap.controller import SerialController, EvalRecord
from pySOT.optimization_problems import OptimizationProblem
from pySOT.experimental_design import SymmetricLatinHypercube
from pySOT.strategy import SRBFStrategy, DYCORSStrategy
from pySOT.surrogate import CubicKernel, LinearTail, RBFInterpolant
from lipo import GlobalOptimizer
from matplotlib import pyplot as plt
import seaborn as sns; sns.set()
from collections import OrderedDict
logger = logging.getLogger(__name__)

# import experiments
# from scikitDT import scikitDT


# Global constants go here
# LOGFILE = r'output/experiment_with_oracle.log'
NAME_CLASS_MAPPING = {'decision_tree': None,
                      'logistic_regression': None}
#
#
# def setup_logger():
#     """
#     set up the logger to log in a file as well as stdout
#     :return:
#     """
#     logFormatter = logging.Formatter("%(asctime)s [%(process)d] [%(threadName)s] [%(levelname)-5.5s] "
#                                      "[%(filename)s:%(lineno)d] [%(funcName)s]"
#                                      "  %(message)s")
#     rootLogger = logging.getLogger()
#     rootLogger.setLevel(logging.INFO)
#
#     fileHandler = logging.FileHandler(LOGFILE, mode='w')
#     fileHandler.setFormatter(logFormatter)
#     rootLogger.addHandler(fileHandler)
#
#     consoleHandler = logging.StreamHandler(sys.stdout)
#     consoleHandler.setFormatter(logFormatter)
#     rootLogger.addHandler(consoleHandler)
# setup_logger()


def process_splits(X, y, splits, randomize=False, return_indices=False):
    """
    Create datasets for the experiment. We need to provide 3 splits - train, val, test.
    When randomize=True explicitly take into account te pid because of this `issue <https://stackoverflow.com/questions/52295283/scikit-learn-train-test-split-inside-multiprocessing-pool-on-linux-armv7l-does/52315513#comment110054481_52315513>`_.

    :param X: 2D-array data to be split
    :param y: corresponding labels
    :param splits: splits as fractions; these must be specified as values in a dict with keys 'train', 'test', 'val'
    :param randomize: whether split must be randomized
    :param return_indices: whether indices in original dataset that end up in different splits must be returned
    :return: tuple with splits *X_train, y_train, idx_train,
        X_train_val, y_train_val, idx_train_val, X_val, y_val, idx_val, X_test, y_test, idx_test* is returned.
        If return_indices is False, the idx* entries are not returned.
    """
    notif_msg = "split %ages don't add up to 1!"
    assert sum(splits.values()) == 1, notif_msg

    fixed_random_state = 0
    indices = list(range(len(y)))
    X_train_val, X_test, y_train_val, y_test, idx_train_val, idx_test = \
        train_test_split(X, y, indices, test_size=splits['test'],
                         train_size=1 - splits['test'], stratify=y,
                         random_state=np.random.randint(0, 10000) + os.getpid()
                         if randomize else fixed_random_state)

    temp = 1.0 * splits['train'] / (splits['train'] + splits['val'])
    X_train, X_val, y_train, y_val, idx_train, idx_val = \
        train_test_split(X_train_val, y_train_val, idx_train_val, test_size=1 - temp,
                         train_size=temp, stratify=y_train_val,
                         random_state=np.random.randint(0, 10000) + os.getpid()
                         if randomize else fixed_random_state)

    if return_indices:
        ret_val = (X_train, y_train, idx_train,
                   X_train_val, y_train_val, idx_train_val,
                   X_val, y_val, idx_val,
                   X_test, y_test, idx_test)
    else:
        ret_val = (X_train, y_train,
                   X_train_val, y_train_val,
                   X_val, y_val,
                   X_test, y_test)
    return ret_val


def uncertainty(predicted_probs):
    """
    Compute uncertainty based on prediction confidences.

    :param predicted_probs: Must to be a list of one of these:

        * dicts, with each dict representing per label probability for a point. Key=class, value=probability.
        * a list of probability values per point (*NOTE: this may be deprecated*)

    :return: 1D array of uncertainty values where size of array is same as number of points
    """
    uncs= []
    # use top_two
    for p in predicted_probs:
        conf_values = list(p.values()) if type(p) == dict else p
        top_1, top_2 = sorted(conf_values, reverse=True)[:2]
        uncs.append(1 - (top_1 - top_2))
    return np.array(uncs)


def ku_pdf(X, a, b):
    """
    **Experimental.**

    Use the Kumaraswamy distribution for fast pdf computation. The Ku distribution has the advantage of having a simple
    CDF which makes sampling easy. See this `article <https://www.johndcook.com/blog/2009/11/24/kumaraswamy-distribution/>`_.
    Eventually I didn't use this since bulk sampling from Betas didn't seem particularly slow compared to this.

    :param X: 2D-array of input points whose density values we want to compute
    :param a: shape parameter of the Ku distribution
    :param b:  shape parameter of the Ku distribution

    :return: the pdf values for X
    """
    # to ensure we don't end up sampling 0 ir infty which happens near the extremes
    LOWER_BOUND, UPPER_BOUND = 0.05, 0.95

    X[X < LOWER_BOUND] = LOWER_BOUND
    X[X > UPPER_BOUND] = UPPER_BOUND

    pdf = a*b*np.power(X, a-1)*np.power(1-np.power(X, a), b-1)
    return pdf


def get_sample_and_weights_using_oracle(sample_size, X, y, uncertainties, dp_alpha, prior_for_a_beta_A,
                      prior_for_a_beta_B, prior_for_b_beta_A, prior_for_b_beta_B, scale_a=10, scale_b=10,
                       pct_from_original=0.0, num_trials=1000):
    """
        Given the training data, generate samples (w/o replacment) based on the oracle. The number of points returned
        in the sample may be less than what is requested since the Beta might be concentrated in regions where we
        have no points; quite possible in the early parts of the search for the optimal distribution.

        :param sample_size: number of points we want to sample
        :param X: 2D-array of data to sample from
        :param y: labels corresponding to X
        :param dp_alpha: concentration parameter of Dirichlet Process
        :param prior_for_a_beta_A: Beta shape parameter A for the prior to use to sample a
        :param prior_for_a_beta_B: Beta shape parameter B for the prior to use to sample a
        :param prior_for_b_beta_A: Beta shape parameter A for the prior to use to sample b
        :param prior_for_b_beta_B: Beta shape parameter B for the prior to use to sample b
        :param scale_a: scaling parameter for Beta, see ``scipy.stats.beta``
        :param scale_b: scaling parameter for Beta, see ``scipy.stats.beta``
        :param pct_from_original: percentage of points to be sampled from the original distribution. This is a stratified
            sample
        :param num_trials: # trials over which instance weights are to be averaged
        :return: sampled X, y, and vector of corresponding instance weights.
        Number of points in the sample might be less than sample_size
        """
    sample_size_from_oracle, sample_size_from_orig = sample_size, 0
    pct_from_original = min([1.0, pct_from_original])
    pct_from_oracle = 1.0 - pct_from_original
    if 0 < pct_from_original:
        sample_size_from_orig = int(pct_from_original * sample_size)
        sample_size_from_oracle = sample_size - sample_size_from_orig
    float_max = np.finfo(np.float64).max
    sample_X, sample_y, trial_weights = [], [], np.zeros((num_trials, len(uncertainties)))
    if pct_from_oracle > 0:
        logging.info(f"Starting to sample from oracle, over {num_trials} trials.")
        start_time = datetime.datetime.now()
        for tr_idx in range(num_trials):
            # determine the IBMM
            clusters = dp.generic_blackwell_macqueen_sampler(dp_alpha, sample_size_from_oracle)
            betas_for_sampling = dp.sample_beta(prior_for_a_beta_A, prior_for_a_beta_B, prior_for_b_beta_A,
                                                prior_for_b_beta_B, len(clusters), scale_a, scale_b)
            for cluster_size, indv_beta in zip(clusters, betas_for_sampling):
                if cluster_size == 0:
                    continue
                frozen_pdf = beta(indv_beta[0], indv_beta[1])
                sample_probs = frozen_pdf.pdf(uncertainties)
                # sample_probs = np.clip(sample_probs, a_min=np.min(sample_probs), a_max=float_max)
                trial_weights[tr_idx, :] = sample_probs
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        logging.info(
            f"Finished obtaining weights from oracle, over {num_trials} trials, {1.0 * duration / num_trials} sec per trial.")

        # we need to average weights across trials - but need to be mindful about the fact that we might see np.inf
        # values here's what we do: replace infs with the max float value *after* taking the mean. Same with the total
        # - note: the replacement in the pdf weights should be done after computing the total, otherwise np.sum
        # (used to compute total) might again bump up values to np.inf
        instance_weights = np.mean(trial_weights, axis=0)
        total_weight = np.sum(instance_weights)
        instance_weights = np.clip(instance_weights, a_min=np.min(instance_weights), a_max=float_max)
        if np.isinf(total_weight):
            total_weight = float_max
        normalized_oracle_weights = instance_weights/total_weight
        if np.any(np.isinf(normalized_oracle_weights)):
            logging.debug(f"Found inf in normalized instance weight array.")
        if np.any(np.isnan(normalized_oracle_weights)):
            logging.debug(f"Found nan in normalized instance weight array.")
    else:
        normalized_oracle_weights =  np.zeros(len(uncertainties))

    # get weights from original, this is simply 1/N
    normalized_orig_weights = np.ones(len(uncertainties))/len(uncertainties)

    # get the final weights
    normalized_weights = pct_from_oracle * normalized_oracle_weights + pct_from_original * normalized_orig_weights
    if np.any(np.isinf(normalized_weights)):
        logging.debug(f"Found inf in normalized weight array.")
    if np.any(np.isnan(normalized_weights)):
        logging.debug(f"Found nan in normalized weight array.")

    # get the desired sample size after ignoring zero weights (zero weights are impossible if pct_from_original > 0 )
    top_idxs = np.argsort(normalized_weights)[-sample_size:]
    top_idxs = [idx for idx in top_idxs if normalized_weights[idx] > 0]
    gap = sample_size - len(top_idxs)
    if gap > 0:
        logging.debug("Requested total size: %d, sampled size=%d, skipped=%d" % (sample_size,
                                                                       len(top_idxs), gap))
    sample_X, sample_y, sample_weights = X[top_idxs, :], y[top_idxs], normalized_weights[top_idxs]
    return sample_X, sample_y, sample_weights


def sample_using_oracle(sample_size, X, y, uncertainties, dp_alpha, prior_for_a_beta_A,
                      prior_for_a_beta_B, prior_for_b_beta_A, prior_for_b_beta_B, scale_a=10, scale_b=10,
                       pct_from_original=0.0, use_weights=False, num_weight_trials=10):
    """
    Given the training data, generate samples (with replacement) based on the oracle. The number of points returned in
    the sample may be less than what is requested since the Beta might be concentrated in regions where we have no
    points; quite possible in the early parts of the search for the optimal distribution.

    :param sample_size: number of points we want to sample
    :param X: 2D-array of data to sample from
    :param y: labels corresponding to X
    :param dp_alpha: concentration parameter of Dirichlet Process
    :param prior_for_a_beta_A: Beta shape parameter A for the prior to use to sample a
    :param prior_for_a_beta_B: Beta shape parameter B for the prior to use to sample a
    :param prior_for_b_beta_A: Beta shape parameter A for the prior to use to sample b
    :param prior_for_b_beta_B: Beta shape parameter B for the prior to use to sample b
    :param scale_a: scaling parameter for Beta, see ``scipy.stats.beta``
    :param scale_b: scaling parameter for Beta, see ``scipy.stats.beta``
    :param pct_from_original: percentage of points to be sampled from the original distribution. This is a stratified
        sample
    :return: sampled X and y. Number of points in the sample might be less than sample_size
    """
    if use_weights:
        sample_X, sample_y, sample_weights = get_sample_and_weights_using_oracle(sample_size, X, y, uncertainties,
                                                                                 dp_alpha, prior_for_a_beta_A,
                                                                                 prior_for_a_beta_B, prior_for_b_beta_A,
                                                                                 prior_for_b_beta_B, scale_a,
                                                                                 scale_b,
                                                                                 pct_from_original,
                                                                                 num_trials=num_weight_trials)
        return sample_X, sample_y, sample_weights
    sample_size_from_oracle, sample_size_from_orig = sample_size, 0
    pct_from_original = min([1.0, pct_from_original])
    if 0 < pct_from_original:
        sample_size_from_orig = int(pct_from_original * sample_size)
        sample_size_from_oracle = sample_size - sample_size_from_orig

    sample_X, sample_y = [], []
    if sample_size_from_oracle > 0:
        logging.info("Starting to sample from oracle")
        
        # determine the IBMM
        clusters = dp.generic_blackwell_macqueen_sampler(dp_alpha, sample_size_from_oracle)
        betas_for_sampling = dp.sample_beta(prior_for_a_beta_A, prior_for_a_beta_B, prior_for_b_beta_A,
                                            prior_for_b_beta_B, len(clusters), scale_a, scale_b)
        samples_skipped = 0  # because of total sampling probs = 0
        for cluster_size, indv_beta in zip(clusters, betas_for_sampling):
            if cluster_size == 0:
                continue
            frozen_pdf = beta(indv_beta[0], indv_beta[1])
            sample_probs = frozen_pdf.pdf(uncertainties)
            if np.any(np.isnan(sample_probs)) or np.any(np.isinf(sample_probs)):
                logging.error("Problems with sample probability for beta(%s, %s) : %s" % (str(indv_beta[0]),
                                                                                          str(indv_beta[1]),
                                                                                          str(sample_probs)))

            total_prob = sum(sample_probs)

            # The total prob might be zero if this beta component is located in part of the unc axis where we have
            # no points. Its quite likely that this distribution is also very peaked, so no other point gets a non-zero
            # probability. This is OK: part of the optimizer's search for discovering good distributions.
            if total_prob == 0:
                # logging.error("Total prob=0, can't sample for this cluster!")
                samples_skipped += cluster_size
                continue
            #sample_probs = ku_pdf(uncertainties, indv_beta[0], indv_beta[1])
            sample_probs = sample_probs / total_prob
            selected_idxs = np.random.choice(len(sample_probs), size=cluster_size, replace=True, p=sample_probs)
            sample_X.append(X[selected_idxs, :])
            sample_y += [y[idx] for idx in selected_idxs]

        # we need to check for the condition that as a whole the IBMM was located in part of the unc region where we
        # had no points. Downstream checks should ensure this doesnt cause problems.
        if len(sample_X) > 0:
            sample_X = np.vstack(sample_X)
        logging.info("Done sampling from oracle.")

        if sample_size_from_oracle > len(sample_X):
            # This is possible, because some mixture components might prefer uncertainties for which we have no points,
            # so nothing will be sampled for those components, leading to a deficit. Since this is expected and not a
            # bug, we just log and move on.
            logging.debug("Requested size: %d, sampled size=%d, skipped=%d" % (sample_size_from_oracle,
                                                                                 len(sample_X), samples_skipped))

    if sample_size_from_orig > 0:
        if sample_size_from_oracle == 0 or len(sample_X) == 0:
            sample_X = np.empty((0, np.shape(X)[1]), dtype=X.dtype)
        sample_orig_X, sample_orig_y = cv_utils.stratified_conservative_sample(X, y, sample_size_from_orig)
        sample_X = np.vstack((sample_X, sample_orig_X))
        sample_y = list(sample_y) + list(sample_orig_y)

    return sample_X, sample_y


def adjust_sample_from_dist(sample_size, pct_from_original, min_sample_size_per_dist):
    """
    If we are sampling less points than is statistically significant either from the original sample or the
    DP, round *pct_from_original* to completely reflect only one of the distributions. This is not a continuous function
    (see section A.1 `here <https://ndownloader.figstatic.com/files/21816114>`_) which
    is a no-no in many cases, but since we are performing *Bayesian Optimization* here, this going to be
    approximated by a smooth function anyway.

    :param sample_size: sample requested of the Dirichlet Process (DP)
    :param pct_from_original: percentage of points in the sample to be sampled from the original distribution
    :param min_sample_size_per_dist: min sample size that needs to be sampled from either the DP or the original
        distribution. Either we sample at least these many points from either distribution, or set one to 0 and sample
        all from the other.
    :return: adjusted percentage of points to be sampled from the original distribution
    """

    if math.floor(sample_size * pct_from_original) < min_sample_size_per_dist or \
            math.floor(sample_size * (1.0 - pct_from_original)) < min_sample_size_per_dist:
        return round(pct_from_original)
    return pct_from_original


def create_search_space(max_components, min_sample_size, min_sample_size_as_pct, max_sample_size_as_pct,
                        alpha_multiplier=2.0, extended_space=True, optimizer_type='hyperopt'):
    """
    Creates a list of search spaces using hyperopt primitives.

    The max alpha is computed with the approximation num_components = 5*alpha +2 as per
    this `paper <http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.330.363&rep=rep1&type=pdf>`_.

    :param max_components: an estimate of the maximum number of components the mixture model over uncertainties
    :param min_sample_size: the smallest sample size; information-wise this is the same as min_sample_size_as_pct but
        expressed as an absolute number.
    :param min_sample_size_as_pct: the smallest size our sample can be, expressed as a fraction of the training data
        sample size
    :param alpha_multiplier: see notes within function
    :param extended_space: if True the shape prior param space is considerable extended
    :param optimizer_type: based on the optimizer backend a different representation of the search space is returned.
    :return: list of hyperopt search space primitives
    """
    # H_n = dp.harmonic_num(min_sample_size)  # H_n is the nth harmonic number

    # While alpha * H_n is the max number of clusters that a DP may produce, we also note that the rate of producing
    # new clusters in a DP decreases as the number of clusters/points seen increases. Hence its not sufficient to, say,
    # set alpha such that alpha*H_n is 10 if we expect to see 10 clusters; since 10 might not be easily reachable.
    # We use an arbitrary multiplier to make higher cluster numbers accessible.

    # max_DP_alpha = alpha_multiplier * max_components / H_n
    max_DP_alpha = (max_components - 2.0) /5.0
    space = [hp.uniform('dp_alpha', 0.1, max_DP_alpha)]
    only_unif = OrderedDict({'dp_alpha': (0.1, max_DP_alpha)})  # only uniform search spaces
    log_transforms = []  # these uniform variables need to be transformed to log-uniform

    # the optimizer decides the size of the sample to be used to train the small model; this is expressed as a fraction
    # of the size of the training data
    space.append(hp.uniform('sample_size_as_pct', min_sample_size_as_pct, max_sample_size_as_pct))
    only_unif['sample_size_as_pct'] = (min_sample_size_as_pct, max_sample_size_as_pct)

    # for a given sample size, the optimizer is free to pick some proportion from the original dataset too
    space.append(hp.uniform('pct_from_original', 0.0, 1.0))
    only_unif['pct_from_original'] = (0.0, 1.0)

    # the priors for components
    # NOTE: the log transformation needs to be done in the optimizer in the case of uniform search space!
    if extended_space:
        space.append(hp.loguniform('prior_for_a_beta_A', -10, 10))
        only_unif['prior_for_a_beta_A'] = (-10, 10)
        log_transforms.append('prior_for_a_beta_A')

        space.append(hp.loguniform('prior_for_a_beta_B', -10, 10))
        only_unif['prior_for_a_beta_B'] = (-10, 10)
        log_transforms.append('prior_for_a_beta_B')

        space.append(hp.loguniform('prior_for_b_beta_A', -10, 10))
        only_unif['prior_for_b_beta_A'] = (-10, 10)
        log_transforms.append('prior_for_b_beta_A')

        space.append(hp.loguniform('prior_for_b_beta_B', -10, 10))
        only_unif['prior_for_b_beta_B'] = (-10, 10)
        log_transforms.append('prior_for_b_beta_B')
    else:
        space.append(hp.uniform('prior_for_a_beta_A', 0.1, 100))
        only_unif['prior_for_a_beta_A'] = (0.1, 100)

        space.append(hp.uniform('prior_for_a_beta_B', 0.1, 100))
        only_unif['prior_for_a_beta_B'] = (0.1, 100)

        space.append(hp.uniform('prior_for_b_beta_A', 0.1, 100))
        only_unif['prior_for_b_beta_A'] = (0.1, 100)

        space.append(hp.uniform('prior_for_b_beta_B', 0.1, 100))
        only_unif['prior_for_b_beta_B'] = (0.1, 100)

    if optimizer_type == 'hyperopt':
        return space
    elif optimizer_type in {'pysot', 'lipo'}:
        return only_unif, log_transforms
    else:
        return None


def determine_split_type(splits):
    """
    Helper to ``run_experiment()``. Since a variety of ``splits`` arguments may be accepted for usability, this is kind
    of the "type-checker". Checks if data or split %ages were specified.

    :param splits:
    :return: returns split type as 'data' or 'proportions' to signify if split data were directly passed in or split
        percentages were specified. Returns None in other cases.
    """
    if len(splits) != 3:
        return None
    s = set(map(type, list(splits.values())))

    if len(s) != 1:
        logging.error("Split values must be of the same type.")
        return None
    common_type = s.pop()

    if common_type == float:
        if sum(splits.values() != 1):
            logging.error("Split proportions don't add up to 1.")
            return None
        return "proportions"

    if common_type in [tuple, list]:
        return 'data'
    return None


def run_experiment(dataset, model_obj, oracle,
                   evals=100, min_sample_size=100, min_sample_size_per_dist=100, max_sample_size=None,
                   max_components=30,
                   sampling_trials=1, use_weights=False, num_weight_trials=10,
                   splits=None,
                   dataset_name=None,
                   create_persistence_obj=False, use_persistence_obj=None,
                   working_dir=r'./',
                   uncertainty_info=None,
                   additional_init_vals=None,
                   scale=10000,
                   compute_all_baselines=False,
                   save_optimal_sample=False,
                   use_extended_search_space=True,
                   optimizer='hyperopt', optimizer_params=None):
    """
    Runs the optimization for given dataset, splits, oracle etc. This is the core algorithm.

    :param dataset: can be a string name for the dataset OR and tuple (X,y). A string name is used by
        ``utils.data_load`` to load up a registered dataset.
    :param model_obj: subclass of ``ModelBuilderBase``
    :param oracle: this can be a bunch of things:

        *   None: the oracle model obj would be looked up in use_persistence_obj. This parameter input leads to an error
            if use_persistence_obj=None
        *   oracle model obj: if an oracle model object is directly passed in it must allow calls to ``predict_proba()``
            and ``predict()``
        *   a function that can be invoked to train the oracle; this must return an oracle model object, which supports
            calls to ``predict_proba()``, ``predict()``

    :param evals: the optimization budget, i.e., number of iteration for which the optimizer is run
    :param min_sample_size: the size of the sample to be generated at a particular iteration shouldn't fall below this;
        this is ensured by defining the search space accordingly.
    :param min_sample_size_per_dist: the min number of samples that can be drawn from either the original dist or the
        DP to be statistically significant
    :param max_sample_size: maximum number of points that can be sampled, if this is None, the upper limit is the size
        of the training split
    :param max_components: max number of components of the mixture model (over uncertainties)
    :param sampling_trials: for a particular setting of the DP how many times to sample, fit and evaluate?
        This is for rigor - averaging over samples provides a stable score for the optimizer to use.
    :param use_weights: you can avoid sampling and fitting (which can be expensive) by using instance weights instead,
        IF your classifier supports learning using instance weights. If this is set to True, sampling_trials MUST be
        set to 1
    :param num_weight_trials: if use_weights is True, this is the number of times instance weights would be averaged
    :param splits: what fraction of the dataset to be used for various tests. This can take on a few possible types:

        *   None: the train-val-test split is the same as DEFAULT_SPLITS (see function body)
        *   dict with float values, must look like this and have values for all keys explicitly specified:
            ``{'train': 0.6, 'val': 0.2, 'test': 0.2}``
        *   dict that passes in the train, val, test datasets directly, should be of the form:
            ``{'train': (X_train, y_train), 'val': (X_val, y_val), 'test': (X_test, y_test)}``. This is helpful where
            precise splits need to be enforced.

    :param dataset_name: name of the dataset, this is used in plotting. Optional. If 'dataset' is a string, that name
        would be used
    :param create_persistence_obj: *marked for deprecation*
    :param use_persistence_obj:  *marked for deprecation*
    :param working_dir: directory to store all results in, this is where files would be created
    :param uncertainty_info: use this option if you don't want to pass in an oracle, and want to use some previously
        determined info. If this parameter is not None, it must be a dict with the following elements:

            *   'uncertainties': list of uncertainty values, len of list must be the same as number of instances
            *   'oracle_score': some representative score of the oracle on the dataset. NOTE that there is potential for
                abstraction leakage here; if the splits parameter only contains split %ages, how would you know the
                oracle score you provide doesnt use data that overlaps with the training subset to be determined?
                Best to ensure that the score comes from an entirely different data sample, or use this option only
                when you are actually passing in data subsets in splits.
            *   'str_info': other info that will be used to print in summaries etc. This is optional.

        If this parameter is not None, the ``oracle`` and ``use_persistence_obj`` parameters are ignored. CAREFUL!

    :param additional_init_vals: these are initial values for the search space. Its called "additional" since there is
        one initial value *always* added: the settings of the baseline score. If provided this should be a list of dicts
        each with the keys: *dp_alpha, sample_size_as_pct, pct_from_original, prior_for_a_beta_A, prior_for_a_beta_B,
        prior_for_b_beta_A, prior_for_b_beta_B*.
    :param scale: input to beta samplers over the shape parameters
    :param compute_all_baselines: this flag decides if all baseline combinations, e.g., train on train and predict on
        train, train on train predict on val etc need to be computed. Those numbers are good for research, but are time
        taking and are not useful for most of the practical use-cases.
    :param save_optimal_sample: whether the samples at the best validation score to be saved into a file. Note that
        since there are more than one sampling trials, all of them would be saved.
    :param use_extended_search_space: solution is searched over a larger space
    :param optimizer: which optimizer backend to use? This can be "hyperopt", "pysot" or "lipo".
    :param optimizer_params: if the optimizer accepts params, they need to be passed in as a dict. There is no standard
        format for this, and would be parsed in an optimizer specific way. Current supported:
        * for optimizer=pysot, this parameter can be {"strategy": "srbf"} or {"strategy": "dycors"}

    :return: *test improvement at the best validation accuracy, best parameters, new_persistence_obj*.

    .. note::
            The choice of return variables are mostly legacy, and the result files produced should be read instead.

    """
    ERRORED_SAVE_PATH = "Error: couldn't save file."
    DEFAULT_SPLITS = {'train': 0.6, 'val': 0.2, 'test': 0.2}
    SUPPORTED_OPTIMIZERS = {'hyperopt', 'pysot', 'lipo'}
    OPTVAR_DIMS = 7
    if optimizer not in SUPPORTED_OPTIMIZERS:
        logging.error(f"Unsupported optimizer: {optimizer}, we only support {','.join(SUPPORTED_OPTIMIZERS)}")
        return
    if use_weights and sampling_trials > 1:
        logging.warning(f"Since use_weights={use_weights}, sampling_trials is set to 1.")
        sampling_trials = 1
    if splits is None:
        splits = DEFAULT_SPLITS

    split_type = determine_split_type(splits)
    if uncertainty_info:
        if use_persistence_obj or oracle:
            logging.error("use_persistence_obj/oracle cannot be used when uncertainty_info is provided. Aborting!")
            return
        if split_type != 'data':
            logging.error("Can't ask to split within the function if  uncertainty_info is provided - directly pass in "
                          "split data. Aborting!")
            return

    if split_type is None:
        logging.error("Invalid split type, aborting.")
        return

    new_persistence_obj = {}
    start_time = datetime.datetime.now()
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)
    optimal_samples_file = working_dir + os.sep + "optimal_samples.pckl"
    uncertainty_file = working_dir + os.sep + "train_uncertainties.txt"
    sample_plot_file = working_dir + os.sep + "sample.png"
    optimizer_progress_plot_file = working_dir + os.sep + "opt_progress.png"  # plot of optimizer progress
    scores_plot_file = working_dir + os.sep + "scores_progress.png"  # plot train/val/test scores
    trials_file = working_dir + os.sep + "trials.txt"  # info about optimizer trials
    results_file = working_dir + os.sep + "results.txt"  # other info, can be used for plotting
    models_dir = working_dir + os.sep + "models"  # model learned on optimal data
    # baseline_models_file = models_dir + os.sep + "baseline_models.pckl"
    baseline_models_dir = models_dir + os.sep + "baseline_models"

    for required_dir in [models_dir, baseline_models_dir]:
        if not os.path.exists(required_dir):
            os.mkdir(required_dir)

    # maintain a json of everything that we want eventually logged
    if uncertainty_info:
        oracle = None
        if "str_info" in uncertainty_info:
            oracle_str = uncertainty_info['str_info']
        else:
            oracle_str = "None: uncertainty info provided"
    else:
        if oracle:
            oracle_str = str(oracle)
        else:
            oracle_str = str(use_persistence_obj['oracle'])

    result_json = {"general_info": {"complexity_param": str(model_obj.complexity_param),
                                    "complexity_param_pickled_hex": pickle.dumps(model_obj.complexity_param).hex(),
                                    "optimizer_iterations": evals, "optimizer": optimizer,
                                    "optimizer_params": optimizer_params,
                                    "sampling_style": f"weight averaging ({num_weight_trials})" if use_weights else
                                                        f"sample and fit ({sampling_trials})",
                                    "model": model_obj.__class__.__name__,
                                    'oracle': oracle_str}}

    X, y = None, None
    if dataset is None:
        if split_type != "data":
            logging.error("No data provided. Aborting!")
            return
        else:
            X = np.vstack((splits['train'][0], splits['val'][0], splits['test'][0]))
            y = list(splits['train'][1]) + list(splits['val'][1]) + list(splits['test'][1])

    if type(dataset).__name__ == "str":
        if dataset_name is None:
            dataset_name = dataset
        X, y = comm_utils_data_load.load_data(dataset)
    elif utils.is_iterable(dataset) and len(dataset) == 2:
        X, y = dataset
        if dataset_name is None:
            dataset_name = "NA"

    logging.info("Loaded dataset. Shape of data: %s" % (str(np.shape(X)),))
    result_json["dataset_properties"] = {"name": dataset_name,
                                         "instances": np.shape(X)[0],
                                         "features": np.shape(X)[1],
                                         "classes": len(set(y)),
                                         "label_entropy": comm_utils_data_load.entropy(y)}

    # split the data
    if split_type == "proportions":
        X_train, y_train, X_train_val, y_train_val, X_val, y_val, X_test, y_test = \
        process_splits(X, y, splits)
    elif split_type == "data":
        X_train, y_train = splits['train']
        X_val, y_val = splits['val']
        X_test, y_test = splits['test']
        X_train_val, y_train_val = np.vstack((X_train, X_val)), list(y_train) + list(y_val)
    else:
        logging.error("Invalid split type: %s. Aborting." % (split_type,))
        return

    model_obj.load_data_splits(X_train, y_train, X_train_val, y_train_val, X_val, y_val, X_test, y_test)

    # log these the %ages
    result_json['splits'] = {'split_train': (np.shape(X_train)[0], 1.0 * np.shape(X_train)[0] / np.shape(X)[0]),
                             'split_train_val': (np.shape(X_train_val)[0], 1.0 * np.shape(X_train_val)[0] / np.shape(X)[0]),
                             'split_val': (np.shape(X_val)[0], 1.0 * np.shape(X_val)[0] / np.shape(X)[0]),
                             'split_test': (np.shape(X_test)[0], 1.0 * np.shape(X_test)[0] / np.shape(X)[0])
                             }

    # build the baseline models
    logging.info("Doing all the baseline fits - this might take a while")
    baseline_train_score_based_on_train, baseline_best_train_model_based_on_train, \
        baseline_val_score_based_on_train, baseline_best_val_model_based_on_train, \
        baseline_test_score_based_on_train, baseline_best_test_model_based_on_train, \
        baseline_test_score_based_on_train_val, baseline_best_test_model_based_on_train_val = \
        model_obj.fit_baseline_model(all_baselines=compute_all_baselines, num_train_points=max_sample_size)

    logging.info("Writing baseline models.")
    baseline_models = {'train_model_based_on_train': baseline_best_train_model_based_on_train,
                       'val_model_based_on_train': baseline_best_val_model_based_on_train,
                       'test_model_based_on_train': baseline_best_test_model_based_on_train,
                       'test_model_based_on_train_val': baseline_best_test_model_based_on_train_val
                       }
    baseline_models_paths = {'train_model_based_on_train': None,
                       'val_model_based_on_train': None,
                       'test_model_based_on_train': None,
                       'test_model_based_on_train_val': None
                       }

    for baseline_model_name, baseline_model in list(baseline_models.items()):
        if baseline_model:
            suggested_path = baseline_models_dir + os.sep + baseline_model_name
            try:
                saved_path = model_obj.save_model(baseline_model, suggested_path)
            except:
                logging.error(f"Couldn't write baseline model {suggested_path}!")
                saved_path = ERRORED_SAVE_PATH
            baseline_models_paths[baseline_model_name] = saved_path if saved_path else suggested_path

    complexity_best_test_model_based_on_train_val = \
        model_obj.get_complexity(baseline_best_test_model_based_on_train_val)
    result_json['baseline_fits'] = {"test_score_based_on_train":
                                    baseline_test_score_based_on_train,
                                    "complexity_best_test_model_based_on_train":
                                        None if baseline_best_test_model_based_on_train is None else
                                        model_obj.get_complexity(baseline_best_test_model_based_on_train),
                                    "test_score_based_on_train_val":
                                        baseline_test_score_based_on_train_val,
                                    "complexity_best_test_model_based_on_train_val":
                                        str(complexity_best_test_model_based_on_train_val),
                                    "complexity_best_test_model_based_on_train_val_pickled_hex":
                                        pickle.dumps(complexity_best_test_model_based_on_train_val).hex(),
                                    "val_score_based_on_train":
                                        baseline_val_score_based_on_train,
                                    "complexity_best_val_model_based_on_train":
                                        None if baseline_best_val_model_based_on_train is None else
                                        model_obj.get_complexity(baseline_best_val_model_based_on_train),
                                    "train_score_based_on_train":
                                        baseline_train_score_based_on_train,
                                    "complexity_best_train_model_based_on_train":
                                        None if baseline_best_train_model_based_on_train is None else
                                        model_obj.get_complexity(baseline_best_train_model_based_on_train),
                                    # file paths
                                    'path_train_model_based_on_train':
                                        baseline_models_paths['train_model_based_on_train'],
                                    'path_val_model_based_on_train':
                                        baseline_models_paths['val_model_based_on_train'],
                                    'path_test_model_based_on_train':
                                        baseline_models_paths['test_model_based_on_train'],
                                    'path_test_model_based_on_train_val':
                                        baseline_models_paths['test_model_based_on_train_val']
                                    }

    logging.info("Done with baseline fits.")
    result_json["runtimes"] = {}
    result_json["runtimes"]["time_till_baseline_fits"] = (datetime.datetime.now() - start_time).total_seconds()

    if uncertainty_info:
        score = uncertainty_info['oracle_score']
        uncertainties = uncertainty_info['uncertainties']
        oracle_model = None
    else:
        if oracle is None and use_persistence_obj:
            oracle_model = use_persistence_obj['oracle']
        elif re.search(r'class|instance', str(type(oracle))): # check for old and new style classes
            oracle_model = oracle
        elif callable(oracle):
            oracle_model = oracle(X_train, y_train)
        else:
            logging.error("Can't obtain oracle. Aborting")
            return
        oracle_y_pred = oracle_model.predict(X_test)
        score = f1_score(y_test, oracle_y_pred, average='macro')
        probs = oracle_model.predict_proba(X_train)
        uncertainties = uncertainty(probs)

    #logging.info("writing out uncertainties ...")
    with open(uncertainty_file, 'w') as f_unc:
        f_unc.write("\n".join(map(str, uncertainties)))

    logging.info("oracle score on test: %0.02f" % (score,))
    result_json ["general_info"]["oracle_score_on_test"] = score
    result_json["runtimes"]["time_till_generating_oracle"] = (datetime.datetime.now() - start_time).total_seconds()

    if create_persistence_obj:
        new_persistence_obj['oracle'] = oracle_model

    # These are instantiated as lists to get around an annoying Python 2.x issue: can't reassign a variable in an outer
    # scope that's not global. We use a list and only use the entry at index 0. Mutation is allowed.
    best_mean_val_score_so_far = [0]
    best_model_so_far = [None]
    best_samples_so_far = [None]

    def minimization_objective(params):
        eval_start_time = datetime.datetime.now()
        dp_alpha, sample_size_as_pct, pct_from_original, prior_for_a_beta_A, prior_for_a_beta_B, \
        prior_for_b_beta_A, prior_for_b_beta_B = params
        sample_size = int(math.floor(sample_size_as_pct * np.shape(X_train)[0]))

        pct_from_original = adjust_sample_from_dist(sample_size, pct_from_original, min_sample_size_per_dist)

        train_scores, val_scores,  test_scores = [], [], []
        sampling_trial_clfs = []
        optimizer_samples = []
        for i in range(sampling_trials):
            logging.info("Running sampling trial: %d of %d" % (i + 1, sampling_trials))
            temp_sample_info = sample_using_oracle(sample_size, X_train, y_train, uncertainties,
                                                   dp_alpha, prior_for_a_beta_A,
                                                   prior_for_a_beta_B, prior_for_b_beta_A,
                                                   prior_for_b_beta_B,
                                                   pct_from_original=pct_from_original, scale_a=scale, scale_b=scale,
                                                     use_weights=use_weights, num_weight_trials=num_weight_trials)

            sample_X, sample_y = temp_sample_info[:2]
            if use_weights:
                sample_weights = temp_sample_info[2]

            optimizer_samples.append(temp_sample_info)
            num_unique_lables_in_sample = len(set(sample_y))
            if num_unique_lables_in_sample< 2:
                logging.debug("Sample has only 1 label!")

            if len(sample_X) > 0 and num_unique_lables_in_sample > 1:
                logging.info("Fitting model within optimizer iteration.")
                if use_weights:
                    temp_ret = model_obj.fit_model_within_iteration(sample_X, sample_y, weights=sample_weights)
                else:
                    temp_ret = model_obj.fit_model_within_iteration(sample_X, sample_y)
                if temp_ret is None:
                    logging.debug("Fit within iteration returned None.")
                    train_trial_score, val_trial_score, test_trial_score, current_iter_model, current_iter_params = \
                        0, 0, 0, None, None
                else:
                    train_trial_score, val_trial_score, test_trial_score, current_iter_model, current_iter_params = \
                        temp_ret
            else:
                train_trial_score, val_trial_score, test_trial_score, current_iter_model, current_iter_params = \
                    0, 0, 0, None, None
            sampling_trial_clfs.append(current_iter_model)
            train_scores.append(train_trial_score)
            val_scores.append(val_trial_score)
            test_scores.append(test_trial_score)

        mean_train_score = np.mean(train_scores)
        mean_val_score = np.mean(val_scores)
        mean_test_score = np.mean(test_scores)
        non_None_sampling_trial_clfs = [t for t in sampling_trial_clfs if t is not None]
        if len(non_None_sampling_trial_clfs) > 0:
            avg_complexity = model_obj.get_avg_complexity(non_None_sampling_trial_clfs)
        else:
            avg_complexity = None

        if mean_val_score > best_mean_val_score_so_far[0]:
            best_mean_val_score_so_far[0] = mean_val_score
            best_model_so_far[0] = sampling_trial_clfs
            best_samples_so_far[0] = optimizer_samples

        logging.info("Optimizer current scores: train=%0.04f, val=%0.04f, test=%0.04f, best val=%0.04f" %
                                                                                        (mean_train_score,
                                                                                         mean_val_score,
                                                                                         mean_test_score,
                                                                                        best_mean_val_score_so_far[0]))
        loss = 1 - mean_train_score
        eval_end_time = datetime.datetime.now()
        eval_duration_sec = (eval_end_time - eval_start_time).total_seconds()
        return {'loss': loss, 'status': STATUS_OK, 'mean_train_score': mean_train_score,
                'mean_val_score': mean_val_score, 'mean_test_score': mean_test_score,
                'avg_complexity': avg_complexity, 'params': list(params),
                'start_time': str(eval_start_time), 'end_time': str(eval_end_time), 'duration_in_sec':eval_duration_sec}

    # initialize with one point - this represents the accuracy we'd get with the original dataset
    # we only need to ensure that sample_size_as_pct=1 and pct_from_original=1. The other values may be arbitrary
    # (but they must be feasible since the sampler would still be called and we dont want it to error out).

    max_sample_size_pct = 1.0
    if max_sample_size:
        max_sample_size_pct = 1.0 * max_sample_size / np.shape(X_train)[0]
    min_sample_size_pct = 1.0 * min_sample_size / np.shape(X_train)[0]
    search_space = create_search_space(max_components, min_sample_size, min_sample_size_pct,
                                       max_sample_size_as_pct=max_sample_size_pct,
                                       extended_space=use_extended_search_space, optimizer_type=optimizer)
    # if the optimizer is hyperopt, then we use the search space as is
    # but there is some handling required for pysot
    if optimizer in {'pysot', 'lipo'}:
        logging.info(f"Preparing search space for {optimizer}.")
        unif_search_space, log_transforms = search_space
        # get the lower and upper bounds
        lb, ub, transforms = [], [], []
        for k, v in unif_search_space.items():
            if k in log_transforms:
                transforms.append(math.exp)
            else:
                transforms.append(None)
            lb.append(v[0])
            ub.append(v[1])

    init_vals = [OrderedDict({'dp_alpha': 0.1,
                              'sample_size_as_pct': max_sample_size_pct,
                              'pct_from_original': 1.0,
                              'prior_for_a_beta_A': 1.0,
                              'prior_for_a_beta_B': 1.0,
                              'prior_for_b_beta_A': 1.0,
                              'prior_for_b_beta_B': 1.0
                              })]
    opt_var_key_order = init_vals[0].keys()

    # prepare a wrapper object for the optimization objective function because many libraries
    # require something like this
    class WrapperOpt(OptimizationProblem):
        def __init__(self):
            # super.__init__()
            self.dim = OPTVAR_DIMS
            self.int_var = np.array([])
            self.cont_var = np.arange(0, OPTVAR_DIMS)
            self.lb, self.ub = np.array(lb), np.array(ub)
            self.trials = []

        def eval(self, params):
            # transform the params if needed - pysot only supports uniform spaces
            tr_params = np.array([param if tr is None else tr(param) for param, tr in zip(params, transforms)])
            result = minimization_objective(tr_params)
            self.trials.append(result)
            return result['loss']

        def eval_d(self, **params):
            """
            This evaluates based on a dictionary of named variables. Required by LIPO.
            :param params:
            :return:
            """
            param_arr = np.array([params[k] for k in opt_var_key_order])
            return self.eval(param_arr)

    if optimizer == 'hyperopt':
        if additional_init_vals is not None:
            init_vals += additional_init_vals
        logging.info("%d init vals provided." % (len(init_vals)))

        trials = generate_trials_to_calculate(init_vals)

        best_params_train = fmin(minimization_objective,
                                 space=search_space,
                                 algo=tpe.suggest,
                                 max_evals=evals,
                                 trials=trials)
    elif optimizer == 'pysot':
        init_vals = [np.array(list(init_vals[0].values()))]
        if additional_init_vals is not None:
            init_vals += additional_init_vals
        init_vals = np.array(init_vals)
        logging.info("%d init vals provided." % (len(init_vals)))
        f = WrapperOpt()
        # pySOT doesn't evaluate the init vals automatically, we need to explicitly provide these
        logging.info(f"Obtaining response at init vals for pySOT, {len(init_vals)} evals needed.")
        init_vals_y = [f.eval(x_init) for x_init in init_vals]

        # set up a strategy and a controller
        rbf = RBFInterpolant(dim=OPTVAR_DIMS, lb=f.lb, ub=f.ub, kernel=CubicKernel(), tail=LinearTail(7))
        slhd = SymmetricLatinHypercube(dim=OPTVAR_DIMS, num_pts=2 * (OPTVAR_DIMS + 1))
        controller = SerialController(f.eval)
        pysot_strategy = 'srbf'
        if optimizer_params is not None:
            pysot_strategy = optimizer_params.get('strategy', 'srbf')
        if pysot_strategy == 'srbf':
            controller.strategy = SRBFStrategy(
                max_evals=evals, opt_prob=f, exp_design=slhd, surrogate=rbf, asynchronous=True,
                extra_points=init_vals, extra_vals=init_vals_y)
        elif pysot_strategy == "dycors":
            controller.strategy = DYCORSStrategy(
                max_evals=evals, opt_prob=f, exp_design=slhd, surrogate=rbf, asynchronous=True,
                extra_points=init_vals, extra_vals=init_vals_y)
        else:
            logging.error(f"Unknown pySOT strategy: {pysot_strategy}, aborting!!!")
            return

        # we also need to modify the controller fevals field for consistency
        for extra_idx in range(len(init_vals)):
            record = EvalRecord(params=(np.ravel(init_vals[extra_idx, :]),), status="completed")
            record.value = init_vals_y[extra_idx]
            record.feasible = True
            controller.fevals.append(record)
        logging.info(f"Updated controller records in pySOT - ready to run.")
        pysot_result = controller.run()
        logging.info(f"Finished pySOT run.")
        temp_explored_space = np.array([(list(t.params[0]) + [t.value]) for t in controller.fevals])
        visited_x, visited_y = temp_explored_space[:, :-1], temp_explored_space[:, -1]
        best_params_train = visited_x[np.argmin(visited_y), :]

    elif optimizer == "lipo":
        # LIPO accepts the dictionary format of init vals
        if additional_init_vals is not None:
            init_vals += additional_init_vals
        logging.info("%d init vals provided." % (len(init_vals)))
        f = WrapperOpt()
        # LIPO doesn't evaluate the init vals automatically, we need to explicitly provide these
        logging.info(f"Obtaining response at init vals for LIPO, {len(init_vals)} evals needed.")
        init_vals_y = [f.eval_d(**x_init) for x_init in init_vals]
        search = GlobalOptimizer(
            f.eval_d,
            lower_bounds=dict([(var, bound) for var, bound in zip(opt_var_key_order, f.lb)]),
            upper_bounds=dict([(var, bound) for var, bound in zip(opt_var_key_order, f.ub)]),
            flexible_bounds=dict([(var, [False, False]) for var in opt_var_key_order]), # bounds should be fixed
            evaluations=[(ix, iy) for ix, iy in zip(init_vals, init_vals_y)],
            maximize=False  # we're minimizing loss
        )
        search.run(evals)
        visited_x, visited_y = [], []
        for es in search.evaluations:
            visited_x.append([es[0][v] for v in opt_var_key_order])
            visited_y.append(-es[1])  # remember to flip the sign, a LIPO oddity
        visited_x, visited_y = np.array(visited_x), np.array(visited_y)
        best_params_train = visited_x[np.argmin(visited_y), :]

    trials_arr = None
    if optimizer == 'hyperopt':
        trials_arr = trials.results
    if optimizer in {'pysot', 'lipo'}:
        trials_arr = f.trials

    # write out the models
    suggested_model_path = "%s%sbest_mean_val_score_models" % (models_dir, os.sep)
    try:
        model_path = model_obj.save_model(best_model_so_far[0], suggested_model_path)
    except:
        logging.error(f"Couldn't write best model {suggested_model_path}!")
        model_path = ERRORED_SAVE_PATH

    # write out the best samples if requested
    if save_optimal_sample:
        with open(optimal_samples_file, 'wb') as f_opt_samples:
            pickle.dump(best_samples_so_far[0], f_opt_samples)

    logging.info("Best params based on train: %s" % (best_params_train,))
    result_json["optimized"] = {}
    result_json["optimized"]["model_path"] = model_path if model_path else suggested_model_path
    if optimizer == 'hyperopt':
        result_json["optimized"]["search_space"] = dict([(i, str(s)) for i, s in enumerate(search_space)])
    if optimizer in {'pysot', 'lipo'}:
        result_json["optimized"]["search_space"] = dict([(k, (f.lb[i], f.ub[i])) for i, k in enumerate(opt_var_key_order)])
    result_json["optimized"]["scale"] = scale
    result_json["optimized"]["best_params_train"] = list(best_params_train)
    with open(trials_file, 'w') as f_trials:
        f_trials.write(json.dumps(trials_arr, indent=4))

    # write the bootstrap score separately, for debugging purposes
    result_json["bootstrap"] = {}
    result_json["bootstrap"]["mean_train_score"] = trials_arr[0]["mean_train_score"]
    result_json["bootstrap"]["mean_val_score"] = trials_arr[0]["mean_val_score"]
    result_json["bootstrap"]["mean_test_score"] = trials_arr[0]["mean_test_score"]
    result_json["bootstrap"]["loss"] = trials_arr[0]["loss"]
    if optimizer == 'hyperopt':
        result_json["bootstrap"]["params"] = init_vals[0]
    if optimizer in {'pysot', 'lipo'}:
        result_json["bootstrap"]["params"] = dict([(i, j) for i, j in zip(opt_var_key_order, init_vals[0])])

    # find the best params on val
    best_iter_idx_val = max(enumerate(trials_arr), key=lambda t: t[1]["mean_val_score"])[0]
    if optimizer == 'hyperopt':
        # tpe internally stores params in the following object as dicts, but each value is wrapped in a list
        best_params_val = dict([(k, v[0])
                                for k, v in list(trials.trials[best_iter_idx_val]['misc']['vals'].items())])
        best_iter_idx_train = min([(h['loss'], idx) for idx, h in enumerate(trials.results)])[1]
        optimizer_scores = [i["mean_train_score"] for i in trials.results]
    if optimizer in {'pysot', 'lipo'}:
        best_params_val = visited_x[best_iter_idx_val, :]
        best_iter_idx_train = int(np.argmin(visited_y))
        optimizer_scores = visited_y

    result_json["optimized"]["best_params_val"] = list(best_params_val)
    result_json["optimized"]["best_iter_idx_val"] = best_iter_idx_val

    if compute_all_baselines is False:
        pct_changes_train, pct_changes_val = None, None
        best_train_improvement, best_val_improvement = None, None
    else:
        pct_changes_train = [100.0 * (s - baseline_train_score_based_on_train) / baseline_train_score_based_on_train
                               for s in optimizer_scores]
        pct_changes_val = [100.0 * (s["mean_val_score"] - baseline_val_score_based_on_train) /
                           baseline_val_score_based_on_train for s in trials_arr]
        best_train_improvement = max(pct_changes_train)
        best_val_improvement = max(pct_changes_val)

    pct_changes_test = [100.0 * (s["mean_test_score"] - baseline_test_score_based_on_train_val) /
                        baseline_test_score_based_on_train_val for s in trials_arr]
    test_improvement_obj_fn_best_params_val = pct_changes_test[best_iter_idx_val]
    # test_improvement_best_params_val = 100.0 * (trials.results[best_iter_idx_val]["mean_test_score"]
    #                                             - baseline_test_score_based_on_train_val) / \
    #                                    baseline_test_score_based_on_train_val

    logging.info("Improvement over baseline: %0.02f%%" % (test_improvement_obj_fn_best_params_val,))
    logging.info("Baseline score: %0.04f" % (baseline_test_score_based_on_train_val))

    # sample_pct = 1.0 * sample_size/np.shape(X_train_val)[0]
    result_json["optimized"]["total_trials"] = len(trials_arr)
    result_json["optimized"]["best_val_score"] = trials_arr[best_iter_idx_val]["mean_val_score"]
    result_json["optimized"]["test_score_obj_fn_at_best_params_val"] = \
        trials_arr[best_iter_idx_val]["mean_test_score"]
    result_json["optimized"]["avg_train_complexity_best_params_val"] = \
        trials_arr[best_iter_idx_val]["avg_complexity"]

    result_json["optimized"]["best_train_score"] = max(optimizer_scores)
    result_json["optimized"]["improvement_best_train"] = best_train_improvement
    result_json["optimized"]["improvement_best_val"] = best_val_improvement
    result_json["optimized"]["improvement_test_obj_fn_best_params_val"] = \
        test_improvement_obj_fn_best_params_val

    avg_complexity_for_best_model = model_obj.get_avg_complexity(best_model_so_far[0])
    result_json["optimized"]["avg_model_complexity_for_best_param_val"] = \
        str(avg_complexity_for_best_model)
    result_json["optimized"]["avg_model_complexity_for_best_param_val_pickled_hex"] = \
        pickle.dumps(avg_complexity_for_best_model).hex()

    result_json["optimized"]["best_iter_idx_train"] = best_iter_idx_train
    result_json["optimized"]["best_iter_idx_val"] = best_iter_idx_val

    # plot the optimizer progress
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if compute_all_baselines:
        best_so_far_train = [pct_changes_train[0]]
        for i in range(1, len(pct_changes_train)):
            best_so_far_train.append(best_so_far_train[-1]
                                       if pct_changes_train[i] <= best_so_far_train[-1] else pct_changes_train[i])

        best_so_far_val = [pct_changes_val[0]]
        for i in range(1, len(pct_changes_val)):
            best_so_far_val.append(best_so_far_val[-1]
                                       if pct_changes_val[i] <= best_so_far_val[-1]
                                          else pct_changes_val[i])
        ax.plot(list(range(len(pct_changes_train))), pct_changes_train, lw=0.5, label="progress", c='gray')
        ax.plot(list(range(len(pct_changes_train))), best_so_far_train, lw=1, label="curr. best train", c='green')
        ax.plot(list(range(len(pct_changes_val))), best_so_far_val, lw=1, label="curr. best val", c='blue')

    best_so_far_test = [pct_changes_test[0]]
    for i in range(1, len(pct_changes_test)):
        best_so_far_test.append(best_so_far_test[-1]
                                      if pct_changes_test[i] <= best_so_far_test[-1]
                                      else pct_changes_test[i])

    ax.plot(list(range(len(pct_changes_test))), best_so_far_test, lw=1, label="curr. best test", c='red')
    ax.axhline(y=test_improvement_obj_fn_best_params_val, lw=1, linestyle="--", label="optimal (%0.02f%%)"
                                                                    % test_improvement_obj_fn_best_params_val, c='red')

    ax.set_xlabel('iterations')
    ax.set_ylabel('% change')
    # ax.set_title("test=%0.02f%%" %(test_improvement_best_params_val_report,))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='upper right', bbox_to_anchor=(1.5, 1))
    fig.savefig(optimizer_progress_plot_file, bbox_inches='tight')

    # plot the train-val-test scores, to ensure no overfitting is happening
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(list(range(len(trials_arr))), [t["mean_train_score"] for t in trials_arr], lw=0.5, label="train", c='green')
    ax.plot(list(range(len(trials_arr))), [t["mean_val_score"] for t in trials_arr], lw=0.5, label="val", c='blue')
    ax.plot(list(range(len(trials_arr))), [t["mean_test_score"] for t in trials_arr], lw=0.5, label="test", c='red')
    ax.set_xlabel('iterations')
    ax.set_ylabel('F1')
    # ax.set_title("test=%0.02f%%" %(test_improvement_best_params_val_report,))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.95, box.height])
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    fig.savefig(scores_plot_file, bbox_inches='tight')

    # plot the original dataset and the sampled dataset if possible
    label_colormap = utils.get_label_colormap(y)
    if np.shape(X)[1] == 2 and label_colormap is not None:
        fig = plt.figure()
        ax = fig.add_subplot(121)
        ax.scatter(X[:, 0], X[:, 1], c=utils.get_label_colors(y, label_colormap), s=1, lw=0)
        ax.set_title("dataset:%s" % (dataset_name,))

        ax = fig.add_subplot(122)
        sample_size = int(best_params_val["sample_size_as_pct"] * np.shape(X_train)[0])
        sample_X, sample_y = sample_using_oracle(sample_size, X_train, y_train, uncertainties,
                                                 best_params_val["dp_alpha"],
                                                 best_params_val["prior_for_a_beta_A"],
                                                 best_params_val["prior_for_a_beta_B"],
                                                 best_params_val["prior_for_b_beta_A"],
                                                 best_params_val["prior_for_b_beta_B"],
                                                 pct_from_original=adjust_sample_from_dist(sample_size,
                                                                                         best_params_val["pct_from_original"],
                                                                                         min_sample_size_per_dist))
        ax.scatter(sample_X[:, 0], sample_X[:, 1], c=utils.get_label_colors(sample_y, label_colormap), s=1, lw=0)
        ax.set_title("best sample")
        fig.savefig(sample_plot_file, bbox_inches='tight')
    end_time = datetime.datetime.now()
    result_json["runtimes"]["total_runtime_in_secs"] = (end_time - start_time).total_seconds()
    with open(results_file, 'w') as f_res:
        f_res.write(json.dumps(result_json, indent=4, sort_keys=True))
        f_res.flush()
    return test_improvement_obj_fn_best_params_val, best_params_val, new_persistence_obj


if __name__ == "__main__":
    pass
    # tpe_evals = 3000
    # base_dir = r'../data/oracle_based/scikit_dt'
    #
    # dataset = 'circle'
    # X, y = comm_utils_data_load.load_data(dataset)
    # X, _, y, _ = train_test_split(X, y, train_size=10000, stratify=y)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, stratify=y)
    # rf = get_oracle_calibrated_gbm(X_train, y_train)
    # #rf = get_oracle_gbm(X_train, y_train)
    # #rf = get_oracle_scikit_rf(X_train, y_train)
    # rf = get_oracle_calibrated_gbm(X_train, y_train)
    # y_pred = rf.predict(X_test)
    # #print rf.best_iteration
    # print f1_score(y_test, y_pred)
    # perf = {}
    # for max_depth in range(1, 16):
    #     logging.info("current MAX_DEPTH=%d"%(max_depth,))
    #     model_obj = scikitDT(max_depth)
    #     score, _, _ = run_experiment('circle', model_obj, oracle=get_oracle_gbm,
    #                    evals=tpe_evals, min_sample_size=1000, min_sample_size_per_dist=300,
    #                    sampling_trials=1,
    #                    splits=None,
    #                    dataset_name='circle',
    #                    baseline_fit_folds=3,
    #                    create_persistence_obj=False, use_persistence_obj=None,
    #                    working_dir=base_dir + os.sep + str(max_depth))
    #     perf[max_depth] = score
    #
    # logging.info(str(perf))