import logging, numpy as np
from typing import NamedTuple, Iterable, Union
import numbers
from collections import Counter
logger = logging.getLogger(__name__)
from compactem.utils.utils import is_iterable
from typing import Iterable, Union, Dict, Optional

# This might be replaced with a DataClass, but that was introduced only in Python 3.7, and I plan to support 3.6.
# Not using NamedTuple here because I need __init__


class DataInfo:
    def __init__(self, dataset_name, data, complexity_params, evals, splits=None, additional_info: Optional[Dict]=None):
        """

        :param dataset_name: this name is used to create result files, associate with results returned etc
        :param data: (X, y), tuple with 2D array of features vectors and labels. This *can be None* if the **splits**
            parameter contains data splits.
        :param complexity_params: list of complexity params for which a model must be built using this dataset.
        :param evals: number of optimizer iterations
        :param splits: dict with keys 'train', 'val' and 'test', and the values being either percentages of these
            splits, or tuples with the actual data splits,
            e.g., ``{'test': (X_t, y_t), 'train': (X_tr, y_tr), 'val': (X_val, y_val)}``. If data splits are provided,
            explicitly set the **data** parameter to ``None``, since that gets precedence.
        :param additional_info: additional info that is transparently passed on to the Model builder init. This must be
            a dict.
        """

        if dataset_name is None or len(dataset_name) == 0:
            logging.error("dataset_name must be a string of non-zero length.")
            raise Exception('dataset_name is None or has zero-length!')

        self.dataset_name: str = dataset_name
        self.data: tuple = data
        self.splits: dict = splits
        # these is the size restriction that would be applied to training
        self.complexity_params: Iterable = complexity_params
        # this should be a list of params - note that we cannot catch the other type of error where the size param
        # is meant to be a vector, but user passes in one instance of it; it would clear the is_iterable() test
        if complexity_params is None or not is_iterable(complexity_params):
            self.complexity_params = [self.complexity_params]

        # the number of iterations to run the optimizer for
        self.evals: int = evals

        if self.splits is None:
            # assign a default value for the splits
            self.splits = {'train': 0.6, 'val': 0.2, 'test': 0.2}

        self.additional_info = additional_info


class UncertaintyInfo:
    def __init__(self, oracle_accuracy, uncertainty_scores, oracle_name=None):
        """

        :param oracle_accuracy: a representative accuracy score for the oracle, this is for display/result collation
            purposes, but is recommended to have for creating helpful analysis.
        :param uncertainty_scores: uncertainty scores for a dataset; list of scalar values in [0, 1].
        :param oracle_name: a name for  display/result collation purposes.
        """
        if oracle_accuracy is None or not isinstance(oracle_accuracy, numbers.Number):
            logging.error("oracle_accuracy must be number!")
            raise ValueError('oracle_accuracy must be number!')

        temp = np.array(uncertainty_scores)
        if not np.all([isinstance(u, numbers.Number) for u in uncertainty_scores]) or \
                not np.all(0 <= temp) or not np.all(temp <= 1):
            logging.error("uncertainty_scores must be numbers in [0,1]!")
            raise ValueError('uncertainty_scores must be numbers in [0,1]!')

        self.oracle_name = oracle_name
        self.oracle_accuracy = oracle_accuracy
        self.uncertainty_scores = uncertainty_scores


def validate_dataset_info(datasets_info: Iterable[DataInfo]) -> bool:
    """
    Check if the dataset info supplied by user is in the correct format.
    Since this is user-facing, we want to validate this closely and notify early rather than downstream.
    TODO: it might make sense to move some of the checks here to the DataInfo class

    :param datasets_info: list of :any:`compactem.utils.data_format.DataInfo` objects.
    :return: True or False, indicating if the datasets passed in clear certain checks.
    """

    dataset_names = [i.dataset_name for i in datasets_info]
    repeated_names = [k for k, v in list(Counter(dataset_names).items()) if v > 1]
    if len(repeated_names) > 0:
        logging.error("Datasets must have unique names, these names repeat: %s" % (",".join(repeated_names)))
        return False

    eval_types = set([type(i.evals) for i in datasets_info])
    if len(eval_types) > 1 or eval_types.pop() != int:
        logging.error("evals can only be integers.")
        return False

    splits_types = set([type(i.splits) for i in datasets_info])
    if len(splits_types) > 1 or splits_types.pop() != dict:
        logging.error("splits_types can only be dict.")
        return False

    expected_keys = {'train', 'test', 'val'}
    for idx, d in enumerate(datasets_info):

        if d.data:
            X, y = d.data[0], d.data[1]
            if np.shape(X)[0] != np.shape(y)[0]:
                logging.error("Rows must match in data field, this is not true for info idx=%d" % (idx,))
                return False
            if len(np.shape(y)) != 1:
                logging.error("y can have exactly 1 column, this is not true for info idx=%d"% (idx,))

        if expected_keys != set(d.splits.keys()):
            logging.error("splits for info idx=%d doesn't have correct keys." % (idx,))
            return False

        values = list(d.splits.values())
        val_types = set([type(v) for v in values])
        if len(val_types) > 1:
            logging.error("All split values should have same type, tuple or float, problem with info idx=%d" % (idx,))
            return False
        common_val_type = val_types.pop()
        if is_iterable(common_val_type):
            # check tuple sizes
            tuple_sizes = set([len(v) for v in values])
            if len(tuple_sizes) > 1 or list(tuple_sizes)[0] != 2:
                logging.error("All split values must have the same iterable size=2 containing <X, y>, "
                              "problem with info at idx=%d" % (idx,))
                return False

            # if actual data splits are provided the data field must be None
            if d.data is not None:
                logging.error("If splits has actual data subsets, the data field must be None, which is not the case "
                              "with info idx=%d" % (idx,))
                return False

            # rows in each tuple entry must match
            for k in expected_keys:
                X, y = d.splits[k]
                if np.shape(X)[0] != np.shape(y)[0]:
                    logging.error("Rows must match in splits subsets, this is not true for %s in info idx=%d"
                                  % (k, idx))
                    return False
                if len(np.shape(y)) != 1:
                    logging.error("y can have exactly 1 column, this is not true for %s in info idx=%d"
                                  % (k, idx))
                    return False

        elif common_val_type == float:
            if sum(values) != 1:
                logging.error("Split fractions must sum to 1, not true for info at idx=%d" % (idx,))
                return False
        else:
            logging.error("Invalid value type for splits at info at idx=%d" % (idx,))
            return False

    return True
