import sys, os, copy, itertools, math
from compactem.model_builder.base_model import ModelBuilderBase
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from collections import Counter
import numpy as np, pandas as pd
import logging
logger = logging.getLogger(__name__)
sys.path.append(os.sep.join([os.path.dirname(os.path.abspath(__file__)), '..', '..', 'common_utils']))
from compactem.utils import data_load as comm_utils_data_load
import lightgbm as lgbm


def get_balanced_sample_weights(y):
    """
    This function coputes sample weight in a way that all classes end up with the same total weight. We need to perform
    this step since LightGBM doesn't allow class weights.

    :param y: list of labels (we don't need instances per se to calculate weights)
    :return: sample weights, list of floats with same length as y
    """
    # we assume the weights of the dominant class is 1, this was thats the smallest weight, and we don't need
    # to worry about underflow
    c = Counter(y)
    dominant = max(list(c.items()), key=lambda t: t[1])[0]
    weights_for_class = {dominant: 1.0}
    for k in set(c.keys()) - {dominant}:
        weights_for_class[k] = 1.0 * c[dominant] / c[k]
    w = [weights_for_class[i] for i in y]
    return w


class LightGBMWrapper(object):
    """
    Wrapper around LightGBM. This is eventually used by the ModelBuilder.
    """

    def __init__(self):
        self.gbm_model = None
        self.best_iteration = None
        self.label_id_to_lightgbm_labels = None
        self.lightgbm_labels_to_label_id = None
        self.imbalance_entropy_threshold = 0.9

    def fit(self, X, y, params, categorical_idxs='auto'):
        y = list(map(int, y))
        balance = False
        if comm_utils_data_load.entropy(y) <= self.imbalance_entropy_threshold:
            balance = True

        # there is a good chance the train_test_split would break here in the many label case (since it doesnt handle
        # cases with 1 data point only for some label). Soln: we artificially stitch these points to val and accordingly
        # create the label id mapping too.
        # pity this isnt part of scikit (maybe with a parameter in train_test_split)

        labels_to_delete = set([k for k, v in list(Counter(y).items()) if v == 1])
        idxs_to_delete = [idx for idx, label in enumerate(y) if label in labels_to_delete]
        temp_X, temp_y = X[idxs_to_delete, :], np.asarray(y)[idxs_to_delete]
        valid_X_train, valid_y_train = np.delete(X, idxs_to_delete, axis=0), np.delete(y, idxs_to_delete)

        try:
            X_train, X_val, y_train, y_val = train_test_split(valid_X_train, valid_y_train,
                                                          train_size=0.8, test_size=0.2, stratify=valid_y_train)
        except ValueError as e:
            logging.warning(f"caught exception: {str(e)}")
            return
        X_val = np.vstack((X_val, temp_X))
        y_val = y_val.tolist() + list(temp_y)

        uniq_labels = set(y_train)
        extra_labels_val = set(y_val) - uniq_labels
        num_classes = len(uniq_labels)
        self.label_id_to_lightgbm_labels = dict([(j, i) for i, j in enumerate(list(uniq_labels) +
                                                                              list(extra_labels_val))])
        w = [1.0] * len(y_train)
        if balance:
            w = get_balanced_sample_weights(y_train)
        self.lightgbm_labels_to_label_id = dict([(j, i) for i, j in list(self.label_id_to_lightgbm_labels.items())])
        lightgbm_train_data = lgbm.Dataset(X_train, [self.label_id_to_lightgbm_labels[i] for i in y_train], weight=w)
        lightgbm_val_data = lgbm.Dataset(X_val, [self.label_id_to_lightgbm_labels[i] for i in y_val])
        self.gbm_model = lgbm.train(params, lightgbm_train_data, valid_sets=[lightgbm_val_data],
                                    categorical_feature=categorical_idxs)
        self.best_iteration = self.gbm_model.best_iteration

    def predict(self, X):
        pred = self.gbm_model.predict(X) # use the best iteration
        # need to process pred, in multiclass this returns probabilities per class
        pred_labels = None
        if len(np.shape(pred)) == 1:  # 1D array, this must be the positive class probabilities in the binary class case
            pred_labels = list(map(int, np.round(pred)))
        else:
            # multiclass case
            pred_labels = np.argmax(pred, axis=1)

        y_pred = [self.lightgbm_labels_to_label_id[i] for i in pred_labels]
        return y_pred

    def predict_proba(self, X):
        """
        Returns per label probability value as a dict
        :param X:
        :return:
        """
        pred = self.gbm_model.predict(X)  # use the best iteration
        probs = []
        # need to process pred, in multiclass this returns probabilities per class
        pred_labels = None
        if len(np.shape(pred)) == 1:  # 1D array, this must be the positive class probabilities in the binary class case
            pred_labels = list(map(int, np.round(pred)))
            pos = self.lightgbm_labels_to_label_id[1]
            neg = self.lightgbm_labels_to_label_id[0]
            for p in pred:
                probs.append({pos: p, neg: 1-p})
        else:
            # multiclass case
            pred_labels = np.argmax(pred, axis=1)
            for p in pred:
                probs.append(dict([(self.lightgbm_labels_to_label_id[idx], p_val) for idx, p_val in enumerate(p)]))

        y_pred = [self.lightgbm_labels_to_label_id[i] for i in pred_labels]
        return probs


