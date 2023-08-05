import platform
#
# if platform.system() == 'Linux':
#     import matplotlib as mpl
#
#     mpl.use('Agg')
import sys, os, string, pickle
from matplotlib import pyplot as plt
from copy import deepcopy
import random, bisect
import glob, json, re, datetime
import traceback
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import f1_score
from compactem.core import oracle_transfer
import multiprocessing as mp
from compactem.model_builder import DecisionTree, ModelBuilderBase
import compactem.model_builder
from compactem.utils import data_format as du
from compactem.utils.utils import is_iterable
# import InteractionModel
# import glmnetModel
import numpy as np
from collections import defaultdict, OrderedDict
import seaborn as sns; sns.set()
import logging
# import oracles
# from compactem.oracles import CalibratedGradientBoostedModel, OracleBase
from compactem.utils.output_processors import filenames, Result
from typing import Iterable, Union, Dict, Optional, Callable
logger = logging.getLogger(__name__)




def run_experiment_p(arg_dict):
    """
    A parallelizable version of 'run_experiment()'
    :param arg_dict:
    :return:
    """
    result = None
    # swallow any SIGTERMS
    try:
        result = oracle_transfer.run_experiment(**arg_dict)
        return result
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        logging.info(''.join('!! ' + line for line in lines))
        return result
    finally:
        return result


def complexity_as_str(complexity):
    """
    This is for creating directory names.
    If the complexity has alphanumeric chars, we use those and separate by underscores.
    There is an exception - if this is a float  (not castable to an int), we round it to 4 places, and add a 6 char
    random string
    :param complexity:
    :return:
    """
    s = ""
    if type(complexity) in (float, np.float16, np.float32, np.float64) and (int(complexity) != complexity):
        if int(complexity) != complexity:
            s = '%0.04f_' % (complexity,)
            s = s.replace(".", "_")
            for i in range(6):
                s += random.choice(string.lowercase)
        else:
            s = str(int(complexity))

    elif type(complexity) == int:
        s = str(complexity)
    else:
        s = "_".join(x for x in str(complexity) if x.isalnum())
    return s


def flatten_curve(orig_a,
                  lower=0.1, upper=0.9, num_bins=20,
                  plot=False, return_bin_info=False):
    """
    points assumed to be in [0, 1]
    :param a:
    :return:
    """
    t = np.argsort(orig_a)
    a = orig_a[t]

    # bin shift
    # lower, upper, num_bins = 0.1, 0.9, 20
    points_in_bins = list(map(len, np.array_split(list(range(len(a))), num_bins)))
    boundaries = np.linspace(lower, upper, num_bins + 1)
    bin_formatted_sample = []
    min_max_scalers, deltas = [], []
    for idx, num_points in zip(list(range(num_bins)), points_in_bins):
        boundary_low, boundary_high = boundaries[idx], boundaries[idx+1]
        delta = (boundary_high - boundary_low)/20.0
        deltas.append(delta)
        curr_bin_sample = a[sum(points_in_bins[:idx]):sum(points_in_bins[:idx]) + points_in_bins[idx]]
        curr_scaler = MinMaxScaler((boundary_low+delta, boundary_high-delta))
        min_max_scalers.append(curr_scaler)
        transformed = curr_scaler.fit_transform(curr_bin_sample.reshape(-1,1)).flatten()
        bin_formatted_sample += transformed.tolist()
    bin_formatted_sample = np.array(bin_formatted_sample)
    order_restored = np.zeros(len(orig_a))
    for i, j in zip(bin_formatted_sample, t):
        order_restored[j] = i
    rank_order_match = np.all(np.argsort(orig_a) == np.argsort(order_restored))
    if rank_order_match is False:
        notif_msg = "ERROR! Rank order did not match!"
        print(notif_msg)
        logging.error(notif_msg)
        return
    if plot:
        sns.kdeplot(orig_a, color='b')
        sns.kdeplot(order_restored, color='g')
        plt.show()

    logging.info("Rank order matched!")

    if return_bin_info:
        return order_restored, {'lower': lower, 'upper': upper, 'bins': num_bins, 'boundaries': boundaries,
                                'scalers': min_max_scalers, 'deltas': deltas}
    return order_restored


