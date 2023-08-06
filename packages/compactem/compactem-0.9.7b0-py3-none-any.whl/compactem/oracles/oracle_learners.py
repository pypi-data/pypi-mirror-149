from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from lightgbm.sklearn import LGBMClassifier
import numpy as np, math
from sklearn.metrics import f1_score


def get_calibrated_gbm(X, y, num_boosting_rounds=200, max_depth=5, learning_rate=0.1, early_stopping_rounds=3, val_pct=0.2,
                       cal_pct=0.2, calibration_method='sigmoid', random_state=None):
    """
    Create a gradient boosting model (GBM) using LightGBM. This is intended for use as an oracle model.
    Many of these parameters directly map to LightGBM parameters.

    :param X: 2D array of data to construct oracle on.
    :param y: corresponding labels.
    :param num_boosting_rounds: maximum number of boosting rounds to be used to construct the classifier.
    :param max_depth: max. depth per boosting round tree.
    :param learning_rate: learning rate fr LightGBM's gbdt implementation.
    :param early_stopping_rounds: stop model construction if validation error does not decrease for these many rounds;
        this supersedes num_boosting_rounds.
    :param val_pct: validation set size as percentage of the overall data.
    :param cal_pct: calibration set size as a percentage of the overall data.
    :param calibration_method: valid calibration_method parameter as in
        `scikit <https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibratedClassifierCV.html>`_.
    :param random_state: random seed.
    :return: calibrated GBM classifier.
    """

    num_classes = len(set(y))
    train_pct = 1.0 - (val_pct + cal_pct)
    rel_val_pct = val_pct / train_pct
    X_train_val, X_cal, y_train_val, y_cal = train_test_split(X, y, train_size=train_pct + val_pct,
                                                              test_size=cal_pct, stratify=y,
                                                              random_state=random_state)
    temp_train_size = int((1.0 - rel_val_pct) * np.shape(X_train_val)[0])
    X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, train_size=temp_train_size,
                                                      test_size=np.shape(X_train_val)[0] - temp_train_size,
                                                      stratify=y_train_val,
                                                      random_state=random_state)

    lightgbm_params = {
        'boosting_type': 'gbdt',
        'objective': 'binary' if num_classes == 2 else 'multiclass',
        'metric': 'binary_logloss' if num_classes == 2 else 'multi_logloss',
        'num_class': 1 if num_classes == 2 else num_classes,
        'max_depth': max_depth,
        'learning_rate': learning_rate,
        'num_boost_round': num_boosting_rounds,
        'early_stopping_rounds': early_stopping_rounds,
        'verbose': -1,
        'num_threads': 1
    }

    lightgbm_fit_params = {
        'eval_metric': 'binary_logloss' if num_classes == 2 else 'multi_logloss',
        'early_stopping_rounds': early_stopping_rounds,
        'verbose': -1,
        'eval_set': (X_val, y_val)
    }

    lightgbm_clf = LGBMClassifier(**lightgbm_params)
    lightgbm_clf.fit(X_train, y_train, **lightgbm_fit_params)
    calibrated_clf = CalibratedClassifierCV(base_estimator=lightgbm_clf, cv='prefit', method=calibration_method)
    calibrated_clf.fit(np.asarray(X_cal), np.asarray(y_cal))

    return calibrated_clf


def get_calibrated_rf(X, y, params_range: dict = None, base_est_params: dict = None, cv_folds=3, cal_pct=0.2,
                      calibration_method='sigmoid', random_state=None):
    """
    Creates a Random Forest oracle using scikits implementation.

    :param X: 2D array of data to construct oracle on.
    :param y: corresponding labels.
    :param params_range: model selection param range for scikit Random Forests in the format that
        `grid search <https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html>`_
        accepts. For ex., ``{'max_depth': [1, 2, 3, 4, 5], 'n_estimators': [5, 10, 50]}``.
    :param base_est_params: params to initialize the base Random Forest that would be fed into the cross-validation
        function. Should have parameters that the
        `Random Forest classifier <https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html>`_
        accepts.
    :param cv_folds: number of cross validation folds to use.
    :param cal_pct: calibration set size as a percentage of the overall data.
    :param calibration_method: valid calibration_method parameter as in
        `scikit <https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibratedClassifierCV.html>`_.
    :param random_state: random seed.
    :return: calibrated Random Forest classifier.
    """

    num_features = np.shape(X)[1]
    DEFAULT_CV_PARAMS_RANGE = {'max_features': np.linspace((math.log(num_features, 2) + 1.0) / num_features, 1.0, 5),
                               'min_samples_leaf': list(range(2, 21, 2)),
                               'n_estimators': [5] + list(range(10, 101, 10)),
                               'max_depth': list(range(1, 31, 2))}

    # DEFAULT_CV_PARAMS_RANGE = {'max_features': [0.5, 0.8, 1.0], 'min_samples_leaf': list(range(2, 21, 2)),
    #                            'n_estimators': list(range(10, 101, 10)), 'max_depth': (100,)}
    DEFAULT_BASE_ESTIMATOR_PARAMS = {'class_weight': 'balanced', 'random_state': 0, 'max_depth': 100}

    cv_params_range = params_range if params_range else DEFAULT_CV_PARAMS_RANGE
    base_est_params = base_est_params if base_est_params else DEFAULT_BASE_ESTIMATOR_PARAMS
    base_estimator = RandomForestClassifier(**base_est_params)
    X_train, X_cal, y_train, y_cal = train_test_split(X, y, train_size=1.0 - cal_pct, stratify=y,
                                                      random_state=random_state)
    cv_clf = GridSearchCV(base_estimator, cv_params_range, cv=cv_folds, refit=True, verbose=3)
    cv_clf.fit(X_train, y_train)
    calibrated_clf = CalibratedClassifierCV(base_estimator=cv_clf.best_estimator_, cv='prefit',
                                            method=calibration_method)
    calibrated_clf.fit(X_cal, y_cal)
    return calibrated_clf


if __name__ == "__main__":
    # sample use
    from sklearn.datasets import load_wine
    X, y = load_wine(return_X_y=True)
    clf = get_calibrated_gbm(X, y)
    gbm_acc = f1_score(y, clf.predict(X), average='macro')

    clf = get_calibrated_rf(X, y)
    rf_acc = f1_score(y, clf.predict(X), average='macro')

    print(f"gbm acc: {gbm_acc}")
    print(f"rf acc: {rf_acc}")
