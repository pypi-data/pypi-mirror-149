import re, sys, os, pickle, json, glob
import numpy as np, pandas as pd
from functools import cmp_to_key
from collections import OrderedDict
import logging
logger = logging.getLogger(__name__)
from compactem.core import oracle_transfer

# file name constants
filenames = {'task_info': "task_info.json",
             'flattening_info': "flattening_info.pckl",
             'indices': 'indices.json',
             'uncertainties_file': 'train_uncertainties.txt',
             'optimal_samples': 'optimal_samples.pckl',
             'NO_FILE': 'NA'}


class Result(object):
    """
    Bunch of output processing utilities are grouped here.
    """
    def __init__(self, task_dir):
        """
        :param task_dir: output directory for a previously run experiment.
        """
        self.task_dir = task_dir

    def process_results(self):
        """
        Processes and collects the results produced from experiment runs, for easy consumption. This is the *single
        point of write* for collated results. All other result processing utilities read the files produced herein.
        Collated results are saved as both csv and pickle, for debugging and preserving type information respectively.

        :return: None, processed results are read by other function.
        """
        task_info_file = os.path.join(self.task_dir, filenames['task_info'])

        # since some of the filenames are created downstream we subtract the task_dir paths here so that clean relative
        # paths only are added to the result files.
        original_task_dir = None
        with open(task_info_file) as f_task:
            task_info = json.loads(f_task.read())
            original_task_dir = task_info['task_dir']

        summary_dir = os.path.join(self.task_dir, 'summary')
        if not os.path.exists(summary_dir):
            os.mkdir(summary_dir)

        file_all_results = os.path.join(summary_dir, 'results.csv')
        file_matched_results = os.path.join(summary_dir, 'size_matched_results.csv')
        file_aggr_results = os.path.join(summary_dir, 'aggregated_results.csv')
        results_df = pd.DataFrame(columns=['dataset_name', 'num_classes', 'num_instances',
                                           'run_id', 'complexity_param', 'complexity_param_pickled_hex',
                                           'complexity', 'complexity_pickled_hex',
                                           'baseline_complexity', 'baseline_complexity_pickled_hex',
                                           'model', 'oracle', 'num_iterations',
                                           'original_score', 'new_score', 'pct_improvement', 'oracle_score',
                                           'optimal_parameters', 'scale',
                                           'runtime_in_sec_total', 'runtime_in_sec_opt',
                                           'best_model_path', 'baseline_model_path',
                                           'flattening_info_file', 'index_translation_file',
                                           'uncertainties_file', 'optimal_samples_file'])

        temp_path = self.task_dir + "/**/results.txt"
        for result_file in glob.glob(temp_path, recursive=True):
            with open(result_file, 'r') as f:
                result_json = json.loads(f.read())
            norm_path = os.path.normpath(result_file)
            run_info = norm_path.split(os.sep)[-3]
            try:
                run_id = int(re.search('run_(\d+)', run_info).groups()[0])
            except:
                continue

            fields = OrderedDict()
            # dataset related
            fields['dataset_name'] = result_json['dataset_properties']['name']
            fields['num_classes'] = int(result_json['dataset_properties']['classes'])
            fields['num_instances'] = int(result_json['dataset_properties']['instances'])

            # experiment parameters
            fields['complexity_param'] = result_json['general_info']['complexity_param']
            fields['complexity_param_pickled_hex'] = result_json['general_info']['complexity_param_pickled_hex']
            fields['complexity'] = result_json['optimized']['avg_model_complexity_for_best_param_val']
            fields['complexity_pickled_hex'] = result_json['optimized'][
                'avg_model_complexity_for_best_param_val_pickled_hex']
            fields['baseline_complexity'] = result_json['baseline_fits'][
                'complexity_best_test_model_based_on_train_val']
            fields['baseline_complexity_pickled_hex'] = \
                result_json['baseline_fits']['complexity_best_test_model_based_on_train_val_pickled_hex']
            fields['model'] = result_json['general_info']['model']
            fields['oracle'] = result_json['general_info']['oracle']
            fields['num_iterations'] = int(result_json['general_info']['optimizer_iterations'])
            fields['run_id'] = run_id

            # accuracy related
            fields['original_score'] = float(result_json['baseline_fits']['test_score_based_on_train_val'])
            temp_new_score = float(result_json['optimized']['test_score_obj_fn_at_best_params_val'])
            if temp_new_score < fields['original_score']:
                fields['new_score'] = fields['original_score']
                fields['pct_improvement'] = 0
            else:
                fields['new_score'] = temp_new_score
                fields['pct_improvement'] = float(result_json['optimized']['improvement_test_obj_fn_best_params_val'])

            fields['oracle_score'] = float(result_json['general_info']['oracle_score_on_test'])

            # This is converted into a json string *again* so that keys remain double quoted while writing it to a file
            # via pandas. Otherwise, if the keys become single quoted (which is an invalid json), the params cannot be
            # loaded using json.loads() later, and we'll have to resort to hacks like eval()
            fields['optimal_parameters'] = json.dumps(result_json['optimized']['best_params_val'])
            fields["scale"] = result_json['optimized']['scale']

            # logistics info - runtime, file paths
            fields['runtime_in_sec_total'] = float(result_json['runtimes']['total_runtime_in_secs'])
            fields['runtime_in_sec_opt'] = float(result_json['runtimes']['total_runtime_in_secs']) - float(
                result_json['runtimes']['time_till_baseline_fits'])  # only the optimization runtime
            fields['best_model_path'] = os.path.relpath(result_json['optimized']['model_path'], original_task_dir)
            fields['baseline_model_path'] = os.path.relpath(result_json['baseline_fits']
                                                            ['path_test_model_based_on_train_val'], original_task_dir)

            temp_fname = os.path.join(os.path.dirname(norm_path), filenames['flattening_info'])
            if os.path.exists(temp_fname):
                fields['flattening_info_file'] = os.path.relpath(temp_fname, original_task_dir)
            else:
                fields['flattening_info_file'] = filenames['NO_FILE']

            temp_fname = os.path.join(os.path.dirname(norm_path), filenames['indices'])
            fields["index_translation_file"] = os.path.relpath(temp_fname, original_task_dir)

            temp_fname = os.path.join(os.path.dirname(norm_path), filenames['uncertainties_file'])
            fields['uncertainties_file'] = os.path.relpath(temp_fname, original_task_dir)

            temp_fname = os.path.join(os.path.dirname(norm_path), filenames['optimal_samples'])
            if os.path.exists(temp_fname):
                fields['optimal_samples_file'] = os.path.relpath(temp_fname, original_task_dir)
            else:
                fields['optimal_samples_file'] = filenames['NO_FILE']

            # append to the dataframe
            results_df = results_df.append(fields, ignore_index=True)

        # ensure types are fine
        results_df = results_df.astype(dtype={'dataset_name': str,
                                              'num_classes': int,
                                              'num_instances': int,
                                              'num_iterations': int,
                                              'original_score': float,
                                              'new_score': float,
                                              'pct_improvement': float,
                                              'oracle_score': float,
                                              'runtime_in_sec_total': float,
                                              'runtime_in_sec_opt': float})

        results_df.sort_values(by=['dataset_name', 'complexity_param', 'run_id', 'new_score'], inplace=True)
        # new column to track specific experiment - one for which row, no semantics, just needs to be unique
        results_df['expt_ID'] = np.arange(len(results_df))
        results_df.reset_index(inplace=True, drop=True)
        # write this out
        results_df.to_csv(file_all_results, index=False)
        results_df.to_pickle(file_all_results + ".pckl")

        # align sizes: this is an important step, the same complexity parameter can lead to different complexities in
        # the baseline vs modified model. When we compare model scores, we want to compare for the same resultant
        # complexities, not same complexity params. This alignment is performed next. We track the "expt_ID" to know
        # what eventually was matched to what, for debugging.

        join_keys = ['dataset_name', 'run_id']
        common_columns = join_keys + ['complexity_param_pickled_hex', 'complexity_param', 'expt_ID']
        baseline_only_columns = ['baseline_complexity', 'baseline_complexity_pickled_hex', 'original_score',
                                 'baseline_model_path']
        baseline_related_columns = baseline_only_columns + common_columns
        new_model_related_columns = list(set(results_df.columns) - set(baseline_only_columns))

        # maintain order of columns for aesthetics
        # explicitly copy() otherwise pandas throws SettingWithCopyWarning
        temp_1 = results_df[sorted(new_model_related_columns,
                                   key=lambda x: list(results_df.columns).index(x))].copy()
        temp_1['complexity'] = [pickle.loads(bytes.fromhex(i)) for i in temp_1['complexity_pickled_hex']]
        # we need have one entry for dataset+run+complexity combination
        # temp_1.sort_values(by=['dataset_name', 'complexity', 'run_id', 'new_score'], inplace=True)

        temp_2 = results_df[baseline_related_columns].copy()
        temp_2.rename(columns={'complexity_param': 'baseline_complexity_param',
                               'expt_ID': "baseline_expt_ID",
                               'complexity_param_pickled_hex': 'baseline_complexity_param_pickled_hex'},
                      inplace=True)
        temp_2['baseline_complexity'] = [pickle.loads(bytes.fromhex(i)) for i in
                                         temp_2['baseline_complexity_pickled_hex']]
        temp_2['baseline_complexity_param'] = [pickle.loads(bytes.fromhex(i))
                                               for i in temp_2['baseline_complexity_param_pickled_hex']]

        # convert_dtypes() is needed to make sure pandas doesnt up-cast types to accommodate NAs
        temp_1, temp_2 = temp_1.convert_dtypes(), temp_2.convert_dtypes()

        # 'outer' and not 'left' because we want retain all info, even baseline-only info that doesn't match any
        # new model. Note, this can lead to multiple rows for a run_id + dataset + complexity
        # combination - that's OK, we will clean up in later steps, keeping the one with the highest new score.
        results_df = temp_1.join(
            temp_2.set_index(join_keys + ['baseline_complexity']), on=join_keys + ['complexity'],
            how='outer')

        # the join collapses the baseline_complexity values into the complexity column, but we want to keep it
        # separate for debugging. Hence we recreate this column based on the rows where some values are NA in the
        # outer join.

        new_compl, baseline_compl = [], []
        for (com, base_s, new_s) in zip(results_df['complexity'], results_df['original_score'],
                                        results_df['new_score']):
            assert not pd.isnull(base_s) or not pd.isnull(new_s), "Both baseline and new scores are null!"
            if pd.isnull(base_s):
                new_compl.append(com)
                baseline_compl.append(pd.NA)
            elif pd.isnull(new_s):
                baseline_compl.append(com)
                new_compl.append(pd.NA)
            else:
                new_compl.append(com)
                baseline_compl.append(com)
        results_df['complexity'] = new_compl
        results_df.insert(list(results_df.columns).index('complexity') + 1, 'baseline_complexity', baseline_compl)
        results_df.sort_values(by=['dataset_name', 'complexity', 'run_id', 'new_score'], inplace=True)
        results_df.reset_index(inplace=True, drop=True)

        # write this out
        results_df.to_csv(file_matched_results, index=False)
        results_df.to_pickle(file_matched_results + ".pckl")

        # aggregate these results

        # begin by getting rid of baseline-only rows
        results_df = results_df[~pd.isnull(results_df['complexity'])]

        # for duplicates for a dataset+run+id+complexity combination, we retain the only with the highest new score only
        results_df.sort_values(by=['dataset_name', 'complexity', 'run_id', 'new_score'], inplace=True)
        results_df.drop_duplicates(subset=['dataset_name', 'complexity', 'run_id'], keep='last', inplace=True)

        # next, add a column to keep the new score and model path together, this would help in aggregation
        def pick_model_path(r):
            if pd.isnull(r['new_score']):
                raise ValueError("new_score is null!")

            if pd.isnull(r['original_score']):
                return r['best_model_path']

            if r['pct_improvement'] == 0:
                return r['baseline_model_path']
            else:
                return r['best_model_path']

        results_df['temp_model_paths'] = results_df.apply(lambda row: ((row['original_score'], row['new_score']),
                                                                       pick_model_path(row)), axis=1)

        # create a dictionary of aggregations - note, since we want pct_improvement over the averages of new and
        # original, we compute it in a later step.

        # To aggregate file paths of models, we use a custom function - that returns json dict with keys as new scores
        # and values as the file paths.
        # It's good to remember here that pandas calculates the std dev with Bessel's correction, so if the grouping is
        # over one row, the std.dev. is *not* 0, its nan.
        # For some variables like iterations, num_classes, num_instances, we just use the first occurrence since they
        # change with the dataset only.

        aggr_dict = {'num_instances': pd.NamedAgg('num_instances', 'first'),
                     'num_classes': pd.NamedAgg('num_classes', 'first'),
                     'num_iterations': pd.NamedAgg('num_iterations', 'first'),
                     'avg_original_score': pd.NamedAgg('original_score', np.nanmean),
                     'std_original_score': pd.NamedAgg('original_score', np.nanstd),
                     'avg_new_score': pd.NamedAgg('new_score', 'mean'),
                     'std_new_score': pd.NamedAgg('new_score', np.std),
                     'avg_oracle_score': pd.NamedAgg('oracle_score', 'mean'),
                     'std_oracle_score': pd.NamedAgg('oracle_score', np.std),
                     'avg_runtime_in_sec_total': pd.NamedAgg('runtime_in_sec_total', 'mean'),
                     'avg_runtime_in_sec_opt': pd.NamedAgg('runtime_in_sec_opt', 'mean'),
                     'best_model_paths_json': pd.NamedAgg('temp_model_paths', lambda x: dict(x.values))}

        aggr_results = results_df.groupby(['dataset_name', 'complexity'], as_index=False).agg(**aggr_dict)

        def calculate_pct_improvement(r):
            if pd.isnull(r['avg_original_score']):
                return pd.NA
            elif r['avg_original_score'] == 0 and r['avg_new_score'] > 0:
                return float('inf')
            else:
                return max(100.0 * (r['avg_new_score'] - r['avg_original_score']) / r['avg_original_score'], 0.0)

        pct_improvement = aggr_results.apply(calculate_pct_improvement, axis=1)

        aggr_results.insert(list(aggr_results.columns).index("std_new_score") + 1, 'pct_improvement', pct_improvement)
        aggr_results.sort_values(by=['dataset_name', 'complexity'], inplace=True)

        # write this out
        aggr_results.to_csv(file_aggr_results, index=False)
        aggr_results.to_pickle(file_aggr_results + ".pckl")

    def get_optimal_sample(self, dataset_name, complexity):
        """
        This returns the optimal samples the optimizer found. For this to work the original experiments must have been
        run with a setting that actually saves such samples.

        :param dataset_name: the dataset for which the sample is required.
        :param complexity: the model complexity (*not* complexity param) for which the sample is required.
        :return: (1) A list of tuples (X, y) is returned, where the list has as many entries as the sampling_trials
            the experiment was run with. Each tuple (X, y) represents the selected sample per trial. The caller may
            aggregate these samples, or simply use any one of them.

            (2) the row from the aggregated results dataframe
            corresponding to the dataset_name and complexity are returned. In case of multiple rows, the one with the
            greatest new_score is selected.
        """
        # get the parameters
        expt_data_file = os.path.join(self.task_dir, 'summary', 'results.csv')
        df_results = pd.read_csv(expt_data_file)

        df_temp = df_results.query(f'dataset_name == "{dataset_name}" and complexity == {complexity}')
        result_row = dict(df_temp.sort_values(by=['new_score']).iloc[-1])

        if result_row['optimal_samples_file'] == filenames['NO_FILE']:
            msg_notif = "Optimal sample was not saved. Saving optimal sample needs to be explicitly enabled."
            print(msg_notif)
            raise FileNotFoundError(msg_notif)

        with open(os.path.join(self.task_dir, result_row['optimal_samples_file']), 'rb') as f:
            sample_info = pickle.load(f)

        return sample_info, result_row

    def read_processed_results(self, all=False):
        """
        The function is used to read the processed result files, and should be the single utility to read those files.
        In other words, this function abstracts away the filesystem: the user obtains dataframes here with no cognizance
        about the file details they're constructed from.

        :param all: if set to True, returns all intermediate dataframes, else only the final aggregated result dataframe
        :return: result dataframes:
            If ``all is True``, returns the *aggregated, size_matched, raw* dataframes.
            Else, returns only the dataframe with the *aggregated results*.
        """
        # get the type-appropriate values for all complexity values
        col_mapping = {'complexity_param_pickled_hex': 'complexity_param',
                       'complexity_pickled_hex': 'complexity',
                       'baseline_complexity_pickled_hex': 'baseline_complexity'}

        expt_data_file = os.path.join(self.task_dir, 'summary', 'results.csv.pckl')
        size_matched_file = os.path.join(self.task_dir, 'summary', 'size_matched_results.csv.pckl')
        aggr_file = os.path.join(self.task_dir, 'summary', 'aggregated_results.csv.pckl')

        try:
            df_results_raw = pd.read_pickle(expt_data_file)
            df_size_matched = pd.read_pickle(size_matched_file)
            df_aggr_results = pd.read_pickle(aggr_file)
            all_dfs = [df_results_raw, df_size_matched, df_aggr_results]
        except FileNotFoundError:
            notif_msg = f"One of the following result files are missing: {','.join(all_dfs)}."
            logging.error(notif_msg)
            raise FileNotFoundError(notif_msg)

        for orig_col, new_col in col_mapping.items():
            for temp_df in all_dfs:
                if orig_col in temp_df:
                    temp_df[new_col] = [pickle.loads(bytes.fromhex(i)) if not pd.isnull(i) else pd.NA
                                        for i in temp_df[orig_col]]
        if all:
            return df_aggr_results, df_size_matched, df_results_raw
        else:
            return df_aggr_results

    def get_compaction_profile(self):
        """
        This function draws up correspondences between baseline and new model complexities, within a task dir.
        Sometimes, this is easy to visualize to understand the compaction effect.

        :return: dict, key=dataset name, value=list of tuples (baseline complexity, new complexity
                that's as accurate as baseline)
        """
        aggr_results = self.read_processed_results()
        datasets = set(aggr_results['dataset_name'])
        compaction_profile = {}
        for d in datasets:
            # get rows for this dataset where we have both baseline and new model accuracies
            df_valid_rows = aggr_results[(aggr_results['dataset_name'] == d) &
                                         (~pd.isnull(aggr_results['avg_new_score'])) &
                                         (~pd.isnull(aggr_results['avg_original_score']))]
            corresp = get_size_correspondences(df_valid_rows['complexity'], df_valid_rows['avg_original_score'],
                                               df_valid_rows['avg_new_score'])
            compaction_profile[d] = corresp
        return compaction_profile

    def get_approx_sampled_indices(self, dataset_name, complexity, resamples=3):
        """
        **Experimental.**

        This function returns the indices of training data to which the optimizer assigns high significance.
        This is *not* the exact data the best final model was trained on; instead data is sampled based on the
        distribution that was learned. Hence, this is approximate.

        Note that this works based on the results produced by compact_using_oracle() and it needs the same task
        directory as input. If there are multiple instances dataset and complexity combination, e.g., because of
        multiple runs,different complexity parameters leading to the same complexity, the one with best new score is
        automatically picked.

        This returns indices:
        * if the compaction was done with explicit data splits, these are indices for the training data split
        * if split percentages were provided, these are indices for the overall data

        Essentially, these indices are to be applied to whatever data was provided.

        :param dataset_name: the dataset name
        :param complexity:
        :param resamples:
        :return: indices of sampled points
        """

        # get the parameters
        expt_data_file = os.path.join(self.task_dir, 'summary', 'results.csv')
        df_results = pd.read_csv(expt_data_file)

        df_temp = df_results.query(f'dataset_name == "{dataset_name}" and complexity == {complexity}')
        result_row = dict(df_temp.sort_values(by=['new_score']).iloc[-1])
        orig_data_size = result_row['num_instances']
        dist_params = json.loads(result_row['optimal_parameters'])
        dist_scale = result_row['scale']
        indices_file = result_row['index_translation_file']
        uncertainties_file = result_row['uncertainties_file']

        with open(os.path.join(self.task_dir, indices_file)) as f:
            h = json.loads(f.read())
        idx_train = np.array(h['idx_train'])
        y_train = np.array(h['y_train'])
        # Need to do this to pass into the sampling function, while being able to keep track of the indices.
        # The sampling function doesnt actually look at the data passed in - we exploit that here.
        X_dummy_train = idx_train.reshape(-1, 1)

        unc_vals = None
        with open(os.path.join(self.task_dir, uncertainties_file)) as f_unc:
            s = f_unc.read()
            unc_vals = list(map(float, s.split("\n")))

        sample_X, sample_y = oracle_transfer.sample_using_oracle(
            sample_size=int(dist_params['sample_size_as_pct'] * orig_data_size),
            X=X_dummy_train, y=y_train, uncertainties=unc_vals,
            dp_alpha=dist_params['dp_alpha'],
            prior_for_a_beta_A=dist_params['prior_for_a_beta_A'],
            prior_for_a_beta_B=dist_params['prior_for_a_beta_B'],
            prior_for_b_beta_A=dist_params['prior_for_b_beta_A'],
            prior_for_b_beta_B=dist_params['prior_for_b_beta_B'],
            scale_a=dist_scale, scale_b=dist_scale,
            pct_from_original=dist_params['pct_from_original'])

        sampled_idxs = sample_X.flatten()
        return sampled_idxs


