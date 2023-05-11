import os

from GraphConfigurator import GraphConfigurator
from AnalysisConfigurator import AnalysisConfigurator
from EventGraph import EventGraph
from concept_drift_detection import concept_drift_analysis

# initialize graph and analysis settings
graph = "bpic2017_susp_res"
gc = GraphConfigurator(graph)
ac = AnalysisConfigurator(graph)
eg = EventGraph(gc.get_password(), gc.get_entity_labels())

# create global analysis directory
analysis_directory = os.path.join(ac.get_analysis_directory(), "concept_drift_detection")
os.makedirs(analysis_directory, exist_ok=True)

window_sizes = [7]
penalties = [1.5, 2, 2.5, 3]

step_process_level_drift_detection = True
# process_drift_feature_sets = {"total_actions": ["total_activity_lifecycle_count"],
#                               "total_tasks": ["total_task_count"]}
# process_drift_feature_sets = {"task_handovers_actor": ["count_per_task_handover_actor"]}
process_drift_feature_sets = {"activity_lcs": ["count_per_activity_lifecycle"]}
# process_drift_feature_sets = {"tasks": ["count_per_task"],
#                               "task_variants": ["count_per_task_variant"],
#                               "activity_lcs": ["count_per_activity_lifecycle"],
#                               "task_handovers_case": ["count_per_task_handover_case"],
#                               "task_variant_handovers_case": ["count_per_task_variant_handover_case"],
#                               "activity_lc_handovers_case": ["count_per_activity_lifecycle_handover_case"]}

step_actor_drift_detection = False
actor_drift_feature_sets = {"tasks": ["count_per_task"]}
# actors = eg.query_actor_list(min_freq=1000)
actors = ["User_27", "User_29"]

step_colab_drift_detection = False
# colab_pairs = eg.query_colab_list()
colab_pairs = [["User_87", "User_30"]]

step_plot_all_actor_frequency = False

if step_process_level_drift_detection:
    concept_drift_analysis.detect_process_level_drift(window_sizes=window_sizes, penalties=penalties,
                                                      feature_sets=process_drift_feature_sets,
                                                      analysis_directory=analysis_directory, event_graph=eg,
                                                      exclude_cluster=ac.get_leftover_cluster(), plot_drift=True)

if step_actor_drift_detection:
    concept_drift_analysis.detect_actor_drift(window_sizes=window_sizes, penalties=penalties,
                                              feature_sets=actor_drift_feature_sets, actor_list=actors,
                                              analysis_directory=analysis_directory, event_graph=eg,
                                              exclude_cluster=ac.get_leftover_cluster(), plot_drift=True)

if step_colab_drift_detection:
    concept_drift_analysis.detect_colab_drift(window_sizes=window_sizes, penalties=penalties,
                                              detailed_analysis=True, colab_list=colab_pairs,
                                              analysis_directory=analysis_directory, event_graph=eg,
                                              exclude_cluster=ac.get_leftover_cluster(), plot_drift=True)

if step_plot_all_actor_frequency:
    concept_drift_analysis.plot_all_actor_activity(analysis_directory, eg)
