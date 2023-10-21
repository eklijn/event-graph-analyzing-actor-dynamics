import os

from GraphConfigurator import GraphConfigurator
from AnalysisConfigurator import AnalysisConfigurator
from EventGraph import EventGraph
from modules.task_cd_detection import concept_drift_analysis

# initialize graph and analysis settings
graph = "bpic2017_susp_res"
gc = GraphConfigurator(graph)
ac = AnalysisConfigurator(graph)
eg = EventGraph(gc.get_password(), gc.get_entity_labels())

# create global analysis directory
analysis_directory = os.path.join(ac.get_analysis_directory(), "modules/task_cd_detection")
os.makedirs(analysis_directory, exist_ok=True)

window_sizes = [1, 7]
penalties = [1.5, 2, 2.5, 3]

step_process_level_drift_detection = False

# process_drift_feature_sets = {"total_actions": ["total_activity_lifecycle_count"],
#                               "total_tasks": ["total_task_count"]}
# process_drift_feature_sets = {"task_handovers_actor": ["count_per_task_handover_actor"]}
# process_drift_feature_sets = {"activity_lcs": ["count_per_activity_lifecycle"]}
# process_drift_feature_sets = {"tasks_relative": ["count_per_task_relative"],
#                               "task_variants_relative": ["count_per_task_variant_relative"],
#                               "activity_lcs_relative": ["count_per_activity_lifecycle_relative"]}
process_drift_feature_sets = {"tasks": ["count_per_task"],
                              "task_variants": ["count_per_task_variant"],
                              "activities": ["count_per_activity"],
                              "task_handovers_case": ["count_per_task_handover_case"],
                              "task_variant_handovers_case": ["count_per_task_variant_handover_case"],
                              "activity_handovers_case": ["count_per_activity_handover_case"],
                              "task_handovers_actor": ["count_per_task_handover_actor"],
                              "task_variant_handovers_actor": ["count_per_task_variant_handover_actor"],
                              "activity_handovers_actor": ["count_per_activity_handover_actor"],
                              "tasks_relative": ["count_per_task_relative"],
                              "task_variants_relative": ["count_per_task_variant_relative"],
                              "activities_relative": ["count_per_activity_relative"],
                              "task_handovers_case_relative": ["count_per_task_handover_case_relative"],
                              "task_variant_handovers_case_relative": ["count_per_task_variant_handover_case_relative"],
                              "activity_handovers_case_relative": ["count_per_activity_handover_case_relative"],
                              "task_handovers_actor_relative": ["count_per_task_handover_actor_relative"],
                              "task_variant_handovers_actor_relative": ["count_per_task_variant_handover_actor_relative"],
                              "activity_handovers_actor_relative": ["count_per_activity_handover_actor_relative"]}

step_actor_drift_detection = False
actor_drift_feature_sets = {"tasks_relative": ["count_per_task_relative"],
                            "task_variants_relative": ["count_per_task_variant_relative"],
                            "activities_relative": ["count_per_activity_relative"],
                            "task_handovers_actor_relative": ["count_per_task_handover_actor_relative"],
                            "task_variant_handovers_actor_relative": ["count_per_task_variant_handover_actor_relative"],
                            "activity_handovers_actor_relative": ["count_per_activity_handover_actor_relative"]}
# actors = eg.query_actor_list(min_freq=1000)
actors = ["User_3", "User_87", "User_5", "User_30", "User_2", "User_100", "User_29", "User_49", "User_68",
          "User_28", "User_41", "User_75", "User_123", "User_18", "User_99", "User_27", "User_15"]

step_colab_drift_detection = True
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
