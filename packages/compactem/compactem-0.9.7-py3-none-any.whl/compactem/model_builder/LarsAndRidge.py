import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns; sns.set()
from sklearn.linear_model import RidgeCV, Lars, Ridge, RidgeClassifierCV, RidgeClassifier
from compactem.utils.utils import MyLabelBinarizer
from compactem.utils import cv_utils, utils
from sklearn.metrics import f1_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.base import BaseEstimator, ClassifierMixin
import logging
logger = logging.getLogger(__name__)


class LarsAndRidgeBinary(BaseEstimator, ClassifierMixin):
    """
    Objects of this class would be used by scikits OneVsRest classifier.
    """
    def __init__(self, non_zero_terms=1, alphas=None, balance=False, fit_ridge=False):
        """
         .. warning::
            I have stopped development of the ``fit_ridge`` option. Consider it not tested and marked for deprecation.

        :param non_zero_terms:
        :param alphas: ignored when fit_ridge=False
        :param balance:
        :param fit_ridge: when we want to use LARs alone, this is faster obviously since there aren't any Ridge fits
        """
        self.non_zero_terms = non_zero_terms
        self.complexity_param = non_zero_terms
        self.alphas = alphas
        self.balance = balance
        self.fit_ridge = fit_ridge
        self.selected_feature_idxs = None
        self.orig_to_new_label_mapping = None
        self.new_label_to_orig_mapping = None
        # lars gives us a regressor hence lar_reg
        self.ridge_clf, self.lar_reg, self.clf = None, None, None
        self.model_lars_coef_, self.model_lars_intercept_ = None, None
        self.model_ridge_alpha, self.model_ridge_coef_, self.model_ridge_intercept_ = None, None, None

    def fit(self, X, y):
        # logging.info("fit() recd data shape: %s, label shape: %s, balance: %s" % (str(np.shape(X)),
        #                                                                           str(np.shape(y)),
        #                                                                str(self.balance)))
        uniq_labels = sorted(list(set(y)))
        if len(uniq_labels) != 2:
            logging.error("We dont have two labels, this class cannot handle this case!")
            return
        self.orig_to_new_label_mapping = {uniq_labels[0]: -1, uniq_labels[1]: 1}
        self.new_label_to_orig_mapping = dict([(v, k) for k, v in list(self.orig_to_new_label_mapping.items())])

        bal_X, bal_y = None, None
        if self.balance is True:
            bal_X, bal_y = cv_utils.balance_data(X, y)
        else:
            bal_X, bal_y = X, y

        # use the mapped values
        bal_y = np.asarray([self.orig_to_new_label_mapping[i] for i in bal_y])
        mapped_orig_y = np.asarray([self.orig_to_new_label_mapping[i] for i in y])

        # the data needs to be balanced only for LAR since it doesn't provide a method to provide sample weights
        reg = Lars(n_nonzero_coefs=self.non_zero_terms, fit_intercept=True, normalize=True)
        logging.info("Fitting Lars for %d non zero terms" % (self.non_zero_terms,))
        # logging.info("data shape: %s, label shape: %s, balance: %s" % (str(np.shape(bal_X)), str(np.shape(bal_y)),
        #                                                                str(self.balance)))
        reg.fit(bal_X, bal_y)
        logging.info("Done with LAR...")
        self.selected_feature_idxs = np.nonzero(reg.coef_)[0]
        self.lar_reg = reg
        self.model_lars_coef_, self.model_lars_intercept_ = reg.coef_, reg.intercept_

        if self.fit_ridge is False:
            self.clf = self.lar_reg
            return

        # fit ridge, we dont need the balanced data anymore
        if utils.is_iterable(self.alphas):
            ridge_clf = RidgeClassifierCV(alphas=self.alphas, normalize=True, fit_intercept=True, class_weight='balanced')
        else:
            ridge_clf = RidgeClassifier(alpha=self.alphas, normalize=True, fit_intercept=True, class_weight='balanced')
        ridge_clf.fit(X[:, self.selected_feature_idxs], mapped_orig_y)
        self.ridge_clf = ridge_clf
        self.clf = self.ridge_clf
        self.model_ridge_alpha, self.model_ridge_coef_, self.model_ridge_intercept_ = \
            self.alphas, ridge_clf.coef_, ridge_clf.intercept_

    def predict(self, X):
        if self.fit_ridge is False:
            # LARs would still accept the original dimensions, setting some coefficients to zero
            y_pred_reg = self.lar_reg.predict(X)
            # force to labels, this is regression after all
            y_pred = [-1 if i < 0 else 1 for i in y_pred_reg]
        else:
            # for ridge we need to provide only the selected features
            y_pred = self.clf.predict(X[:, self.selected_feature_idxs])

        # map back the labels
        y_pred = [self.new_label_to_orig_mapping[i] for i in y_pred]
        return y_pred

    def decision_function(self, X):
        """ Needed by the one-vs-rest classifier"""
        if self.fit_ridge:
            return self.ridge_clf.decision_function(X[:, self.selected_feature_idxs])
        else:
            return self.lar_reg.predict(X)

    def get_params(self, deep=True):
        return {"non_zero_terms": self.non_zero_terms, "alphas": self.alphas, "balance": self.balance,
                "fit_ridge": self.fit_ridge}

    def set_params(self, **parameters):
        for parameter, value in list(parameters.items()):
            setattr(self, parameter, value)
        return self


