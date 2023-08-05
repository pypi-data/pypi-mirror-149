from compactem.model_builder.base_model import ModelBuilderBase
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
import itertools, sys, traceback
from collections import Counter
import numpy as np

import logging
logger = logging.getLogger(__name__)


class DecisionTree(ModelBuilderBase):
    """
    scikits decision tree is used.
    """
    def __init__(self, complexity_param, *args, **kwargs):
        """
        The complexity parameter is the *max_depth*.

        :param complexity_param: *max_depth* of the tree, scalar int
        :param args:
        :param kwargs:
        """
        super(DecisionTree, self).__init__(complexity_param)

    def get_complexity(self, estimator, *args, **kwargs):
        """
        :param estimator: decision tree object
        :param args:
        :param kwargs:
        :return: depth of tree
        """
        return estimator.get_depth()

    def get_avg_complexity(self, list_of_estimators, *args, **kwargs):
        """
        Average is defined as median depth cast to int.

        :param list_of_estimators: list of decision tree models
        :param args:
        :param kwargs:
        :return: median tree depth
        """
        return int(np.median([self.get_complexity(est) for est in list_of_estimators]))

    def fit_and_select_model(self, X, y, params, inside_optimizer_iteration=False, *args, **kwargs):
        """
        If ``inside_optimizer_iteration`` is set to ``True`` a held-out set is used for model selection in the params
        search space. This is repeated a few times per param. If ``False``, i.e., this function call occurs outside of
        the optimization step, we perform a CV-based grid search.

        :param X: 2D array to perform model selection on
        :param y: corresponding labels
        :param params: model parameter search space
        :param inside_optimizer_iteration: boolean to indicate if function is called inside optimizer
        :param args:
        :param kwargs:
        :return: best model across params search space, parameters for this model
        """
        cv_folds = 5
        X_train, y_train = X, y
        sample_weight = None
        if kwargs and 'weights' in kwargs:
            sample_weight = kwargs['weights']
        best_tree_on_all_train, best_params = None, None
        clf = DecisionTreeClassifier(random_state=0, class_weight="balanced")
        if not inside_optimizer_iteration:
            # if sample weights are provided make them part of the CV param dict so they may be passed on to the
            # fit() function of the DT
            if kwargs and "weights" in kwargs:
                params['sample_weight'] = [kwargs['weights']]
            clf = GridSearchCV(clf, params, scoring='f1_macro', cv=cv_folds, refit=True)
            clf.fit(X_train, y_train)
            best_tree_on_all_train = clf.best_estimator_
            best_params = clf.best_params_
        else:
            # there is a good chance the train_test_split would break here in the many label case
            # pity this isnt part of scikit
            validation_trials = 3
            labels_to_delete = set([k for k, v in list(Counter(y_train).items()) if v == 1])
            idxs_to_delete = [idx for idx, label in enumerate(y_train) if label in labels_to_delete]
            valid_X_train, valid_y_train = np.delete(X_train, idxs_to_delete, axis=0), np.delete(y_train,
                                                                                                 idxs_to_delete)
            if sample_weight is not None:
                valid_sample_weight_train = np.delete(sample_weight, idxs_to_delete)

            try:
                temp_train_idxs, temp_val_idxs = train_test_split(np.arange(np.shape(valid_X_train)[0]),
                                                                                  test_size=0.2,
                                                                                  train_size=0.8,
                                                                                  stratify=valid_y_train)
                temp_X_train, temp_X_val = valid_X_train[temp_train_idxs], valid_X_train[temp_val_idxs]
                temp_y_train, temp_y_val = valid_y_train[temp_train_idxs], valid_y_train[temp_val_idxs]
                if sample_weight is not None:
                    temp_sample_weight_train, temp_sample_weight_val = valid_sample_weight_train[temp_train_idxs], \
                                                                       valid_sample_weight_train[temp_val_idxs]
                else:
                    temp_sample_weight_train = None
            except ValueError:
                # likely some problem with data vs label proportions, this is acceptable as long as we return
                # reasonable values
                return None, None
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                logging.warning("Gracefully handled but here's the exception:\n" +
                                ' '.join("only_print: " + l for l in lines))
                return None, None

            best_max_depth, best_min_imp_dec, score = 0, 0, float('-inf')
            for min_imp_dec, md in itertools.product(params['min_impurity_decrease'], params['max_depth']):
                # logging.info("min_imp_dec:%0.04f" % (min_imp_dec,))
                validation_trial_scores = []
                for _ in range(validation_trials):
                    clf = DecisionTreeClassifier(random_state=0, class_weight="balanced", max_depth=md,
                                                 min_impurity_decrease=min_imp_dec)
                    clf.fit(temp_X_train, temp_y_train, sample_weight=temp_sample_weight_train)
                    validation_trial_scores.append(f1_score(temp_y_val, clf.predict(temp_X_val), average='macro'))
                current_score = np.mean(validation_trial_scores)
                if current_score > score:
                    score = current_score
                    best_max_depth = md
                    best_min_imp_dec = min_imp_dec
            logging.info("Best params on hold out: min_impurity_decrease=%0.04f, max_depth=%d" %
                    (best_min_imp_dec, best_max_depth))
            # fit on the whole dataset
            clf = DecisionTreeClassifier(random_state=0, class_weight="balanced", max_depth=best_max_depth,
                                         min_impurity_decrease=best_min_imp_dec)
            clf.fit(X_train, y_train, sample_weight=sample_weight)
            best_tree_on_all_train = clf
            best_params = {'min_impurity_decrease':best_min_imp_dec, 'max_depth': best_max_depth}

        return best_tree_on_all_train, best_params

    @staticmethod
    def get_complexity_param_range(X, y, *args, **kwargs):
        """
        Perform a grid search CV till a max depth.

        :param X: 2D array to perform model selection on
        :param y: corresponding labels
        :param args:
        :param kwargs:

        :return: list of *max_depths* from 1...max_depth discovered
        """
        folds, max_max_depth = 5, 50
        base_clf = DecisionTreeClassifier(class_weight='balanced')
        grid_clf = GridSearchCV(base_clf, {'max_depth': range(1, max_max_depth + 1, 2)},
                                scoring='f1_macro', cv=folds, verbose=10)
        grid_clf.fit(X, y)
        logging.info(grid_clf.best_score_)
        complexity_param_range = list(range(1, grid_clf.best_params_['max_depth']))
        return complexity_param_range

    def get_baseline_fit_params(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: param search space with *min_impurity_decrease* and *max_depth*
        """
        return {'min_impurity_decrease': np.linspace(0, 1.0, 5), 'max_depth': [self.complexity_param]}

    def get_iteration_fit_params(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: param search space with *min_impurity_decrease* and *max_depth*
        """
        return {'min_impurity_decrease': np.linspace(0, 1.0, 5), 'max_depth': [self.complexity_param]}


if __name__ == "__main__":
    from sklearn.datasets import load_iris
    print(DecisionTree.get_complexity_param_range(*load_iris(return_X_y=True)))