def nullable_dict_merge(h_primary, h_secondary):
    """
    Merges two dictionaries accounting for either of them being passed in as None.

    :param h_primary: this dict gets priority in case of key conflicts.
    :param h_secondary: dict that is to be merged into h_primary.
    :return: merged dict
    """
    temp_pri = h_primary if h_primary else dict()
    temp_sec = h_secondary if h_secondary else dict()
    # because temp_pri can override temp_sec this has to be the order of updating
    temp_sec.update(temp_pri)
    merged = None if len(temp_sec) == 0 else temp_sec
    return merged


def compact_using_oracle(datasets_info: Union[du.DataInfo, Iterable[du.DataInfo]],
                         model_builder_class: ModelBuilderBase,
                         oracle: Union[Callable, Dict[str, du.UncertaintyInfo]],
                         task_dir: str, overwrite: bool=False,
                         poolsize: int = -1, runs: int = 1,
                         model_init_info: Optional[Dict] = None, oracle_params: Optional[Dict] = None,
                         flatten=True, max_components: int = 500, scale: float = 10000,
                         min_sample_size: int = 400, min_sample_size_per_dist: int = 200,
                         max_sample_size: Optional[int] = None,
                         sampling_trials: int = 3,
                         use_weights: bool = False, num_weight_trials: int = 10,
                         save_optimal_sample: bool = False,
                         optimizer: str = 'hyperopt',
                         optimizer_params: dict = None):
    """
    This is the main entry function for a user.

    :param datasets_info: this is the data on which models/oracles are to be built. This must be an object of type
        :any:`compactem.utils.data_format.DataInfo`, or in case of multiple datasets, a list of such objects.

        The complexity params for ``DataInfo`` object **may be None**, in which case determining the complexity
        param range would be attempted by calling
        ``get_complexity_param_range()`` on the `model_builder_class` parameter.
        If this is not implemented, the function is aborted.
    :param model_builder_class: this is the class used to train models of various complexities. This must be a subclass
        of :any:`compactem.model_builder.base_model.ModelBuilderBase`.
    :param oracle: the oracle training *function*, or alternatively a *dict* where the key is a dataset names and
        the value is an object of type :any:`compactem.utils.data_format.UncertaintyInfo`.

        If a dict is passed, the keys should exactly match the dataset names
        passed as part of the DataInfo objects assigned to the datasets_info parameter.

        The oracle can be a function or a dict - these two types cannot be mixed.
    :param task_dir: output directory where results would be stored. **This should be empty** - since processing of
        results can be confounded by outputs from prior runs. If not empty, this throws an error, unless parameter
        ``overwrite is True``.

        This directory is created (including subdirectories in the path if needed) if it does not exist.

    :param overwrite: if True, even if task_dir is not empty, use it anyway. NOTE: this does not delete existing
        contents, just overwrites the files in conflict.
    :param poolsize: number of processes to use. A poolsize of < 1 creates ``multiprocessing.cpu_count()`` number of
        processes.
    :param runs: the number of times the whole experiment is repeated. For ex if you have one dataset only, with 3
        complexities to build models for, then if ``runs==1``, 3 models would be constructed, one for each complexity.
        If ``runs==2``, 6 models would be constructed, 2 per complexity.
        This is intended for rigorous reporting of results.
    :param model_init_info: initialization parameters that would be passed to the model builder object. The same params
        would be passed into all model builder initializations. If a specific DataInfo object has a non-None
        ``additional_info`` field, then these two dicts are merged, with the ``additional_info`` keys taking priority
        in case of a conflict.
    :param oracle_params: these are passed into the oracle learner function.
    :param flatten: whether to flatten the uncertainty distribution from the oracle; it's safe to set this to True in
        most cases; adds some minor processing overhead, but potentially improves accuracy.
    :param max_components: number of mixture components the distribution to be modelled might have; it's safe to keep
        defaults if you don't have a good guess. This adds processing overhead, but makes the algorithm likely to
        succeed across a wide variety of datasets.
    :param scale: this is the scale parameter in scipy's
        `beta implementation <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.beta.html>`_. Safe to use
        defaults unless domain knowledge suggests otherwise.
    :param min_sample_size: lower bound on the number of points optimizer can sample
    :param min_sample_size_per_dist: since the sampling happens from both the mixture model and the original
        distribution, use this to set the min samples per distribution. It's safe to set this to
        half of ``min_sample_size``.
    :param max_sample_size: upper bound on how many samples can the optimizer pick; this is useful for analysis of
        samples picked, but for the use case of getting a compact model, it is better to allow the optimizer to
        potentially use up all points (this is what ``max_sample_size=None`` does).

        If you want to save time by reducing the dataset size, consider doing that outside this function,
        and passing in only the reduced dataset.
    :param sampling_trials: the number of model fits the optimizer performs within each iteration. Option provided for
        robustness.
    :param use_weights: you can avoid sampling and fitting (which can be expensive) by using instance weights instead,
        IF your classifier supports learning using instance weights. If this is set to True, sampling_trials MUST be
        set to 1
    :param num_weight_trials: if use_weights is True, this is the number of times instance weights would be averaged
    :param save_optimal_sample: whether the optimal sample found should be saved. Note this would save the optimal
        sample for all model complexity+dataset combinations. This is helpful for post-hoc analysis of the
        optimal sample.
    :param optimizer: optimizer backend to use, currently supported "hyperopt" (default) or "pysot"
    :param optimizer_params: if the optimizer accepts params, they need to be passed in as a dict. There is no standard
        format for this, and would be parsed in an optimizer specific way. Current supported:
        * for optimizer=pysot, this parameter can be {"strategy": "srbf"} or {"strategy": "dycors"}

    :return: dataframe of results aggregated across runs.
    """
    num_flatten_bins = 20
    task_info_file = os.path.join(task_dir, filenames['task_info'])
    flattening_info_filename = filenames['flattening_info']
    indices_filename = filenames['indices']

    # some basic checks - since this is a user facing function, we want to fail early and return helpful errors

    if os.path.exists(task_dir) and os.path.isdir(task_dir) and os.listdir(task_dir):
        if overwrite:
            logging.warning(f"Provided output directory '{task_dir}' is not empty, but argument asks to "
                            f"use it anyway.")
        else:
            notif_msg = f"Provided output directory '{task_dir}' is not empty, will abort. If you want to" \
                        f" use a non-empty directory anyway, set the overwrite parameter to True."
            logging.error(notif_msg)
            print(notif_msg)
            raise ValueError

    if not os.path.exists(task_dir) or not os.path.isdir(task_dir):
        os.makedirs(task_dir)

    if isinstance(datasets_info, du.DataInfo):
        datasets_info = [datasets_info]

    if not du.validate_dataset_info(datasets_info):
        notif_msg = "datasets_info is not valid!"
        logging.error(notif_msg)
        raise TypeError(notif_msg)

    if not issubclass(model_builder_class, ModelBuilderBase):
        notif_msg = "model_builder_class must be of type ModelBuilderBase!"
        logging.error(notif_msg)
        raise TypeError(notif_msg)

    # if not isinstance(oracle, OracleBase) and not isinstance(oracle, dict):
    if not callable(oracle) and not isinstance(oracle, dict):
        notif_msg = "oracle must be of type dict or OracleBase!"
        logging.error(notif_msg)
        raise TypeError(notif_msg)

    if isinstance(oracle, dict):
        dataset_names = set([i.dataset_name for i in datasets_info])
        datasets_wih_unc_info = set(oracle.keys())
        missing_datasets = dataset_names -datasets_wih_unc_info
        if len(missing_datasets) > 0:
            notif_msg = "Some datasets are missing uncertainty info: %s" % (",".join(missing_datasets))
            logging.error(notif_msg)
            raise KeyError(notif_msg)

        # if uncertainty info are provided then (1) splits can have only data
        # (2) the length of the list must match training data size - this check happens downstream.
        # For (1) we just check one value in the splits dict.

        if not np.all([is_iterable(list(i.splits.values())[0]) for i in datasets_info]):
            notif_msg = "When oracle is a dict, splits can have only the exact data splits!"
            logging.error(notif_msg)
            raise ValueError(notif_msg)

    # all checks done, lets begin with the actual experiment setup

    if poolsize <= 0:
        poolsize = mp.cpu_count()
        logging.info("Will train with poolsize=%d." % (poolsize,))

    with open(task_info_file, 'w') as f_task:
        f_task.write(json.dumps({'task_dir': task_dir, 'start_time': str(datetime.datetime.now())}))


    # config variables
    recompute_unbounded_model = False
    isolate_runs = True
    # evals_for_dataset = {'covtype.binary': 3000, 'Sensorless': 1000}
    # evals_for_dataset = {'letter': 30}
    # evals_for_dataset = dict([(dataset, 3000) for dataset in BINARY_DATASETS])
    # evals_for_dataset.update(dict([(dataset, 1000) for dataset in MULTICLASS_DATASETS]))
    # evals_for_dataset = {'Sensorless': 5}
    # dataset_names = list(evals_for_dataset.keys())
    # dataset_size = 10000
    # DEFAULT_SPLITS = {'train': 0.6, 'val': 0.2, 'test': 0.2}
    min_sample_size, min_sample_size_per_dist, sampling_trials = min_sample_size, min_sample_size_per_dist, \
                                                                 sampling_trials
    # experimentally I've observed a good scale to be 10000
    max_components, scale = max_components, scale

    for run_idx in range(runs):
        logging.info("Starting on run %d of %d." % (run_idx + 1, runs))

        # loading the dataset is randomized too - hence its inside the run loop
        # datasets = {}
        # logging.info("Loading datasets.")
        # for dataset in dataset_names:
        #     X, y = comm_utils_data_load.load_data(dataset)
        #     X, _, y, _ = train_test_split(X, y, train_size=dataset_size, stratify=y)
        #     datasets[dataset] = (X, y)
        # logging.info("Finished loading datasets.")

        run_expt_args = []

        run_dir = task_dir + os.sep + "run_%d" % (run_idx + 1)
        if not os.path.exists(run_dir):
            os.makedirs(run_dir)

        # split the datasets
        for dataset in datasets_info:
            if dataset.data:
                X, y = dataset.data
                X_train, y_train, idx_train, X_train_val, y_train_val, idx_train_val, X_val, y_val, idx_val, X_test, \
                y_test, idx_test = oracle_transfer.process_splits(X, y, dataset.splits,
                                                                  randomize=True, return_indices=True)
                logging.info("Performed split on dataset: %s" % (dataset.dataset_name,))
            else:
                X_train, y_train = dataset.splits['train']
                X_val, y_val = dataset.splits['val']
                X_test, y_test = dataset.splits['test']
                idx_train = list(range(len(X_train)))
            # evals = evals_for_dataset[dataset]
            # X_train, y_train, X_train_val, y_train_val, X_val, y_val, X_test, y_test = \
            #     oracle_transfer.process_splits(X, y, DEFAULT_SPLITS, randomize=True)
            # logging.info("Performed split on dataset: %s" % (dataset,))

            if callable(oracle):
                ora_name = oracle.__name__
                logging.info('Training oracle on training data.')
                if oracle_params:
                    oracle_model = oracle(X_train, y_train, **oracle_params)
                else:
                    oracle_model = oracle(X_train, y_train)
                y_pred_test = oracle_model.predict(X_test)
                test_F1_macro = f1_score(y_test, y_pred_test, average='macro')
                # compute uncertainties
                probs = oracle_model.predict_proba(X_train)
                train_uncertainties = oracle_transfer.uncertainty(probs)

            elif isinstance(oracle, dict):
                ora_name = "Unc. provided"
                test_F1_macro = oracle[dataset.dataset_name].oracle_accuracy
                train_uncertainties = oracle[dataset.dataset_name].uncertainty_scores

                if np.shape(train_uncertainties)[0] != np.shape(dataset.splits['train'][0])[0]:
                    notif_msg = f"number of uncertainty values must match size of X_train for " \
                                f"dataset {dataset.dataset_name}"
                    logging.error(notif_msg)
                    raise ValueError(notif_msg)

            else:
                logging.error("Invalid oracle, returning!")
                return

            # oracle_model = oracle(X_train, y_train)
            # y_pred_test = oracle_model.predict(X_test)
            # test_F1_macro = f1_score(y_test, y_pred_test, average='macro')


            orig_train_uncertainties = deepcopy(train_uncertainties)

            if flatten:
                train_uncertainties, flattening_info = flatten_curve(np.array(train_uncertainties),
                                                                     num_bins=num_flatten_bins,
                                                                     plot=False, return_bin_info=True)
            complexity_params = dataset.complexity_params
            if complexity_params:
                if len(complexity_params) == 0:
                    notif_msg = f"Iterable complexity_params for dataset {dataset.dataset_name} is empty, skipping."
                    logging.error(notif_msg)
                    raise ValueError(notif_msg)
            else:
                logging.info("Model complexity range was not provided for dataset %s, trying to fetch from model class"
                             % (dataset.dataset_name,))
                complexity_params = model_builder_class.get_complexity_param_range(X, y)
                logging.info("Obtained complexity range for dataset %s: %s" % (dataset.dataset_name,
                                                                               str(complexity_params)))
            for model_size_idx, model_size_param in enumerate(sorted(complexity_params)):
                # instead of the model_size param use the idx --- much less likely to cause OS issues
                working_dir = run_dir + os.sep + "%s_%s" % (dataset.dataset_name, model_size_idx)
                if not os.path.exists(working_dir):
                    os.makedirs(working_dir)

                with open(os.path.join(working_dir, indices_filename), 'w') as f_indices:
                    f_indices.write(json.dumps({'idx_train': list(idx_train), 'y_train': y_train.tolist()}))

                if flatten:
                    with open(working_dir + os.sep + flattening_info_filename, 'wb') as f_flat_info:
                        pickle.dump(flattening_info, f_flat_info)

                    with open(working_dir + os.sep + "original_uncertainties.txt", 'w') as f_orig_unc:
                        f_orig_unc.write("\n".join(["%f"%(x,) for x in orig_train_uncertainties]))

                    fig = plt.figure()
                    ax = fig.add_subplot(111)
                    sns.kdeplot(orig_train_uncertainties, color='b', ax=ax, label="original")
                    sns.kdeplot(train_uncertainties, color='g', ax=ax, label="flattened")
                    ax.set_xlabel('uncertainty')
                    ax.set_ylabel('pdf')
                    ax.set_xlim(-0.2, 1.2)
                    # plt.savefig(working_dir + os.sep + "unc_dists.svg")
                    box = ax.get_position()
                    ax.set_position([box.x0, box.y0, box.width * 0.95, box.height])
                    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
                    fig.savefig(working_dir + os.sep + "unc_dists.png", bbox_inches='tight')
                    plt.close(fig)

                uncertainty_info = {'oracle_score': test_F1_macro, 'uncertainties': train_uncertainties,
                                    'str_info': ora_name}

                init_info = nullable_dict_merge(dataset.additional_info, model_init_info)
                model_obj = model_builder_class(model_size_param, init_info) if init_info \
                    else model_builder_class(model_size_param)
                expt_args = {'dataset': None, 'model_obj': model_obj, 'oracle': None,
                             'evals': dataset.evals,
                             'splits': {'train': (X_train, y_train), 'val': (X_val, y_val),
                                                        'test': (X_test, y_test)},
                             'uncertainty_info': uncertainty_info,
                             'dataset_name': dataset.dataset_name,
                             'min_sample_size': min_sample_size,
                             'min_sample_size_per_dist': min_sample_size_per_dist,
                             'max_sample_size': max_sample_size,
                             'sampling_trials': sampling_trials,
                             'working_dir': working_dir,
                             'max_components': max_components,
                             'scale': scale,
                             'compute_all_baselines': False,
                             'save_optimal_sample': save_optimal_sample,
                             'optimizer': optimizer,
                             'optimizer_params': optimizer_params,
                             'use_weights': use_weights,
                             'num_weight_trials': num_weight_trials
                             }
                run_expt_args.append(expt_args)

        logging.info('Arguments constructed for run %d - will dispatch.' % (run_idx + 1))
        p = mp.Pool(poolsize)
        results = p.map(run_experiment_p, run_expt_args)
        p.close()
        p.join()
        logging.info('Finished run %d.' % (run_idx + 1))
    result_obj = Result(task_dir)
    result_obj.process_results()
    aggr_results = result_obj.read_processed_results()
    return aggr_results


