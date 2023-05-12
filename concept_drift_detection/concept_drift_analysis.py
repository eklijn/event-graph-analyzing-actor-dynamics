import pandas as pd
import numpy as np
from tqdm import tqdm
from itertools import product
import os

from concept_drift_detection.feature_extraction import FeatureExtraction
from concept_drift_detection import change_point_detection
from concept_drift_detection import change_point_visualization


def get_feature_extractor_objects(feature_names, window_sizes, eg, exclude_cluster=""):
    list_f_extr = []
    for window_size in window_sizes:
        f_extr = FeatureExtraction(eg, exclude_cluster)
        f_extr.query_subgraphs_for_feature_extraction(window_size, feature_names)
        list_f_extr.append(f_extr)
    return list_f_extr


def strip_inactive_windows(features):
    index_where_inactive = list(np.where(np.all(features == 0, axis=1)))
    original_index = list(range(0, len(features)))
    original_index_stripped = sorted(np.setdiff1d(original_index, index_where_inactive))
    features_stripped = features[np.where(~np.all(features == 0, axis=1))]
    return features_stripped, original_index_stripped


def strip_inactive_windows_colab(features, actor_1_activity, actor_2_activity):
    index_where_inactive_actor_1 = list(np.where(np.all(actor_1_activity == 0, axis=1)))
    index_where_inactive_actor_2 = list(np.where(np.all(actor_2_activity == 0, axis=1)))
    list_both_inactive = np.concatenate([index_where_inactive_actor_1, index_where_inactive_actor_2], axis=1).flatten()
    index_where_either_inactive = sorted(list(set(list_both_inactive)))
    original_index = list(range(0, len(features)))
    original_index_stripped = sorted(np.setdiff1d(original_index, index_where_either_inactive))
    features_stripped = features[np.where(~np.all(features == 0, axis=1))]
    return features_stripped, original_index_stripped


def retrieve_original_cps(cps, original_index_stripped):
    actual_cps = []
    for cp in cps:
        actual_cps.append(original_index_stripped[cp])
    return actual_cps


def remove_duplicate_colab_pairs(colab_pairs):
    colab_pairs_distinct = []
    for colab_pair in colab_pairs:
        sorted_colab_pair = sorted(colab_pair)
        if sorted_colab_pair not in colab_pairs_distinct:
            colab_pairs_distinct.append(sorted_colab_pair)
    return colab_pairs_distinct


def detect_process_level_drift(window_sizes, penalties, feature_sets, analysis_directory, event_graph,
                               exclude_cluster, plot_drift=False):
    all_features = [item for sublist in list(feature_sets.values()) for item in sublist]
    list_f_extr = get_feature_extractor_objects(all_features, window_sizes, event_graph, exclude_cluster)

    # create analysis directory for process drift detection
    process_level_drift_directory = os.path.join(analysis_directory, f"process_level_drift")
    os.makedirs(process_level_drift_directory, exist_ok=True)

    # initialize dataframe to store change points
    cp_settings = ["{}_{}".format(a_, b_) for a_, b_ in product(window_sizes, penalties)]
    indices = [fs_name for fs_name, _ in feature_sets.items()]
    df_process_level_drift_points = pd.DataFrame(index=indices, columns=cp_settings)

    for feature_set_name, feature_list in feature_sets.items():
        # create analysis directory for specified feature set
        process_level_drift_feature_directory = os.path.join(process_level_drift_directory, feature_set_name)
        os.makedirs(process_level_drift_feature_directory, exist_ok=True)

        for index, window_size in enumerate(window_sizes):
            feature_names, feature_vector = list_f_extr[index].apply_feature_extraction(feature_list)
            reduced_feature_vector = list_f_extr[index].pca_reduction(feature_vector, 'mle', normalize=True,
                                                                      normalize_function="max")
            for pen in penalties:
                # detect change points for specified penalty and write to dataframe
                cp = change_point_detection.rpt_pelt(reduced_feature_vector, pen=pen)
                print(f"Change points {feature_set_name}: {cp}")
                df_process_level_drift_points.loc[feature_set_name, f"{window_size}_{pen}"] = cp
            if plot_drift:
                change_point_visualization.plot_trends(feature_vector, feature_names, window_size,
                                                       process_level_drift_feature_directory)
    df_process_level_drift_points.to_csv(f"{process_level_drift_directory}\\process_cp.csv")


