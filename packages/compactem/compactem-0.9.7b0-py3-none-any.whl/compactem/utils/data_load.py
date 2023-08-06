from collections import Counter, defaultdict
import numpy as np
import math
from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import train_test_split


def entropy(labels, full_label_set=None):
    label_counts = list(Counter(labels).values())
    if full_label_set:
        missing_labels = set(full_label_set) - set(labels)
        for missing_label in missing_labels:
            label_counts.append(0)
    p = 1.0*np.asarray(label_counts)/sum(label_counts)
    try:
        ent = sum([0 if i == 0 else -1.0*i*math.log(i, len(p)) for i in p])
    except:
        print("probably need to use the 'full_label_set' param of this function.")
        print(p, full_label_set)
    return ent


def load_data(*args):
    """
    stub
    """

    datafile = r'data/letter.scale.txt'
    data = load_svmlight_file(datafile)
    X, y = data[0].toarray(), np.asarray(data[1], dtype=int)

    # use only 10000 points
    X, _, y, _ = train_test_split(X, y, train_size=12000, stratify=y)
    return X, y