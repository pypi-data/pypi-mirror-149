import sys, os
from compactem.model_builder.base_model import ModelBuilderBase
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV, train_test_split
import numpy as np
from sklearn.datasets import make_classification
import logging
logger = logging.getLogger(__name__)
from compactem.model_builder.LarsAndRidge import LarsAndRidgeBinary
from sklearn.multiclass import OneVsRestClassifier
from compactem.utils import data_load


class LinearProbabilityModel(ModelBuilderBase):
    """
    Wrapper methods for building a Linear Probability Model (LPM) - since it has some
    `advantages over logistic regression <See http://jakewestfall.org/misc/mood2010.pdf>`_ in terms of interpretability.
    General idea:

    *   select given number of features using LARS
    *   fit on features using Ridge (note: Ridge might be deprecated)
    """
    def __init__(self, complexity_param, *args, **kwargs):
        """
        The complexity param here is the number of terms with non-zero coefficients in a LPM; if the dataset has n
        classes, a one-vs-all estimator is constructed, and the complexity param applies to *each* component classifier.

        :param complexity_param: number of terms with non-zero coefficients
        :param args:
        :param kwargs:
        """
        super(LinearProbabilityModel, self).__init__(complexity_param)
        # if the label entropy is below this number we assume there is class imbalance and fix it
        self.imbalance_entropy_threshold = 0.9
        self.ova_clf = None

    def get_complexity(self, ova_estimator, *args, **kwargs):
        """
        :param ova_estimator: one-vs-all LPM classifier
        :param args:
        :param kwargs:
        :return: complexity of ova estimator - this is computed as the number of non-zero coefficients per LPM in the
            one-vs-all classifier, and raises ValueError if this number is not identical across them
        """
        # scikits one-vs-all classifier
        # switches over to _ConstantPredictor objects for estimators whenever all labels are identical
        non_zero_terms = [i.non_zero_terms if hasattr(i, 'non_zero_terms') else 0 for i in ova_estimator.estimators_]
        if len(set(non_zero_terms)) != 1:
            notif_msg = "The ova estimators have more than value for non_zero_terms!"
            logging.error(notif_msg)
            raise ValueError(notif_msg)
        return non_zero_terms[0]

    def get_avg_complexity(self, list_of_estimators, *args, **kwargs):
        """
        Calculate "average" complexity across a bunch of ova LPMs: here the "average" is essentially a check that all
        ova LPMs have the same complexity: if not, this is an error.

        :param list_of_estimators: list of ova LPMs
        :param args:
        :param kwargs:
        :return: # non-zero coefficients in the ova LPMs if they are identical, else raise error
        """
        est_complexities = [self.get_complexity(est) for est in list_of_estimators]
        if len(set(est_complexities)) != 1:
            notif_msg = "The list of estimators has more than value for non zero terms!: %s" % (str(est_complexities))
            logging.error(notif_msg)
            raise ValueError(notif_msg)
        return np.median(est_complexities)

    def fit_and_select_model(self, X, y, params, inside_optimizer_iteration=False, *args, **kwargs):
        """
        No parameter search here since the complexity param and complexity are both number of terms with non-zero
        coefficients, and is expected that the complexity passed in <= the unbounded complexity found via CV.

        :param X: 2D array to perform model selection on
        :param y: corresponding labels
        :param params: model parameter search space
        :param inside_optimizer_iteration: boolean to indicate if function is called inside optimizer
        :return: best model across params search space, parameters for this model
        :param args:
        :param kwargs:
        :return:
        """
        X_train, y_train = X, y
        best_model, best_params = None, None
        balance = False
        if data_load.entropy(y_train, full_label_set=set(self.y_train)) <= self.imbalance_entropy_threshold:
            balance = True
        lrb_clf = LarsAndRidgeBinary(self.complexity_param, params['alphas'], balance=balance, fit_ridge=False)
        ova = OneVsRestClassifier(lrb_clf)
        if len(set(y_train)) == 1:
            logging.warning("Only got points for one label (%s) in LPM fit! Total train data size: %d" % (str(y_train[0]),
                                                                                                    len(y_train)))
        ova.fit(X_train, y_train)
        # score = f1_score(y_test, ova.predict(X_test), average='macro')
        # we explicitly check for the "ridge_clf" attribute since scikits one-vs-rest classifier
        # switches over to _ConstantPredictor objects for estimators whenever all labels are identical
        best_model, best_params = ova, [i.ridge_clf.alpha_ if hasattr(i, 'ridge_clf') and i.ridge_clf else None
                                                    for i in ova.estimators_]
        return best_model, best_params

    def get_baseline_fit_params(self, *args, **kwargs):
        """
        Returns a search space for the ridge regression; doesn't affect number of terms with non-zero coefficients.
        *NOTE: support for ridge might be deprecated soon.*

        :param args:
        :param kwargs:
        :return:
        """
        return {'alphas': np.logspace(-3, 2, 6)}

    def get_iteration_fit_params(self, *args, **kwargs):
        """
        Returns a search space for the ridge regression; doesn't affect number of terms with non-zero coefficients.
        *NOTE: support for ridge might be deprecated soon.*

        :param args:
        :param kwargs:
        :return:
        """

        return {'alphas': np.logspace(-3, 2, 6)}

    @staticmethod
    def get_complexity_param_range(X, y, *args, **kwargs):
        """
        Grid search via CV is performed to find the best number of non-zero coefficients in the
        range 1...np.shape(X)[1].

        :param X: 2D array to perform model selection on
        :param y: corresponding labels
        :param args:
        :param kwargs:
        :return: list of non-zero coefficients from 1 up to whatever grid search discovered
        """
        max_terms = np.shape(X)[1]
        folds =5
        balance = False
        if data_load.entropy(y, full_label_set=set(y)) <= 0.9:
            balance = True
        lrb_clf = LarsAndRidgeBinary(non_zero_terms=1, alphas=None,
                                     balance=balance, fit_ridge=False)
        ova = OneVsRestClassifier(lrb_clf)
        grid_clf = GridSearchCV(ova, {'estimator__non_zero_terms': range(1, max_terms + 1)},
                                scoring='f1_macro', cv=folds, verbose=10)
        logging.info("About to perform grid search.")
        grid_clf.fit(X, y)
        logging.info(grid_clf.best_score_)
        complexity_param_range = list(range(1, grid_clf.best_params_['estimator__non_zero_terms']))
        return complexity_param_range


if __name__ == "__main__":
    # usage/tests
    from sklearn.datasets import load_digits
    print(LinearProbabilityModel.get_complexity_param_range(*load_digits(return_X_y=True)))