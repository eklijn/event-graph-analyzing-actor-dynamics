import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import os

from GraphConfigurator import GraphConfigurator
from AnalysisConfigurator import AnalysisConfigurator
from EventGraph import EventGraph
from concept_drift_detection.feature_extraction import FeatureExtraction
from concept_drift_detection import change_point_detection

# initialize graph and analysis settings
graph = "bpic2017_case_attr"
gc = GraphConfigurator(graph)
ac = AnalysisConfigurator(graph)
eg = EventGraph(gc.get_password(), gc.get_entity_labels())

# create global analysis directory
analysis_directory = os.path.join(ac.get_analysis_directory(), "concept_drift_detection")
os.makedirs(analysis_directory, exist_ok=True)

step_control_flow_drift_detection = False
step_actor_drift_detection = True

############ CP DETECTION - control flow ##############
if step_control_flow_drift_detection:
    window_size = 7

    feature_settings = [[["distinct_task_count", "count_per_task"], 1.2],
                        [["case_count"], 3]]
    # [["distinct_activity_count", "count_per_activity"], 3],
    # [["distinct_activity_lifecycle_count", "count_per_activity_lifecycle"], 3]]

    f_extr = FeatureExtraction(eg)
    f_extr.query_subgraphs_for_feature_extraction(window_size)

    for feature in feature_settings:
        feature_names, features = f_extr.apply_feature_extraction(feature[0])
        reduced_features = f_extr.pca_reduction(features, 'mle', normalize=True, normalize_function="max")
        cp = change_point_detection.rpt_pelt(reduced_features, pen=feature[1])
        print(f"Change points {feature[0]}: {cp}")
        change_point_detection.plot_cosine_similarity(features, feature[0], window_size)

############ CP DETECTION - actor drift ##############
if step_actor_drift_detection:
    actor_drift_directory = os.path.join(analysis_directory, "actor_drift")
    os.makedirs(actor_drift_directory, exist_ok=True)

    window_sizes = [7]
    penalties = [1, 2, 3]
    feature_sets = [[["distinct_task_count", "count_per_task"], "tasks"]]
                    # [["distinct_handover_count", "count_per_handover"], "handovers"],
                    # [["distinct_task_variant_count", "count_per_task_variant"], "task_variants"]]

    actor_list = eg.query_actor_list()
    # cp_settings = ["{}_{}".format(a_, b_) for a_, b_ in product(window_sizes, penalties)]

    for window_size in window_sizes:
        f_extr = FeatureExtraction(eg)
        f_extr.query_subgraphs_for_feature_extraction(window_size)

        for feature_set in feature_sets:
            actor_drift_feature_directory = os.path.join(actor_drift_directory, feature_set[1])
            os.makedirs(actor_drift_feature_directory, exist_ok=True)
            df_actor_drift_points = pd.DataFrame(index=actor_list, columns=penalties)
            for actor in actor_list:
                # actor_feature_set = [f"{feature}_{actor}" for feature in feature_set[0]]
                actor_feature_names, actor_features = f_extr.apply_feature_extraction(feature_set[0], actor=actor)
                reduced_actor_features = f_extr.pca_reduction(actor_features, 'mle', normalize=True, normalize_function="max")
                for pen in penalties:
                    cp = change_point_detection.rpt_pelt(reduced_actor_features, pen=pen)
                    print(f"Change points {feature_set[1]}: {cp}")
