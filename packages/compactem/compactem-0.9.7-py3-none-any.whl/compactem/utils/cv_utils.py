import re, sys, os
import numpy as np
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold


def split_integer_into_parts(total, parts):
    """
    divides a number into a given number of integer parts

    :param total:
    :param parts:
    :return:
    """
    temp = int(1.0 * total / parts)
    per_bracket = [temp] * parts
    idxs = np.random.choice(parts, total - per_bracket[0] * parts, replace=False)
    if len(idxs) > 0:
        for idx in idxs:
            per_bracket[idx] += 1
    return per_bracket


def generate_cv_indices(X, y, folds, balance=True):
    """
    scikit's grid search cv method relies on the class_weights/sample_weights param of the underlying
    classifier/regressor to handle imbalances. Unfortunately not all predictors support this param e.g. LAR
    This method generates indices that should be used in a CV in the case of class imabalance;
    the indices take care of balancing the dataset for the training data.

    :param X:
    :param y:
    :param folds:
    :param balance: if classes need to be balanced
    :return: list of tuples, size of the list = folds, each tuple has these entries (1) list representing
        the training indices (2) list of indices representing the test indices for that fold
    """
    unique_labels = list(set(y))
    skf = StratifiedKFold(n_splits=folds)
    skf.get_n_splits(X, y)
    cv_idxs = []
    for train_index, test_index in skf.split(X, y):
        y_train = y[train_index]
        new_train_index = []
        if balance:
            points_per_label = dict(list(zip(unique_labels, split_integer_into_parts(len(train_index), len(unique_labels)))))
            for label, num_points in list(points_per_label.items()):
                label_idxs = np.where(y_train == label)[0]
                sampled_idxs = np.random.choice(label_idxs, num_points, replace=True)
                new_train_index += sampled_idxs
            cv_idxs.append((new_train_index, test_index))
        else:
            cv_idxs.append((train_index, test_index))
    return cv_idxs


def get_train_and_hold_out_splits(X, y, hold_out_pct=0.2, balance=True):
    """
    This method is written to return the dataset itself since we'd be making one version of this data anyway even with
    the indices. Unlike cross-val where <folds> versions of the dataset need to be stored in memory.
    The held out set must represent the original distribution, but the training sets must be balanced to facilitate the
    learner.
    The balanced training dataset has the same size as the unbalanced training dataset

    :param X:
    :param y:
    :param hold_out_pct:
    :param balance: if classes are to be balanced
    :return:
    """
    unique_labels = list(set(y))
    X_train, X_held_out, y_train, y_held_out = train_test_split(X, y, train_size=1-hold_out_pct,
                                                                test_size=hold_out_pct, stratify=y)
    if balance is False:
        return X_train, X_held_out, y_train, y_held_out
    points_per_label = dict(list(zip(unique_labels, split_integer_into_parts(np.shape(X_train)[0], len(unique_labels)))))
    new_X_train, new_y_train = [], []
    for label, num_points in list(points_per_label.items()):
        label_idxs = np.where(y_train == label)[0]
        sampled_idxs = np.random.choice(label_idxs, num_points, replace=True)
        new_X_train.append(X_train[sampled_idxs, :])
        new_y_train += list(y_train[sampled_idxs])
    new_X_train, new_y_train = np.asarray(new_X_train), np.asarray(new_y_train)
    return new_X_train, X_held_out, new_y_train, y_held_out


def balance_data(X, y):
    """
    Returns a class balanced dataset of the same size as numpy.shape(X)[0]

    :param X:
    :param y:
    :return:
    """
    unique_labels = list(set(y))
    points_per_label = dict(list(zip(unique_labels, split_integer_into_parts(np.shape(X)[0], len(unique_labels)))))
    new_X, new_y = np.empty((0, np.shape(X)[1]), X.dtype), []
    for label, num_points in list(points_per_label.items()):
        label_idxs = np.where(y == label)[0]
        sampled_idxs = np.random.choice(label_idxs, num_points, replace=True)
        #new_X.append(X[sampled_idxs, :])
        new_X = np.vstack((new_X, X[sampled_idxs, :]))
        new_y += list(y[sampled_idxs])
    new_X, new_y = new_X, np.asarray(new_y)
    return new_X, new_y