def invert_flattened_data(X, bin_info):
    """
    This maps X to the original data distribution. Essentially, this inverts the transformation created by
    flatten_curve(). The bin_info is required.

    :param X: data for inverse transformation
    :param bin_info: object returned by flatten_curve()
    :return:
    """
    if bin_info is None:  # pass through
        return X
    num_bins = len(bin_info['boundaries']) - 1
    X = np.array(X)
    temp = np.digitize(X, bin_info['boundaries'])
    temp = np.clip(temp, 1, num_bins)
    bin_idxs = temp - 1  # the bin numbers produced by digitize start at 1
    X_inv = np.zeros(X.shape)
    for b_idx in sorted(set(bin_idxs)):
        x_idxs = np.where(bin_idxs==b_idx)[0]
        current_scaler = bin_info['scalers'][b_idx]
        temp_inv = current_scaler.inverse_transform(X[x_idxs].reshape(-1, 1))
        temp_inv = temp_inv.flatten()

        # this clipping is necessary because some points might have been assigned to this bin due to digitize + clipping
        # and they might actually fall outside the actual scalers boundaries (different from bin boundaries). Also since
        # the bin boundaries dont start at 0 and end at 1, we allow extreme values at the boundaries and adjust them
        # them later.
        if b_idx == 0:
            temp_inv = np.clip(temp_inv, a_min=None, a_max=bin_info['boundaries'][b_idx+1])
        elif b_idx == num_bins - 1:
            temp_inv = np.clip(temp_inv, a_min=bin_info['boundaries'][b_idx], a_max=None)
        else:
            temp_inv = np.clip(temp_inv, bin_info['boundaries'][b_idx], bin_info['boundaries'][b_idx+1])
        X_inv[x_idxs] = temp_inv

    # for values beyond boundaries, we will spread them out uniformly
    low_b, high_b = bin_info['boundaries'][0], bin_info['boundaries'][-1]
    low_idxs, high_idxs = np.where(X_inv < low_b)[0], np.where(X_inv > high_b)[0]
    if len(low_idxs) > 0:
        X_inv[low_idxs] = MinMaxScaler(feature_range=(0.0, low_b)).fit_transform(X_inv[low_idxs].reshape(-1, 1)).flatten()
    if len(high_idxs) > 0:
        X_inv[high_idxs] = MinMaxScaler(feature_range=(high_b, 1.0)).fit_transform(X_inv[high_idxs].reshape(-1, 1)).flatten()
    #X_inv = np.clip(X_inv, 0.0, 1.0)
    return X_inv


