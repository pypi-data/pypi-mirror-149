from abc import ABCMeta, abstractmethod
from compactem.utils import utils
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
import pickle, sys
import logging
logger = logging.getLogger(__name__)


class ModelBuilderBase(metaclass=ABCMeta):

    """ Pythons' enforcement of abstract class is weak in the sense that deriving classes don't need to match
    the function signature. The signature provided herein should be used as "documentation" if
    you don't want stuff to break.

    Guiding principles:

    *   abstract methods to be implemented in subclass.
    *   methods that mention "**Do not override in subclass.**" in their doc string typically shouldn't be overriden,
        unless you want to change some fundamental behavior.
    *   all else is optional and whether to implement should be decided based on the doc string.

    """

    def __init__(self, complexity_param, *args, **kwargs):
        """
        The complexity parameter is fixed for an object of this class. In other words, an object of this class can build
        models only for a fixed complexity, controlled by the complexity_param.

        :param complexity_param: the param that decides the complexity of the model to be learned.

        """
        self.complexity_param = complexity_param

    @abstractmethod
    def get_complexity(self, estimator, *args, **kwargs):
        """
        Get the complexity of the model passed in.

        :param estimator: model whose complexity is to be computed
        :return: complexity value
        """
        complexity = None
        return complexity

    @abstractmethod
    def get_avg_complexity(self, list_of_estimators, *args, **kwargs):
        """
        Define how would you calculate the average complexity of estimators. For ex in the case of decision trees
        this could be the median decision tree depth.

        :param list_of_estimators:
        :return: average of the complexities of the estimators
        """

    @abstractmethod
    def fit_and_select_model(self, X, y, params, inside_optimizer_iteration=False, *args, **kwargs):
        """
        This is the key model training function: it implements how a model is trained on a dataset, given a parameter
        range to search. Other functions in this class rely on this method.

        :param X: 2D array to perform model selection on
        :param y: labels
        :param params: param range to search - no fixed format, since subclass decides how "params" is produced by
            other functions like ``get_baseline_fit_params()``, which also subclass implements. Must be consistent.
        :param inside_optimizer_iteration: denotes if this is call from within the optimizer iterations -
                it might make sense to define the function based on the location of call
        :return: best_model (must support ``predict()``), best_params

        .. attention::
            Remember to handle cases when the data passed in might not be "proper", e.g. sample has only points of one
            label. This might happen when the optimizer is exploring the search space. Handle such cases by returning
            an accuracy of 0, so that the optimizer learns to avoid them.

        """
        best_model, best_params = None, None
        return best_model, best_params

    @abstractmethod
    def get_baseline_fit_params(self, *args, **kwargs):
        """
        This function should return a range of parameters, across which a model is to be selected as the baseline
        model. The format for this range is up to the user since it would be handled by ``fit_and_evaluate_on_data()``
        which also needs to be implemented in the sub-class.

        :return: parameter range across which the best baseline model is to be picked
        """
        pass

    @abstractmethod
    def get_iteration_fit_params(self, *args, **kwargs):
        """
        This function should return the range of parameters, across which a model is to be selected within an optimizer
        iteration. Ideally, this should be cheap to compute since this is within an iteration. The format for this
        range is up to the user since it would be handled by ``fit_and_evaluate_on_data()`` which also needs to be
        implemented in the sub-class.

        :return: parameter range across which the best model within an optimizer iteration is to be picked
        """
        pass

    #######################################################
    # The following methods may be optionally implemented.
    #######################################################

    @staticmethod
    def get_complexity_param_range(X, y, *args, **kwargs):
        """
        An implementation should return the range of sizes, as an iterable, that models need to be built for. This is
        helpful only if user wants this range to be derived based on some data (X, y), e.g., if they want to build
        models with complexity lesser than what natural optimal complexity of the model found via
        cross-validation. This is grouped here to keep things related to model building in one place.

        This is not an object method because this provides sizes/complexities, that would be required to instantiate an
        object with.
        This is intended to be a convenience method, and optional to implement.

        :param X: 2D array of data based on which parameter range must be determined
        :param y: corresponding labels
        :return: parameter range
        """
        raise NotImplementedError

    @staticmethod
    def save_model(model, file_path_no_ext, *args, **kwargs):
        """
        If this is not implemented by a subclass, an attempt would be made to save model with pickle.
        This is not an object function, and is grouped here to keep all things related to model building at one place.

        :param model: model object to save
        :param file_path_no_ext: the path where the model is to be saved, without the extension. The final path must
            returned to add to the result files. If a subclass implements this, its good practice to add an extension
            for usability.
        :return: path where file is saved
        """
        try:
            file_path = file_path_no_ext + ".pckl"
            with open(file_path, 'wb') as fw:
                pickle.dump(model, fw)
        except:
            print("Unexpected error while trying to save model:", sys.exc_info()[0])
            raise

        return file_path

    #######################################################
    # The following methods need not be implemented.
    #######################################################

    def load_data_splits(self, X_train, y_train, X_train_val, y_train_val, X_val, y_val, X_test, y_test):
        """
        **Do not override in subclass.**

        The data splits are assigned in one place so that the overhead due to passing in different function
        calls are avoided.

        :param X_train: 2D array denoting train data
        :param y_train: corresponding train labels
        :param X_train_val: 2D array denoting train+val data
        :param y_train_val: corresponding train+val labels
        :param X_val: 2D array denoting val data
        :param y_val: corresponding val labels
        :param X_test: 2D array denoting test data
        :param y_test: corresponding test labels
        :return: None
        """
        self.X_train = X_train
        self.y_train = y_train
        self.X_train_val = X_train_val
        self.y_train_val = y_train_val
        self.X_val = X_val
        self.y_val = y_val
        self.X_test = X_test
        self.y_test = y_test

    def data_split_resolver(self, dataset_identifier):
        """
        **Do not override in subclass.**

        A convenience function that allow referring to splits by name. A helper function to
        ``__resolve_datasets_for_fit_and_eval__()``. If a tuple (X, y) of data is passed, this transparently returns it
        with no processing.

        :param dataset_identifier: can be a string ('train', 'val', 'train_val', 'test') or a tuple
        :return: data X, y
        """
        if type(dataset_identifier) == str:
            if dataset_identifier.lower() == 'train':
                return self.X_train, self.y_train

            if dataset_identifier.lower() == 'train_val':
                return self.X_train_val, self.y_train_val

            if dataset_identifier.lower() == 'test':
                return self.X_test, self.y_test

            if dataset_identifier.lower() == 'val':
                return self.X_val, self.y_val
        elif utils.is_iterable(dataset_identifier) and len(dataset_identifier) == 2:
            return dataset_identifier
        else:
            return None

    def __resolve_datasets_for_fit_and_eval__(self, fit_on, eval_on):
        """
        **Do not override in subclass.**

        Convenience function that resolves dataset arguments.

        :param fit_on: data to train on, can be a string ('train', 'val', 'train_val', 'test') or a tuple
        :param eval_on: validation data, can be a string ('train', 'val', 'train_val', 'test') or a tuple
        :return: resolved datasets: train data as a 2D array, its corresponding labels, validation data as a 2D array,
            its correspnding labels
        """
        temp1 = self.data_split_resolver(fit_on)
        temp2 = self.data_split_resolver(eval_on)
        if temp1 is None or temp2 is None:
            logging.error("Couldn't resolve datasets!")
            return

        fit_X, fit_y = temp1
        eval_X, eval_y = temp2
        return fit_X, fit_y, eval_X, eval_y

    def fit_baseline_model(self, all_baselines=False, num_train_points=None):
        """
        **Do not override in subclass.**

        Fit the baseline model on different splits.
        Reuse fit_and_evaluate() here.

        :param all_baselines: do we need all combinations of baseline models? Probably not, for practical use.
            Combinations here mean train on train and report score on train, train on train report on validation etc.
            This option was used initially for research.
        :param num_train_points: number of points to use from the training split
        :return: return various scores and models (consult source)
        """
        baseline_fit_params = self.get_baseline_fit_params()

        logging.info("Fitting on train_val, evaluating on test.")
        test_score_based_on_train_val, best_test_model_based_on_train_val, best_test_model_params_based_on_train_val = \
            self.fit_and_evaluate('train_val', 'test', baseline_fit_params, inside_optimizer_iteration=False,
                                  num_train_points=num_train_points)

        test_score_based_on_train, best_test_model_based_on_train, best_test_model_params_based_on_train = \
            None, None, None
        train_score_based_on_train, best_train_model_based_on_train, best_train_model_params_based_on_train = \
            None, None, None
        val_score_based_on_train, best_val_model_based_on_train, best_val_model_params_based_on_train = \
            None, None, None

        if all_baselines:
            logging.info("Fitting on train, evaluating on test.")
            test_score_based_on_train, best_test_model_based_on_train, best_test_model_params_based_on_train = \
                self.fit_and_evaluate('train', 'test', baseline_fit_params, inside_optimizer_iteration=False,
                                      num_train_points=num_train_points)

            logging.info("Fitting on train, evaluating on train.")
            train_score_based_on_train, best_train_model_based_on_train, best_train_model_params_based_on_train = \
                self.fit_and_evaluate('train', 'train', baseline_fit_params, inside_optimizer_iteration=False,
                                      num_train_points=num_train_points)

            logging.info("Fitting on train, evaluating on val.")
            val_score_based_on_train, best_val_model_based_on_train, best_val_model_params_based_on_train = \
                self.fit_and_evaluate('train', 'val', baseline_fit_params, inside_optimizer_iteration=False,
                                      num_train_points=num_train_points)

        return train_score_based_on_train, best_train_model_based_on_train, \
            val_score_based_on_train, best_val_model_based_on_train, \
            test_score_based_on_train, best_test_model_based_on_train, \
            test_score_based_on_train_val, best_test_model_based_on_train_val

    def fit_model_within_iteration(self, X, y, **kwargs):
        """
        **Do not override in subclass.**

        This fit method is invoked within the optimization loop.
        We reuse fit_and_evaluate() here.


        :param X: data generated with current density params
        :param y: labels for X
        :param **kwargs: any other params to be passed on to fit_and_evaluate
        :return: scores on train, val and test; and the model fit on train.
        """
        iteration_fit_params = self.get_iteration_fit_params()
        train_trial_score, best_model, best_params = self.fit_and_evaluate((X, y), 'train', iteration_fit_params,
                                                                           inside_optimizer_iteration=True, **kwargs)
        if best_model is not None:
            val_trial_score = f1_score(self.y_val, best_model.predict(self.X_val), average='macro')
            test_trial_score = f1_score(self.y_test, best_model.predict(self.X_test), average='macro')
        else:
            val_trial_score, test_trial_score  = 0, 0
        return train_trial_score, val_trial_score, test_trial_score, best_model, best_params

    def fit_and_evaluate(self, fit_on, eval_on, params, inside_optimizer_iteration=False, num_train_points=None,
                         **kwargs):
        """
        **Do not override in subclass.**

        This is a wrapper around ``fit_and_evaluate_on_data()`` which subclass must implement.


        :param fit_on: data to train on, can be a string ('train', 'val', 'train_val', 'test') or a tuple
        :param eval_on: validation data, can be a string ('train', 'val', 'train_val', 'test') or a tuple
        :param params: parameters for model selection
        :param inside_optimizer_iteration: denotes if this is call from within the optimizer iterations -
                it might make sense to define the function based on the location of call
        :param num_train_points: number of training points (stratified) to use from ``fit_on``. If ``None`` use all
            points.
        :return: score on validation data, best model learned on ``fit_on`` data, best paramters from ``params``
        """
        X_train, y_train, X_test, y_test = self.__resolve_datasets_for_fit_and_eval__(fit_on, eval_on)

        if num_train_points:
            X_train, _, y_train, _ = train_test_split(X_train, y_train, stratify=y_train, train_size=num_train_points)

        best_model, best_params = self.fit_and_select_model(X_train, y_train, params,
                                                            inside_optimizer_iteration=inside_optimizer_iteration,
                                                            **kwargs)
        score = 0.0
        if best_model is not None:
            score = f1_score(y_test, best_model.predict(X_test), average='macro')

        return score, best_model, best_params
