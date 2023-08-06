"""
Helper functions to process scikit decision trees.
"""
import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict, Counter
import math
from sklearn.preprocessing import LabelBinarizer

is_iterable = lambda obj: hasattr(obj,'__iter__') or hasattr(obj,'__getitem__')


def get_label_colormap(labels):
    """
    Get a colormap dict for labels.

    :param labels:
    :return: dict with key = label and value as color name. None if there are more labels than can be supported.
    """
    colors = ['r', 'g', 'teal' 'darkmagenta', 'darkorange', 'gold', 'sienna', 'orchid', 'slategray']
    s = set(labels)
    num_uniq_labels = len(s)
    if num_uniq_labels > len(colors):
        return None
    else:
        return dict(list(zip(sorted(s), colors)))


def get_label_colors(y, label_colormap):
    """
    Get colors corresponding to labels

    :param y: labels
    :param label_colormap: obtained from get_label_colormap()
    :return: list of colors, length of list is the same as y
    """
    label_colors = [label_colormap[i] for i in y]
    return label_colors


def pick_best_k(values, k):
    """
    This is a quick way to select a bunch of parameters that are "close" together on the real line.
    The idea is if we have a one-vs-all classifier and each of the classifiers returns a parameter space, then
    deciding on a global param space across all classes can be difficult.

    One soln: if we need p params and we have c classes, then get p params per class - for a total of pc params - then
    perform a k-means with k=p.

    :param values:
    :param k:
    :return:
    """
    kmeans = KMeans(n_clusters=k).fit(np.asarray(values).reshape(-1, 1))
    selected_values = list(kmeans.cluster_centers_.ravel())
    return selected_values


class MyLabelBinarizer(object):
    """
    This is different from the original LabelBinarizer in how it handles the 2 class case.
    We don't want to return a vector of one dimensional labels in this case, we flatten it.
    """
    def __init__(self):
        self.lb = LabelBinarizer()
        self.classes_ = None

    def fit(self, y):
        self.lb.fit(y)
        self.classes_ = self.lb.classes_

    def transform(self, y):
        temp = self.lb.transform(y)
        if len(self.classes_) == 2:
            return temp.flatten()
        else:
            return temp

    def inverse_transform(self, Y):
        if len(self.classes_) == 2:
            return self.lb.inverse_transform(np.reshape(Y, (-1, 1)))
        else:
            return self.lb.inverse_transform(Y)


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def entropy(labels):
    label_counts = list(Counter(labels).values())
    if len(label_counts) == 1:
        return 0.0
    p = 1.0*np.asarray(label_counts)/sum(label_counts)
    ent = sum([0 if i == 0 else -1.0*i*math.log(i, len(p)) for i in p])
    return ent