def detect_actor_drift(window_sizes, penalties, feature_sets, actor_list, analysis_directory, event_graph,
                       exclude_cluster, plot_drift=False):
    all_features = [item for sublist in list(feature_sets.values()) for item in sublist]
    list_f_extr = get_feature_extractor_objects(all_features, window_sizes, event_graph, exclude_cluster)

    for feature_set_name, feature_list in feature_sets.items():
        print(f"Feature set: {feature_set_name}")

        # create analysis directory for (actor drift detection X specified feature set)
        actor_drift_feature_directory = os.path.join(analysis_directory, f"actor_drift\\{feature_set_name}")
        os.makedirs(actor_drift_feature_directory, exist_ok=True)

        # initialize dataframe to store change points for specified feature set
        cp_settings = ["{}_{}".format(a_, b_) for a_, b_ in product(window_sizes, penalties)]
        df_actor_drift_points = pd.DataFrame(index=actor_list, columns=cp_settings)

        print(f"Detecting change points for {len(actor_list)} actors...")
        for actor in tqdm(actor_list):
            # create analysis directory for actor to plot
            if plot_drift:
                actor_drift_feature_subdirectory = os.path.join(actor_drift_feature_directory, actor)
                os.makedirs(actor_drift_feature_subdirectory, exist_ok=True)

            # initialize dictionary to store change points for specified feature set
            dict_actor_drift_points = {}
            for index, window_size in enumerate(window_sizes):
                # generate mv time series for specified features/actor/window size
                actor_feature_names, actor_feature_vector = list_f_extr[index].apply_feature_extraction(feature_list, actor=actor,
                                                                                                        actor_1=actor,
                                                                                                        actor_2=actor)
                actor_feature_vector_stripped, time_window_mapping = strip_inactive_windows(actor_feature_vector)
                reduced_actor_feature_vector = list_f_extr[index].pca_reduction(actor_feature_vector_stripped, 'mle',
                                                                                normalize=True,
                                                                                normalize_function="max")
                for pen in penalties:
                    # detect change points for specified penalty and write to dataframe
                    cp = change_point_detection.rpt_pelt(reduced_actor_feature_vector, pen=pen)
                    # print(f"Change points {actor} {feature_set[1]} (pen={pen}): {cp}")
                    cp = retrieve_original_cps(cp, time_window_mapping)
                    df_actor_drift_points.loc[actor, f"{window_size}_{pen}"] = cp
                    dict_actor_drift_points[pen] = cp
                if plot_drift:
                    change_point_visualization.plot_trends(actor_feature_vector, actor_feature_names, window_size,
                                                           actor_drift_feature_subdirectory, dict_actor_drift_points,
                                                           actor, min_freq=20)
        df_actor_drift_points.to_csv(f"{actor_drift_feature_directory}\\actor_cp_{feature_set_name}.csv")