def test_LarsAndRidgeBinary_2class(use_ovr=False):
    """
    These are 'visual' tests. Manually look at the output.

    :param use_ovr: you can optionally do the binary test with the OVR too, just to check how the OVR works
        with binary.

    :return:
    """
    label_colors = {-1: 'r', 0: 'b', 1: 'g'}
    red_rgb, green_rgb, blue_rgb = [1.0, 0, 0], [0, 0.5, 0], [0, 0, 1.0]
    X, y = [], []

    # the two-class case
    for x in np.linspace(0, 10, 100):
        for x2 in np.linspace(0, 10, 100):
            X.append((x, x2))
            y.append(1 if x <=5 else 0)
    X, y = np.asarray(X), np.asarray(y)
    X += np.random.randn(*np.shape(X))

    if use_ovr:
        lrb_clf = LarsAndRidgeBinary(1, None, fit_ridge=False)
        clf = OneVsRestClassifier(lrb_clf)
        print('About to fit OVA-LarsAndRidgeBinary ... fit_ridge is set to', lrb_clf.fit_ridge)
        clf.fit(X, y)
    else:
        # classify using the binary classifier
        clf = LarsAndRidgeBinary(1, 0.001, balance=False, fit_ridge=False)
        print('About to fit LarsAndRidgeBinary ... fit_ridge is set to', clf.fit_ridge)
    clf.fit(X, y)
    y_pred = clf.predict(X)
    score = f1_score(y, y_pred)
    if use_ovr:
        print("Selected feature idxs:", ",".join(map(str, clf.estimators_[0].selected_feature_idxs)))
    else:
        print("Selected feature idxs:", ",".join(map(str, clf.selected_feature_idxs)))
    print("F1 on train: %0.02f" % (score,))

    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.scatter(X[:, 0], X[:, 1], c=[label_colors[label] for label in y], s=5, lw=0, alpha=0.5, marker='o')

    xv, yv = np.meshgrid(np.linspace(-2, 12, 150), np.linspace(0, 10, 150))
    plot_X = np.asarray([(i, j) for i, j in zip(xv.ravel(), yv.ravel())])
    plot_y = clf.predict(plot_X)
    decisions = clf.decision_function(plot_X)
    t1, t2 = min(decisions), max(decisions)
    color_alphas = np.asarray([1.0 * d / t2 if d>=0 else 1.0 * abs(d) / abs(t1) for d in decisions])
    ax = fig.add_subplot(122)
    rgba_cols = [tuple(green_rgb + [alpha]) if label == 1 else tuple(blue_rgb + [alpha])
                 for alpha, label in zip(color_alphas, plot_y)]
    ax.scatter(plot_X[:, 0], plot_X[:, 1], s=5, lw=0, marker='o', c=rgba_cols)
    if use_ovr:
        ax.set_title("# features=%d, F1=%0.02f" % (clf.estimators_[0].non_zero_terms, score))
    else:
        ax.set_title("# features=%d, F1=%0.02f" % (clf.non_zero_terms, score))
    plt.show()


