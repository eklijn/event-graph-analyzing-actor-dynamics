from datetime import timedelta
from sklearn.decomposition import PCA
import numpy as np


class FeatureExtraction:
    def __init__(self, event_graph):
        self.num_windows = None
        self.event_graph = event_graph
        self.task_subgraphs_nodes = []
        self.task_subgraphs_edges = []
        self.event_subgraphs_nodes = []
        self.event_subgraphs_edges = []

    def query_subgraphs_for_feature_extraction(self, window_size):
        graph_start_date, graph_end_date = self.event_graph.query_start_end_date()

        # Calculate the number of windows
        self.num_windows = (graph_end_date - graph_start_date).days // window_size

        for window in range(0, self.num_windows):
            self.task_subgraphs_nodes.append(
                self.event_graph.query_task_subgraph_nodes(
                    (graph_start_date + timedelta(days=window * window_size)).strftime("%Y-%m-%d"),
                    (graph_start_date + timedelta(days=(window + 1) * window_size)).strftime(
                        "%Y-%m-%d")))
            # self.event_subgraphs_nodes.append(
            #     self.event_graph.query_event_subgraph_nodes(
            #         (graph_start_date + timedelta(days=window * window_size)).strftime("%Y-%m-%d"),
            #         (graph_start_date + timedelta(days=(window + 1) * window_size)).strftime(
            #             "%Y-%m-%d")))
            # self.task_subgraphs_edges.append(
            #     self.event_graph.query_task_subgraph_edges(
            #         (graph_start_date + timedelta(days=window * window_size)).strftime("%Y-%m-%d"),
            #         (graph_start_date + timedelta(days=(window + 1) * window_size)).strftime(
            #             "%Y-%m-%d")))
            # self.event_subgraphs_edges.append(
            #     self.event_graph.query_event_subgraph_edges(
            #         (graph_start_date + timedelta(days=window * window_size)).strftime("%Y-%m-%d"),
            #         (graph_start_date + timedelta(days=(window + 1) * window_size)).strftime(
            #             "%Y-%m-%d")))

    def apply_feature_extraction(self, features, actor="", actor_1="", actor_2=""):
        # feature_vectors = []
        feature_vectors = [[] for i in range(0, self.num_windows)]
        for feature in features:
            results = []
            if feature == "case_count":
                results = extract_number_of_cases(self.task_subgraphs_nodes, actor)
            if feature == "distinct_task_count":
                results = extract_distinct_task_count(self.task_subgraphs_nodes, actor)
            if feature == "distinct_task_variant_count":
                results = extract_distinct_task_variant_count(self.task_subgraphs_nodes, actor)
            if feature == "distinct_activity_count":
                results = extract_distinct_activity_count(self.event_subgraphs_nodes, actor)
            if feature == "distinct_activity_lifecycle_count":
                results = extract_distinct_activity_lifecycle_count(self.event_subgraphs_nodes, actor)
            if feature == "count_per_task":
                results = extract_count_per_task(self.task_subgraphs_nodes, actor)
            if feature == "count_per_activity_lifecycle":
                results = extract_count_per_activity(self.event_subgraphs_nodes, actor)
            if feature == "count_per_activity":
                results = extract_count_per_activity_lifecycle(self.event_subgraphs_nodes, actor)
            # more features
            for i in range(0, len(results)):
                for result in results[i]:
                    feature_vectors[i].append(result)
        # set non existent features to zero
        feature_names__ = []
        for window in range(0, self.num_windows):
            for feature in range(0, len(feature_vectors[window])):
                feature_names__.append(feature_vectors[window][feature][0])

        feature_names = list(set(feature_names__))

        feature_lists = []
        for feature_name in range(0, len(feature_names)):
            feature_list = []
            for window in range(0, self.num_windows):
                existing_features = [i[0] for i in feature_vectors[window]]
                if feature_names[feature_name] in existing_features:
                    # find index
                    idx = existing_features.index(feature_names[feature_name])
                    feature_list.append(feature_vectors[window][idx][1])
                else:
                    feature_list.append(0)
            feature_lists.append(feature_list)

        return feature_names, np.asarray(feature_lists).transpose()

    def pca_reduction(self, features_np, dimensions, normalize=False, normalize_function='max'):
        '''Reduces a time series of features
        features: Two dimensional array of features
        dimensions: Target dimensionality. Use 'mle' for automated choice of dimensionality
          Automated choice of dimensionality can sometimes fail, a manual choice of dimensionality
          is then needed. If the Feautres are more than the time series is long, the automated
          choice can not be applied. We sole this by first reducing the features to the length
          of the time series and then reducing automatically.
        normalize: Whether the feautres should be normalized before reduction. The
          features should be normalized, if they have very different scales.
        normalize_function: Choose 'max' or 'sum'
        '''
        # print(features_np.shape)
        # print(features_np)
        if normalize:
            row_sums = features_np.sum(axis=0) + 0.0001
            if normalize_function == 'max':
                row_sums = features_np.max(axis=0) + 0.0001
            # print(row_sums)
            new_matrix = features_np / row_sums[np.newaxis, :]
            features_np = new_matrix
            # print(features_np)
        tmp_features = features_np
        if dimensions == 'mle':
            if features_np.shape[1] > features_np.shape[0]:
                pca = PCA(n_components=features_np.shape[0], svd_solver="full")
                pca.fit(features_np)
                tmp_features = pca.transform(features_np)
        pca = PCA(n_components=dimensions, svd_solver="full")
        pca.fit(tmp_features)
        reduced_features = pca.transform(tmp_features)

        if reduced_features.shape[1] == 0:
            pca = PCA(n_components=1, svd_solver="full")
            pca.fit(tmp_features)
            reduced_features = pca.transform(tmp_features)
        # print("Original features: ", features_np.shape)
        # print("Reduced features shape: ", reduced_features.shape)
        return reduced_features