def detect_colab_drift(window_sizes, penalties, detailed_analysis, colab_list, analysis_directory, event_graph,
                       exclude_cluster, plot_drift=False):
    colab_pairs_distinct = remove_duplicate_colab_pairs(colab_list)
    if detailed_analysis:
        feature_sets = {"task_handovers_case": ["count_per_task_handover_case"]}
    else:
        feature_sets = {"total_task_handovers_case": ["total_task_handover_count_case"]}

    all_features = [item for sublist in list(feature_sets.values()) for item in sublist]
    all_features += ["total_task_count"]
    list_f_extr = get_feature_extractor_objects(all_features, window_sizes, event_graph, exclude_cluster)

    # set up indices and columns for dataframes
    cp_settings = ["{}_{}".format(a_, b_) for a_, b_ in product(window_sizes, penalties)]
    index_colab_pairs = [f"{pair[0]}_{pair[1]}" for pair in colab_pairs_distinct]

    # retrieve activity per time window for all actors in colab_pairs
    list_actors = [actor for colab_pair in colab_pairs_distinct for actor in colab_pair]
    dicts_actor_activity_per_ws = []
    for i, ws in enumerate(window_sizes):
        dict_actor_activity = {}
        for a in list_actors:
            _, actor_activity = list_f_extr[i].apply_feature_extraction(["total_task_count"], actor=a)
            dict_actor_activity[a] = actor_activity
        dicts_actor_activity_per_ws.append(dict_actor_activity)

    for feature_set_name, feature_list in feature_sets.items():
        print(f"Feature set: {feature_set_name}")

        # create analysis directory for (colab drift detection X specified feature set)
        colab_drift_feature_directory = os.path.join(analysis_directory, f"colab_drift\\{feature_set_name}")
        os.makedirs(colab_drift_feature_directory, exist_ok=True)

        # initialize dataframe to store change points for specified feature set
        df_colab_drift_points = pd.DataFrame(index=index_colab_pairs, columns=cp_settings)

        for colab_pair in colab_pairs_distinct:
            # create analysis directory for actor to plot
            if plot_drift:
                colab_drift_feature_subdirectory = os.path.join(colab_drift_feature_directory, f"{colab_pair[0]}_{colab_pair[1]}")
                os.makedirs(colab_drift_feature_subdirectory, exist_ok=True)

            colab_pair_reversed = colab_pair[::-1]
            for index, window_size in enumerate(window_sizes):
                actor_1_activity = dicts_actor_activity_per_ws[index][colab_pair[0]]
                actor_2_activity = dicts_actor_activity_per_ws[index][colab_pair[1]]

                # generate mv time series for specified features/colab_pair/window size
                colab_feature_names, colab_feature_vector = list_f_extr[index].apply_feature_extraction(
                    feature_list, actor_1=colab_pair[0], actor_2=colab_pair[1])
                colab_feature_names = [f"dir1_{f_name}" for f_name in colab_feature_names]
                colab_reverse_feature_names, colab_reverse_feature_vector = list_f_extr[index].apply_feature_extraction(
                    feature_list, actor_1=colab_pair_reversed[0], actor_2=colab_pair_reversed[1])
                colab_reverse_feature_names = [f"dir2_{f_name}" for f_name in colab_reverse_feature_names]
                colab_total_feature_vector = np.concatenate((colab_feature_vector, colab_reverse_feature_vector),
                                                            axis=1)
                colab_total_feature_vector_stripped, time_window_mapping = strip_inactive_windows_colab(
                    colab_total_feature_vector,
                    actor_1_activity,
                    actor_2_activity)

                colab_all_feature_names = colab_feature_names + colab_reverse_feature_names
                reduced_colab_feature_vector = list_f_extr[index].pca_reduction(colab_total_feature_vector_stripped,
                                                                                'mle', normalize=True,
                                                                                normalize_function="max")
                for pen in penalties:
                    # detect change points for specified penalty and write to dataframe
                    cp = change_point_detection.rpt_pelt(reduced_colab_feature_vector, pen=pen)
                    cp = retrieve_original_cps(cp, time_window_mapping)
                    print(
                        f"Change points {colab_pair[0]}_{colab_pair[1]} {feature_set_name} (pen={pen}): {cp}")
                    df_colab_drift_points.loc[f"{colab_pair[0]}_{colab_pair[1]}", f"{window_size}_{pen}"] = cp
                if plot_drift:
                    change_point_visualization.plot_trends(colab_total_feature_vector, colab_all_feature_names, window_size,
                                                           colab_drift_feature_subdirectory, "",
                                                           f"{colab_pair[0]}_{colab_pair[1]}", min_freq=20)
        df_colab_drift_points.to_csv(f"{colab_drift_feature_directory}\\colab_cp_{feature_set_name}.csv")


def plot_all_actor_activity(analysis_directory, event_graph):
    actor_activity_trend_directory = os.path.join(analysis_directory, "actor_drift", "overall_frequency")
    os.makedirs(actor_activity_trend_directory, exist_ok=True)

    window_sizes = [1, 7]
    actor_list = event_graph.query_actor_list()
    actor_list = ["User_87", "User_30"]

    list_f_extr = get_feature_extractor_objects(["total_task_count"], window_sizes, event_graph)

    for actor_to_plot in actor_list:
        for index, window_size in enumerate(window_sizes):
            # generate mv time series for specified features/actor/window size
            actor_feature_names, actor_feature_vector = list_f_extr[index].apply_feature_extraction(
                ["total_task_count"], actor=actor_to_plot)
            change_point_visualization.plot_trends(actor_feature_vector, actor_feature_names, window_size,
                                                   actor_activity_trend_directory, subgroup=actor_to_plot)