def get_size_correspondences(complexities, baseline_accs, new_accs, complexity_compare_func=None):
    """
    Given the model accuracies for baseline and the new model, for different complexities, this function returns a list
    of tuples of the form (x, y) where x is a baseline model complexity, and y is a new model complexity whose accuracy
    is equal or greater than the baseline model of complexity x.

    :param complexities: model complexities
    :param baseline_acc: corresponding baseline accuracies
    :param new_acc: corresponding new accuracies
    :param complexity_compare_func: a custom compare function for ordering complexities may be provided. It must accepts two
            arguments a, b and return a value <0 if a is to be sorted before b, a value >0 if a is to be sorted after
            b, and value == 0 if there is no preferential order defined for a and b.
    :return: list of tuples of complexities
    """
    temp = list(zip(complexities, baseline_accs, new_accs))
    temp = sorted(temp, key=None if complexity_compare_func is None else cmp_to_key(complexity_compare_func))

    correspondences = []
    for idx, i in enumerate(temp):
        curr_baseline_acc = i[1]
        valid_complexities = [j[0] for j in temp if curr_baseline_acc <= j[2]]

        # the case for key=None needs to be handled separately, this was something that was fixed in Python in 3.8,
        # see https://docs.python.org/3/library/functions.html#min
        if complexity_compare_func:
            min_valid_complexity = min(valid_complexities, key=cmp_to_key(complexity_compare_func))
        else:
            min_valid_complexity = min(valid_complexities)
        correspondences.append((i[0], min_valid_complexity))

    return correspondences