def extract_distinct_task_count(task_subgraphs_nodes, actor):
    results = []
    for df_subgraph in task_subgraphs_nodes:
        all_tasks = []
        for index, row in df_subgraph.iterrows():
            if actor == "":
                all_tasks.append(row['task'])
            else:
                if row['actor'] == actor:
                    all_tasks.append(row['task'])
        results.append([('distinct_task_count', len(set(all_tasks)))])
    return results


def extract_distinct_task_variant_count(task_subgraphs_nodes, actor):
    results = []
    for df_subgraph in task_subgraphs_nodes:
        all_task_variants = []
        for index, row in df_subgraph.iterrows():
            if actor == "":
                all_task_variants.append(row['task_variant'])
            else:
                if row['actor'] == actor:
                    all_task_variants.append(row['task_variant'])
        results.append([('distinct_task_variant_count', len(set(all_task_variants)))])
    return results


def extract_distinct_activity_count(event_subgraphs_nodes, actor):
    results = []
    for df_subgraph in event_subgraphs_nodes:
        all_activity = []
        for index, row in df_subgraph.iterrows():
            if actor == "":
                all_activity.append(row['activity'])
            else:
                if row['actor'] == actor:
                    all_activity.append(row['activity'])
        results.append([('distinct_activity_count', len(set(all_activity)))])
    return results


def extract_distinct_activity_lifecycle_count(event_subgraphs_nodes, actor):
    results = []
    for df_subgraph in event_subgraphs_nodes:
        all_activity_lifecycle = []
        for index, row in df_subgraph.iterrows():
            if actor == "":
                all_activity_lifecycle.append(row['activity_lifecycle'])
            else:
                if row['actor'] == actor:
                    all_activity_lifecycle.append(row['activity_lifecycle'])
        results.append([('distinct_activity_lifecycle_count', len(set(all_activity_lifecycle)))])
    return results


def extract_number_of_cases(task_subgraphs_nodes, actor):
    results = []
    for df_subgraph in task_subgraphs_nodes:
        all_cases = []
        for index, row in df_subgraph.iterrows():
            if actor == "":
                all_cases.append(row['case'])
            else:
                if row['actor'] == actor:
                    all_cases.append(row['case'])
        results.append([('case_count', len(set(all_cases)))])
    return results