def check_decisions_multiclass(decisons, y):
    """
    Does some basic checks on the decision values returned.

    :param decisons:
    :param y:
    :return:
    """
    uniq_labels = sorted(list(set(y)))
    correct = []
    all_neg_count = 0
    for d_tuple, label in zip(decisons, y):
        temp = np.argmax(d_tuple)
        correct.append(uniq_labels[temp] == label)
        all_neg = True
        for d in d_tuple:
            if d > 0:
                all_neg = False
        if all_neg:
            all_neg_count += 1
    if correct.count(False) > 0:
        print("Something wrong with the decisions.")
        return False
    print("Max decison values align with labels.")
    print("# decisions with all values -ve: %d (%0.02f%%)" % \
          (all_neg_count, 100.0 * all_neg_count / np.shape(decisons)[0]))
    return True


def confidence_from_scaled_decisions(scaled_decisions, strategy="top_two"):
    confidences = None
    if strategy == "top_two":
        confidences = []
        for dec in scaled_decisions:
            t = sorted(dec, reverse=True)
            confidences.append(t[0]-t[1])
    elif strategy == "max":
        confidences = np.max(scaled_decisions, axis=1)
    else:
        print("unknown strategy to compute confidences")
    return confidences


def test_LarsAndRidgeBinary_multiclass():
    """
    'visual' tests

    :return:
    """
    label_colors = {0: 'r', 1: 'b', 2: 'g'}
    red_rgb, green_rgb, blue_rgb = [1.0, 0, 0], [0, 0.5, 0], [0, 0, 1.0]
    label_rgb = {0: red_rgb, 1: blue_rgb, 2: green_rgb}

    X, y = [], []

    # the two-class case
    for x in np.linspace(0, 10, 100):
        for x2 in np.linspace(0, 10, 100):
            X.append((x, x2))
            label = 2
            if x2 < 7:
                label = 1 if x <=5 else 0
            y.append(label)
    X, y = np.asarray(X), np.asarray(y)
    X += np.random.randn(*np.shape(X))

    # classify using the binary classifier
    lrb_clf = LarsAndRidgeBinary(1, None, fit_ridge=False)
    ova = OneVsRestClassifier(lrb_clf)
    print('About to fit OVA-LarsAndRidgeBinary ... fit_ridge is set to', lrb_clf.fit_ridge)
    ova.fit(X, y)
    y_pred = ova.predict(X)
    score = f1_score(y, y_pred, average='macro')
    for i in ova.estimators_:
        print("Selected feature idxs:", ",".join(map(str, i.selected_feature_idxs)))
    print("F1 on train: %0.02f" % (score,))

    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.scatter(X[:, 0], X[:, 1], c=[label_colors[label] for label in y], s=5, lw=0, alpha=0.5, marker='o')

    xv, yv = np.meshgrid(np.linspace(-2, 12, 150), np.linspace(0, 10, 150))
    plot_X = np.asarray([(i, j) for i, j in zip(xv.ravel(), yv.ravel())])
    plot_y = ova.predict(plot_X)
    decisions = ova.decision_function(plot_X)
    check_decisions_multiclass(decisions, plot_y)
    decision_min, decision_max = np.min(decisions), np.max(decisions)
    scaled_decisions = (decisions - decision_min)/(decision_max-decision_min)
    confidences = confidence_from_scaled_decisions(scaled_decisions)
    # t1, t2 = min(decisions), max(decisions)
    # color_alphas = np.asarray([1.0 * d / t2 if d>=0 else 1.0 * abs(d) / abs(t1) for d in decisions])
    ax = fig.add_subplot(122)
    rgba_cols = [tuple(label_rgb[label] + [alpha])
                 for alpha, label in zip(confidences, plot_y)]
    ax.scatter(plot_X[:, 0], plot_X[:, 1], s=5, lw=0, marker='o', c=rgba_cols)
    num_features = [len(i.selected_feature_idxs) for i in ova.estimators_]
    uniq_num_features = list(set(num_features))
    if len(uniq_num_features) > 1:
        print("We've somehow ended up with different # of features.!!!")
    else:
        ax.set_title("# features=%d, F1=%0.02f" % (uniq_num_features[0], score))
    plt.show()


if __name__== "__main__":
    # print check_estimator(LarsAndRidgeBinary_test)
    test_LarsAndRidgeBinary_2class(True)
    # test_LarsAndRidgeBinary_multiclass()