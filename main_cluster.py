from GraphConfigurator import GraphConfigurator
from modules.task_clustering.ClusterConfigurator import ClusterConfigurator
from modules.task_clustering.ClusterConstructor import ClusterConstructor
from modules.task_clustering.TaskClusterModule import TaskClusterModule
from modules.task_clustering.VariantVisualizer import VariantVisualizer

# --------------------------- BEGIN CONFIG ----------------------------- #
# TO START:
# specify the name of the graph:
# graph = "operators"
graph = "bpic2017_susp_res"
# and configure all the settings related to this graph name in "graph_confs_old.py"
gc = GraphConfigurator(graph)
c_confs = ClusterConfigurator(graph)

step_construct_clusters = True
step_visualize_task_variants_colored = True

# ------------------------------ END CONFIG ---------------------------- #

# CLUSTERING
if step_construct_clusters:
    tcm = TaskClusterModule(graph, c_confs.get_analysis_directory(), c_confs.get_min_variant_freq())
    cc = ClusterConstructor(gc.get_password(), graph, gc.get_case_label(), gc.get_actor_label())
    cc.remove_cluster_constructs()
    cc.construct_clusters(tcm.encode_and_cluster_specific(c_confs.get_cluster_min_variant_length(),
                                                          c_confs.get_manual_clusters(), c_confs.get_num_clusters(),
                                                          c_confs.get_cluster_include_remainder(),
                                                          c_confs.get_clustering_instance_description()))

# VISUALIZATION of TASK CLUSTER VARIANTS
if step_visualize_task_variants_colored:
    vv = VariantVisualizer(graph=graph, output_directory=c_confs.get_analysis_directory())
    vv.visualize_variants_colored()