def arbitrary_function_runner(t):
    """
    In Python 2.7 it is required that for a function to be run via te multiprocessing module, it has to be statically
    defined and it must take as an input. Which implied we need to create such a version for each function.

    Instead we use this "caller". t[0] is the function to call within multiprocessing, and t[1] are its arguments as a
    dict.
    """

    result = None
    # swallow any SIGTERMS
    try:
        result = t[0](**t[1])
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        logging.info(''.join('!! ' + line for line in lines))
        return result
    finally:
        return result





if __name__ == "__main__":
    # for i in range(3):
    #     config_real_datasets(16, r'../data/dt_based_density/overfitting_tests/100_real_data_%d'%(i,))
    # read_results(r'../data/dt_based_density/real_data', r'real_data_experiment_summary', smooth=False)
    # model_class = scikitDT.scikitDT
    # model_class = LinearProbabilityModel.LinearProbabilityModel
    # model_class = InteractionModel.InteractionModel
    # model_class = GradientBoostingModel.GradientBoostingModel
    # model_class.max_depth = 2
    # model_class = glmnetModel.glmnetModel
    # config_dataset_runs_with_persistence(8, r'../data/oracle_based/icde_round_2_additional_runs/small_scikitdt_ora_scikitrf_run2',
    #                                      model_class)
    # config_dataset_runs_with_persistence(8,
    #                                      r'../data/oracle_based/icde_round_2_additional_runs/small_scikitdt_ora_scikitrf_run3',
    #                                      model_class)

    # model_class = LinearProbabilityModel.LinearProbabilityModel
    # config_dataset_runs_with_persistence(8,
    #                                      r'../data/oracle_based/icde_round_2_additional_runs/small_scikitdt_ora_calgbm_run2',
    #                                      model_class)
    # config_dataset_runs_with_persistence(8,
    #                                      r'../data/oracle_based/lpm_bug_test',
    #                                      model_class)
    # oracle_transfer_wth_uncertainty_prior()
    # test_with_uncertainty_sampling(1000, smoothing_coeff=0)
    # orig_a = beta.rvs(a=0.5, b=4.5, size=1000)
    # sns.kdeplot(orig_a, color='b', bw=0.05)
    # boxcox_a = MinMaxScaler().fit_transform(boxcox(orig_a)[0].reshape(-1, 1)).flatten()
    # qt_a = QuantileTransformer(n_quantiles=2, random_state=0, output_distribution='uniform').fit_transform(orig_a.reshape(-1, 1)).flatten()
    # transformed_a = MinMaxScaler().fit_transform(qt_a.reshape(-1, 1)).flatten()
    # sns.kdeplot(transformed_a, color='g', bw=0.05)
    # rank_match = np.all(np.argsort(orig_a)==np.argsort(transformed_a))
    # plt.title(str(rank_match))
    # plt.show()
    # flatten_curve(orig_a, plot=True, lower=0.05, upper=0.95, num_bins=10)
    # experiment_inverse_transformation()


    # model_class = LinearProbabilityModel
    # model_class = DecisionTree
    # oracle_obj = CalibratedGradientBoostedModel(max_rounds=10)
    # # oracle_fit_fn = oracle_transfer.get_oracle_scikit_rf
    # #
    # base_dir = r"output"
    # compact_using_oracle(poolsize=8, model_builder_class=model_class,
    #                      oracle=oracle_obj, runs=1,
    #                      base_dir=base_dir, flatten=False, max_components=50, scale=10)
    # # test_arbitrary_exit_fixes()

    # missed_fits_file = r'../data/oracle_based/flattened_runs_final/missed_fits/scikitDT_rf_missed_fits.csv'
    # original_runs_with_missed_fits = r'../data/oracle_based/flattened_runs_final/scikitDT_rf'
    # op_dir = r'../data/oracle_based/flattened_runs_final/missed_fits/scikitDT_rf'
    #
    # missing_fits_df = generate_missing_fits(original_runs_with_missed_fits)
    # missing_fits_df.to_csv(missed_fits_file)
    # rerun_missed_fits(missing_fits_df, poolsize=8, model_class=model_class, oracle_fit_fn=oracle_fit_fn,
    #                   base_dir=op_dir, flatten=True)
    # test_inversion()

    # get_size_correspondences([1, 2, 3, 4, 5], [0.1, 0.2, 0.3, 0.4, 0.5], [0.3, 0.3, 0.4, 0.45, 0.5])
    pass