class GradientBoostingModel(ModelBuilderBase):
    """

    .. note::
                Unlike Random Forest, the complexity in terms of actual tree depths *cannot* be computed since LightGBM
                does not expose that information: see `here <https://github.com/Microsoft/LightGBM/issues/2034>`_.
                The *max_depth* itself is returned as one of the complexity dimensions (the other being number of
                boosting rounds or trees).
    """

    def __init__(self, complexity_param, *args, **kwargs):
        """
        We define a tuple as the complexity (max_depth, num_boosting_rounds). Additional keyword arguments may be
        provided. Currently supported:

        *   categorical indices: lightgbm can treat dimensions as categorical, a list of categorical indices may be
            passed in.
        *   learning_rate

        :param complexity_param: tuple  (max_depth, num_boosting_rounds)
        :param args:
        :param kwargs: the following additional keyword arguments are supported:

            *   **categorical_idxs**: LightGBM's can treat dimensions as categorical, a list of categorical indices may
                be passed in. This is its parameter
                `categorical_feature <https://lightgbm.readthedocs.io/en/latest/Parameters.html#categorical_feature>`_.
                Default: ``'auto'``.

            *   **learning_rate**: LightGBM's parameter
                `learning_rate <https://lightgbm.readthedocs.io/en/latest/Parameters.html#learning_rate>`_.
                Default: ``0.1``.

        """
        super(GradientBoostingModel, self).__init__(complexity_param)
        # if the label entropy is below this number we assume there is class imbalance and fix it
        self.max_depth, self.num_boosting_rounds = complexity_param
        self.orig_labels_to_lgbm_labels, self.lgbm_labels_to_orig_labels = None, None
        self.categorical_idxs = 'auto'
        self.learning_rate = 0.1

        if kwargs and 'categorical_idxs' in kwargs:
            self.categorical_idxs = kwargs['categorical_idxs']
        if kwargs and 'learning_rate' in kwargs:
            self.learning_rate = kwargs['learning_rate']

    def get_complexity(self, clf, *args, **kwargs):
        """
        Complexity is the **max_depth** and best boosting iteration. The actual depths per tree is not made available
        in the LightGBM API
        (see `here <https://github.com/Microsoft/LightGBM/issues/2034>`_),
        so max_depth (same as the supplied initialization) parameter is returned. "max_depth" is
        the *upper bound* on what we know about the depth complexity.

        Both properties can be acquired from the object init properties, so this function just returns them.

        :param clf: LightGBMWrapper object
        :param args:
        :param kwargs:
        :return: max_depth, num_boosting_rounds
        """
        # if we were using early_stopping we'd have needed to get clf.best_iteration
        return self.max_depth, self.num_boosting_rounds

    def get_avg_complexity(self, list_of_estimators, *args, **kwargs):
        """
        median of max_depth, boosting rounds

        :param list_of_estimators: list of LightGBMWrapper objects
        :param args:
        :param kwargs:
        :return:  median of max_depth, boosting rounds
        """

        temp = [self.get_complexity(e) for e in list_of_estimators]
        temp = np.reshape(temp, (-1, 2))
        temp = np.median(temp, axis=0)
        return int(temp[0]), int(temp[1])

    def fit_and_select_model(self, X, y, params, inside_optimizer_iteration=False, *args, **kwargs):
        """
            .. note::
                        ``num_threads`` should be set to ``1`` because of this
                        `issue <https://lightgbm.readthedocs.io/en/latest/FAQ.html#lightgbm-hangs-when-multithreading-openmp-and-using-forking-in-linux-at-the-same-time>`_.

        :param X: 2D array to perform model selection on
        :param y: corresponding labels
        :param params: model parameter search space
        :param inside_optimizer_iteration: denotes if this is call from within the optimizer iterations
        :param args:
        :param kwargs:
        :return: LightGBMWrapper object, best_parameters in params search space
        """
        uniq_train_labels = set(y)
        num_classes = len(uniq_train_labels)

        # determine the loss function based on unique labels
        data_specific_params = {'objective': 'binary' if len(uniq_train_labels) == 2 else 'multiclass',
                                'metric': 'binary_logloss' if len(uniq_train_labels) == 2 else 'multi_logloss',
                                'num_class': 1 if num_classes == 2 else num_classes
                                }

        curr_params = copy.deepcopy(params)
        curr_params.update(data_specific_params)

        if 'num_threads' in curr_params:
            curr_params['num_threads'] = 1

        lgbm_obj = LightGBMWrapper()
        best_model, best_params = None, None

        lgbm_obj.fit(X, y, curr_params, categorical_idxs=self.categorical_idxs)
        if lgbm_obj.gbm_model is None:
            best_model, best_params = None, None
        else:
            best_model, best_params = lgbm_obj, lgbm_obj.best_iteration

        return best_model, best_params

    def get_baseline_fit_params(self):
        """
        :return: dict of params, see code.
        """

        lgbm_params = {
            'boosting_type': 'gbdt',
            'max_depth': self.max_depth,
            'learning_rate': self.learning_rate,
            'num_iterations': self.num_boosting_rounds,
            'num_threads': 1,
            'verbose': -1
        }

        return lgbm_params

    def get_iteration_fit_params(self):
        """

        :return:  dict of params, see code.
        """
        lgbm_params = {
            'boosting_type': 'gbdt',
            'max_depth': self.max_depth,
            'learning_rate': self.learning_rate,
            'num_iterations': self.num_boosting_rounds,
            'num_threads': 1,
            'verbose': -1
        }

        return lgbm_params

    @staticmethod
    def get_complexity_param_range(X, y, *args, **kwargs):
        """
        We go over a range of max_depths with a fixed number of (very high) number of boosting rounds with early
        stopping. This avoids a combinatorial search of the space, since we get the "natural" number of rounds for a
        given max_depth.

        Since this leads to volatility in the number of rounds discovered i.e. the same max_depth might lead (very)
        different boosting rounds, we train with the same max_depth multiple times, and use the median number of rounds.

        *TODO: there is still some amount of volatility that needs to be revisited. Maybe we should group results that
        are close enough and pick the small complexity among the group with the highest representative accuracy?*

        :param X: 2D array to perform model selection on
        :param y: corresponding labels
        :param args:
        :param kwargs:
        :return:
        """
        categorical_idxs = 'auto'
        if kwargs and 'categorical_idxs' in kwargs:
            categorical_idxs = kwargs['categorical_idxs']

        max_num_boosting_rounds = 200
        range_max_depths = list(range(1, 31, 2))
        num_trials = 3
        results_df = pd.DataFrame(columns=['max_depth', 'num_boosting_rounds', 'trial_idx', 'score'])

        for max_depth, trial_idx in itertools.product(range_max_depths, range(num_trials)):

            # find the best # of rounds using a validation set
            train_X, test_X, train_y, test_y = train_test_split(X, y, train_size=0.8, test_size=0.2, stratify=y,
                                                                random_state=None)
            uniq_train_labels = set(train_y)
            num_classes = len(uniq_train_labels)

            logging.info(f"Trying out max_depth={max_depth}, trial_idx={trial_idx}.")

            # train and keep evaluating on validation
            metric = 'binary_logloss' if len(uniq_train_labels) == 2 else 'multi_logloss'
            params = {
                'boosting_type': 'gbdt',
                'objective': 'binary' if len(uniq_train_labels) == 2 else 'multiclass',
                'metric': metric,
                'num_class': 1 if num_classes == 2 else num_classes,
                'max_depth': max_depth,
                'learning_rate': 0.1,
                'num_iterations': max_num_boosting_rounds,
                'early_stopping_rounds': 5,
                'verbose': -1,

            }

            gbm_model = LightGBMWrapper()
            gbm_model.fit(train_X, train_y, params, categorical_idxs=categorical_idxs)
            test_y_pred = gbm_model.predict(test_X)
            score = f1_score(test_y, test_y_pred, average='macro')

            # complexities_vs_scores[(max_depth, gbm_model.best_iteration)] =
            results_df = results_df.append({'max_depth': max_depth, 'num_boosting_rounds': gbm_model.best_iteration,
                                            'trial_idx': trial_idx, 'score': score}, ignore_index=True)

        aggr_dict = {'avg_score': pd.NamedAgg('score', 'mean'),
                     'median_num_rounds': pd.NamedAgg('num_boosting_rounds', 'median')}
        aggr_results = results_df.groupby(['max_depth'], as_index=False).agg(**aggr_dict)
        h = aggr_results.iloc[aggr_results['avg_score'].idxmax()].to_dict()

        best_complexity, best_score = (int(h['max_depth']), int(h['median_num_rounds'])), h['avg_score']
        logging.info(f"Best complexity: {str(best_complexity)}")
        print(f"Best complexity: {str(best_complexity)}")

        # get all possible combination up to the depth and estimators
        res = list(itertools.product(1 + np.arange(math.ceil(best_complexity[0])),
                                     1 + np.arange(math.ceil(best_complexity[1]))))
        return res


def try_basic_functionality():
    from sklearn.datasets import load_digits
    X, y = load_digits(return_X_y=True)
    complexity_range = GradientBoostingModel.get_complexity_param_range(X, y, categorical_idxs=[0, 1])
    return complexity_range[-1]


if __name__ == "__main__":
    highest_comp = []
    for i in range(5):
        res = try_basic_functionality()
        highest_comp.append(res)
    print("\n\n" + str(highest_comp))