def extract_count_per_task(task_subgraphs_nodes, actor):
    results = []
    for df_subgraph in task_subgraphs_nodes:
        count_per_task = {}
        count_per_task = {"total": 0}
        for index, row in df_subgraph.iterrows():
            if actor == "":
                if not row['task'] in count_per_task.keys():
                    count_per_task[row['task']] = 0
                count_per_task[row['task']] += 1
                count_per_task["total"] += 1
            else:
                if row['actor'] == actor:
                    if not row['task'] in count_per_task.keys():
                        count_per_task[row['task']] = 0
                    count_per_task[row['task']] += 1
                    count_per_task["total"] += 1
        subgraph_results = [('Task_count' + str(task), count_per_task[task]) for task in count_per_task.keys()]
        results.append(subgraph_results)
    return results


def extract_count_per_task_variant(task_subgraphs_nodes, actor):
    results = []
    for df_subgraph in task_subgraphs_nodes:
        count_per_task_variant = {}
        count_per_task_variant = {"total": 0}
        for index, row in df_subgraph.iterrows():
            if actor == "":
                if not row['task_variant'] in count_per_task_variant.keys():
                    count_per_task_variant[row['task_variant']] = 0
                count_per_task_variant[row['task_variant']] += 1
                count_per_task_variant["total"] += 1
            else:
                if row['actor'] == actor:
                    if not row['task_variant'] in count_per_task_variant.keys():
                        count_per_task_variant[row['task_variant']] = 0
                    count_per_task_variant[row['task_variant']] += 1
                    count_per_task_variant["total_variant"] += 1
        subgraph_results = [('Task_variant_count' + str(task_variant), count_per_task_variant[task_variant]) for
                            task_variant in count_per_task_variant.keys()]
        results.append(subgraph_results)
    return results


def extract_count_per_activity(event_subgraphs_nodes, actor):
    results = []
    for df_subgraph in event_subgraphs_nodes:
        # count_per_activity = {}
        count_per_activity = {"total": 0}
        for index, row in df_subgraph.iterrows():
            if actor == "":
                if not row['activity'] in count_per_activity.keys():
                    count_per_activity[row['activity']] = 0
                count_per_activity[row['activity']] += 1
                count_per_activity["total"] += 1
            else:
                if row['actor'] == actor:
                    if not row['activity'] in count_per_activity.keys():
                        count_per_activity[row['activity']] = 0
                    count_per_activity[row['activity']] += 1
                    count_per_activity["total"] += 1
        subgraph_results = [
            ('Activity_count' + str(activity), count_per_activity[activity]) for activity in count_per_activity.keys()]
        results.append(subgraph_results)
    return results


def extract_count_per_activity_lifecycle(event_subgraphs_nodes, actor):
    results = []
    for df_subgraph in event_subgraphs_nodes:
        # count_per_activity_lifecycle = {}
        count_per_activity_lifecycle = {"total": 0}
        for index, row in df_subgraph.iterrows():
            if actor == "":
                if not row['activity_lifecycle'] in count_per_activity_lifecycle.keys():
                    count_per_activity_lifecycle[row['activity_lifecycle']] = 0
                count_per_activity_lifecycle[row['activity_lifecycle']] += 1
                count_per_activity_lifecycle["total"] += 1
            else:
                if row['actor'] == actor:
                    if not row['activity_lifecycle'] in count_per_activity_lifecycle.keys():
                        count_per_activity_lifecycle[row['activity_lifecycle']] = 0
                    count_per_activity_lifecycle[row['activity_lifecycle']] += 1
                    count_per_activity_lifecycle["total"] += 1
        subgraph_results = [
            ('Activity_lifecycle_count' + str(activity_lifecycle), count_per_activity_lifecycle[activity_lifecycle]) for
            activity_lifecycle in count_per_activity_lifecycle.keys()]
        results.append(subgraph_results)
    return results
