from compactem.model_builder.base_model import ModelBuilderBase
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score
import numpy as np, math, itertools
from copy import deepcopy
import logging
logger = logging.getLogger(__name__)


def calculate_RandomForest_complexity(estimator):
    """
    We calculate the complexity of a Random Forest as the (median of tree depths, number of trees).
    This logic doesn't depend on the dataset, and defining at the module level means we can reuse it at
    different places.

    :param estimator: scikit's RandomForestClassifier object
    :return: median depth (can be float), number of trees
    """
    trees = estimator.estimators_
    # median can return float (when we have even # of entries) but that is OK here since scikit allows max_depth to
    # be float
    median_depth = np.median([t.get_depth() for t in trees])
    n_estimators = len(trees)

    return median_depth, n_estimators


class RandomForest(ModelBuilderBase):

    def __init__(self, complexity_param, *args, **kwargs):
        """
        We define a tuple as the complexity (max_depth, n_estimators)

        :param complexity_param: tuple (max_depth, n_estimators)
        """
        super(RandomForest, self).__init__(complexity_param)

    def get_complexity(self, estimator, *args, **kwargs):
        """

        :param estimator: scikit's RandomForestClassifier object
        :param args:
        :param kwargs:
        :return: median depth (can be float), number of trees
        """

        return calculate_RandomForest_complexity(estimator)

    def get_avg_complexity(self, list_of_estimators, *args, **kwargs):
        """
        We compute the median per complexity dimension separately.

        :param list_of_estimators: list of scikit's RandomForestClassifier objects
        :return: median of the complexities i.e. median of Random Forest depths, and number of trees, as calculated by
            ``get_complexity()``
        """
        temp = [self.get_complexity(e) for e in list_of_estimators]
        temp = np.reshape(temp, (-1, 2))

        # num trees has to be an integer , scikit throws an error when you call fit() on a RF with
        # non-integer n_estimators
        return np.median(temp[:, 0]), int(np.median(temp[:, 1]))

    def fit_and_select_model(self, X, y, params, inside_optimizer_iteration=False, *args, **kwargs):
        """
        Only CV is performed, and based on whether the fit is inside the optimizer or outside it, we change the
        number of folds. Also note: in addition to the params passed in, this adds an additional search space
        dimension *"max_features"*: this is done here since we use Breiman's
        `suggestion <https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf>`_ as a lower bound,
        :math:`\\log_2(\\text{num_features}) + 1`
        which is data dependent. It is determined here based on the input X.

        :param X: 2D array to perform model selection on
        :param y: corresponding labels
        :param params: model parameter search space
        :param inside_optimizer_iteration: denotes if this is call from within the optimizer iterations
        :return: scikit's RandomForestClassifier object, best_parameters in params search space
        """

        # We perform the CV over one param: num features
        cv_folds = 3 if inside_optimizer_iteration else 5
        num_features = np.shape(X)[1]
        params['max_features'] = np.linspace((math.log(num_features, 2) + 1.0) / num_features, 1.0, 5)
        base_estimator_params = {'class_weight': 'balanced', 'random_state': 0}
        base_estimator = RandomForestClassifier(base_estimator_params)
        clf_grid = GridSearchCV(base_estimator, params, cv=cv_folds, refit=True)
        try:
            clf_grid.fit(X, y)
            best_model = clf_grid.best_estimator_
            best_params = clf_grid.best_params_
        except:
            best_model, best_params = None, None
        return best_model, best_params

    def get_baseline_fit_params(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: search space has exactly one value of max_depth and n_estimators - the complexity param defined for
            this object
        """
        return {'max_depth': [self.complexity_param[0]],
                'n_estimators': [self.complexity_param[1]]}

    def get_iteration_fit_params(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: search space has exactly one value of max_depth and n_estimators - the complexity param defined for
            this object
        """
        return {'max_depth': [self.complexity_param[0]],
                'n_estimators': [self.complexity_param[1]]}

    @staticmethod
    def get_complexity_param_range(X, y, hold_fixed=None, *args, **kwargs):
        """
        Provides the complexity range for a RF in terms of max_depth and n_estimators. For experiments, where both
        parameters don't need to change, one may specify the parameter to hold constant, and what value.

        :param X: 2D array to perform model selection on
        :param y: corresponding labels
        :param hold_fixed: dict to specify which parameter to hold fixed. For ex, if we want to hold max_depth at 5,
                this argument should be {'max_depth': 5}
        :param args:
        :param kwargs:
        :return:
        """
        cv_folds = 5
        # for max features we use breiman's suggestion of 1+logM features as the lower bound,
        # see https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf
        num_features = np.shape(X)[1]
        cv_params_range = {'max_features': np.linspace((math.log(num_features, 2) + 1.0) / num_features, 1.0, 5),
                           'min_samples_leaf': list(range(2, 21, 2)),
                           'n_estimators': [5] + list(range(10, 101, 10)),
                           'max_depth': list(range(1, 31, 2))}

        if hold_fixed:
            if "n_estimators" not in hold_fixed and 'max_depth' not in hold_fixed:
                notif_msg = "hold_fixed must be a dict with entries n_estimators or max_depth or both."
                logging.error(notif_msg)
                raise ValueError(notif_msg)
            if "n_estimators" in hold_fixed:
                cv_params_range["n_estimators"] = [hold_fixed["n_estimators"]]
            if "max_depth" in hold_fixed:
                cv_params_range["max_depth"] = [hold_fixed["max_depth"]]

        base_estimator_params = {'class_weight': 'balanced', 'random_state': 0}
        base_estimator = RandomForest(base_estimator_params)
        clf_grid = GridSearchCV(base_estimator, cv_params_range, cv=cv_folds, refit=True)
        clf_grid.fit(X, y)
        median_depth, n_estimators = calculate_RandomForest_complexity(clf_grid.best_estimator_)

        # get all possible combination up to the depth and estimators
        res = list(itertools.product(1+np.arange(math.ceil(median_depth)), 1+np.arange(math.ceil(n_estimators))))
        return res