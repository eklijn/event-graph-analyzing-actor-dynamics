from GraphConfigurator import GraphConfigurator
from AnalysisConfigurator import AnalysisConfigurator
from DFGVisualizer import DFGVisualizer

# --------------------------- BEGIN CONFIG ----------------------------- #
# TO START:
# specify the name of the graph:
graph = "bpic2017_case_attr"
# and configure all the settings related to this graph name in "graph_confs.py"
gc = GraphConfigurator(graph)

# specify the analysis description (patterns to be analyzed and number of clusters)
pattern_subset_description = "P_freq_geq_10__C_20"
# and configure all analysis parameters in "analysis_confs.py"
ac = AnalysisConfigurator(pattern_subset_description)

step_create_intra_task_DFG = False
step_create_inter_task_DFG = False
step_create_inter_task_DFG_concept_drift_comparison = False
step_create_inter_task_DFG_resource_specific = False

# ------------------------------ END CONFIG ---------------------------- #

dfg_vis = DFGVisualizer(graph, gc.get_password(), gc.get_name_data_set(), gc.get_entity_labels(),
                        gc.get_action_lifecycle_labels(), ac.get_analysis_directory(),
                        ac.get_clustering_instance_description(), ac.get_dfg_exclude_clusters())
if step_create_inter_task_DFG:
    dfg_vis.visualize_inter_task_DFG('case', ac.get_dfg_inter_show_threshold(), ac.get_dfg_inter_weight_threshold(),
                                     start_end_date=ac.get_dfg_inter_start_end_date(),
                                     resources=ac.get_dfg_inter_resources(),
                                     print_description=ac.get_dfg_inter_print_description())
if step_create_intra_task_DFG:
    dfg_vis.visualize_intra_task_DFG(ac.get_task_cluster_to_mine())
if step_create_inter_task_DFG_concept_drift_comparison:
    dfg_vis.visualize_inter_task_DFG_concept_drift_comparison('case', ac.get_dfg_inter_show_threshold(),
                                                              ac.get_dfg_inter_cd_comparison_start_end_dates())
if step_create_inter_task_DFG_resource_specific:
    dfg_vis.visualize_inter_task_DFG_resources(ac.get_dfg_resource_inter_show_threshold_under(),
                                               ac.get_dfg_resource_inter_show_threshold_over(),
                                               ac.get_dfg_resource_inter_list_overlaid(),
                                               start_end_date=ac.get_dfg_resource_inter_start_end_date(),
                                               resources=ac.get_dfg_resource_inter_resources())