def sample_with_conservative_replacement(X, sample_size):
    """
    Sample points from a given 2D-array X, without replacement, to have maximal variety of points in the sample.
    If sample_size <= num points in X, sample without replacement.
    If sample_size > num_points in X, *repeat* all of X as many times as possible. And sample the residual
    quantity without replacement.

    Return only the indices of the sample because this is likely going to be used as an internal routine to other
    functions and we
    want this to be fast

    :param X: 2D array of points
    :param sample_size: number of points to samples
    :return: indices of points from X that are in the sample
    """
    num_points, idxs = np.shape(X)[0], None
    if sample_size <= num_points:
        idxs = np.random.choice(num_points, sample_size, replace=False)
    else:
        # sample as much as possible from the original set without replacing
        # if the sample size k*num_points +b, then stack together the original set of points k times and THEN
        # sample the remaining b points
        repeats, rest = divmod(sample_size, num_points)
        idxs = list(range(num_points)) * repeats
        idxs = np.random.choice(num_points, rest, replace=False).tolist() + idxs
        idxs = np.asarray(idxs)
    return idxs


def stratified_conservative_sample(X, y, sample_size):
    """
    Get a stratified sample from X based on y. Create per class samples based on sample_with_conservative_replacement()
    and stack them together.

    :param X: 2D array of points
    :param y: labels, which will be used for stratification
    :param sample_size: number of points to sample
    :return: sample of points from X, corresponding labels
    """
    num_points = np.shape(X)[0]
    label_counts = Counter(y)
    label_dist = dict([(k, 1.0*v/num_points) for k, v in list(label_counts.items())])
    uniq_labels = list(label_dist.keys())
    #points_per_label = split_integer_into_parts(sample_size, len(uniq_labels))
    points_per_label = dict([(label, int(freq * sample_size)) for label, freq in list(label_dist.items())])
    # check for residuals
    rest = sample_size - sum(points_per_label.values())
    if rest > 0:
        selected_labels = np.random.choice(uniq_labels, rest, replace=False)
        for s in selected_labels:
            points_per_label[s] += 1

    sample_points, sample_labels = [], []
    for label, size in list(points_per_label.items()):
        X_curr_label = X[y == label]
        idxs = sample_with_conservative_replacement(X_curr_label, size)
        sample_points.append(X_curr_label[idxs])
        sample_labels += [label] * size
    sample_points = np.vstack(sample_points)
    return sample_points, sample_labels


def robust_train_test_split(*arrays, **options):
    """
    A robust version of train_test_split() that returns something even when some classes have one instance- a condition
    on which sklearn errors out. This is needed while exploring distributions, the objective being "stratify when you
    can, for what remains assign it to the test". All iterable arguments are expected to be in numpy array format and
    the "stratify" argument must necessarily be specified, both unlike train_test_split().

    The residual assignments are made to test since the test is typically used to calculate
    accuracy metrics and it is important to show a 0 score for these left-over labels.

    :param arrays: namesake argument wrt train_test_split()
    :param options: namesake argument wrt train_test_split()
    :return:
    """
    if 'stratify' not in options:
        raise ValueError("stratify option needs to be provided.")
    strat = np.array(options['stratify'])
    labels_low_data = [k for k, v in Counter(strat).items() if v == 1]
    if len(labels_low_data) == 0:
        return train_test_split(*arrays, **options)
    else:
        new_arrays = []
        left_out_rows = []
        for arr in arrays:
            new_arrays.append(arr[~np.isin(strat, labels_low_data)])
            left_out_rows.append(arr[np.isin(strat, labels_low_data)])

        # we are creating a copy, the original stratifier is untouched
        strat_new = strat[~np.isin(strat, labels_low_data)]
        options['stratify'] = strat_new
        result_arrays = train_test_split(*new_arrays, **options)
        for idx in range(len(result_arrays)):
            if idx % 2 == 1:
                result_arrays[idx] = np.concatenate((result_arrays[idx], left_out_rows[int((idx - 1) / 2)]))
        return result_arrays


if __name__ == "__main__":
    pass

    X = np.random.random((5, 3))
    y = np.array([1, 1, 0, 0, 1])
    print(X)
    print(y)
    print(robust_train_test_split(X, y, np.array(range(len(X))), stratify=y, train_size=0.5))