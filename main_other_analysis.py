from GraphConfigurator import GraphConfigurator
from AnalysisConfigurator import AnalysisConfigurator
from modules.other_analysis.TaskAnalyzer import TaskAnalyzer

# EVENT GRAPH, HIGH LEVEL EVENTS, AND CLASS CONSTRUCTS SHOULD ALREADY IN PLACE
# -------------- BEGIN CONFIG ----------------- #

# TO START:
# specify the name of the graph:
# graph = "operators"
graph = "bpic2017_case_attr"
# and configure all the settings related to this graph name in "graph_confs_old.py"
gc = GraphConfigurator(graph)
# and configure all analysis parameters in "analysis_confs.py"
ac = AnalysisConfigurator(graph)

# ------------- OTHER ANALYSIS ------------- #
t_analyzer = TaskAnalyzer(graph, ac.get_analysis_directory(), ac.get_clustering_instance_description())
# trend
# step_plot_variant_trends_per_cluster = False
# if step_plot_variant_trends_per_cluster:
# t_analyzer.plot_variant_trends_per_cluster(clusters=t_agg.get_cluster_list())


clusters_to_analyze_inter_cluster = range(0, 20)

step_plot_variant_trends_paper = False
step_plot_variant_trends_variant_subset = False
step_plot_variant_trends_variants_resources = False
# resources_trend = ["User_29", "User_30", "User_68", "User_100"]
# resources_trend = ["User_5", "User_16", "User_49"]
# resources_trend = ["User_3", "User_5", "User_10", "User_49"]
# resources_trend = ["User_113", "User_116", "User_121", "User_123"]
# resources_trend = ["User_116", "User_121", "User_123"]
resources_trend = ["User_113", "User_121", "User_123"]
variants_trend = [25, 49]

case_attribute_to_analyze = "AT"
group_type = 'Cluster'
# groups_to_compare = [[1, 9], 25]
# groups_to_compare = [[1, 3, 9], [25, 3]]
# groups_to_compare = [50, [9, 53]]
groups_to_compare = [1, 2, 5, 10, 16]

groups_description = ""
# groups_description = "all clusters"
resources_to_compare = [1, 3, 5, 10, 27, 29, 30, 49, 68, 75, 87, 90, 99, 100, 109, 112, 113, 116, 117, 120, 121, 123,
                        126]
# resources_description = ""
resources_description = "most_frequent"

step_plot_heatmap_case_attributes_per_cluster = False
step_plot_heatmap_case_attributes_across_groups = False

step_plot_heatmap_resources_across_groups = False

step_plot_boxplot_case_duration_across_groups = False
step_plot_boxplot_case_duration_group_and_remainder = False
group = [16]

step_plot_cluster_bar_chart = False

if step_plot_variant_trends_paper:
    # ta.plot_variant_trends_paper()
    # ta.plot_variant_trends_paper_appendix()
    t_analyzer.plot_variant_trends_variants_resources_paper()

if step_plot_variant_trends_variants_resources:
    t_analyzer.plot_variant_trends_variants_resources(variants_trend, resources_trend)

# CASE ATTRIBUTE ANALYSIS
if step_plot_heatmap_case_attributes_per_cluster:
    t_analyzer.plot_heatmap_case_attributes_per_cluster(ac.get_case_analysis_filters()[case_attribute_to_analyze],
                                                        clusters_to_analyze_inter_cluster)
if step_plot_heatmap_case_attributes_across_groups:
    t_analyzer.plot_heatmap_case_attributes_across_groups(group_type, groups_to_compare,
                                                          ac.get_case_analysis_filters()[case_attribute_to_analyze])

# RESOURCE ANALYSIS
if step_plot_heatmap_resources_across_groups:
    t_analyzer.plot_heatmap_resources_across_groups(group_type, groups_to_compare, resources_to_compare,
                                                    groups_description, resources_description)

# PERFORMANCE ANALYSIS
if step_plot_boxplot_case_duration_across_groups:
    t_analyzer.plot_boxplot_case_duration_across_groups(group_type, groups_to_compare)
if step_plot_boxplot_case_duration_group_and_remainder:
    t_analyzer.plot_boxplot_case_duration_group_and_remainder(group_type, group)

# variant FREQUENCY ANALYSIS
if step_plot_cluster_bar_chart:
    t_analyzer.plot_cluster_bar_chart()
