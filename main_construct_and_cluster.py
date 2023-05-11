from GraphConfigurator import GraphConfigurator
from AnalysisConfigurator import AnalysisConfigurator
import PreprocessSelector
from constructors.EventGraphConstructor import EventGraphConstructor
from constructors.HighLevelEventConstructor import HighLevelEventConstructor
from constructors.ClusterConstructor import ClusterConstructor
from TaskClusterModule import TaskClusterModule
from VariantVisualizer import VariantVisualizer

# --------------------------- BEGIN CONFIG ----------------------------- #
# TO START:
# specify the name of the graph:
# graph = "operators"
graph = "bpic2017_susp_res"
# and configure all the settings related to this graph name in "graph_confs.py"
gc = GraphConfigurator(graph)
# and configure all analysis parameters in "analysis_confs.py"
ac = AnalysisConfigurator(graph)

# --------------------------- CONSTRUCTION ----------------------------- #
# IF STARTING FROM SCRATCH (without event graph constructed in neo4j)
# (1) create graph in Neo4j (with same password as specified in "graph_confs.py")
#     and allocate enough memory: set dbms.memory.heap.max_size=20G
# (2) install APOC plugin
# (3) specify path to import directory of neo4j database:
path_to_neo4j_import_directory = 'C:\\Users\\s111402\\.Neo4jDesktop\\relate-data\dbmss\\' \
                                 'dbms-75cf61d5-5ce3-4ffb-be62-b22a7cc7c5d8\\import\\'
# (4) set "step_preprocess" and "step_create_event_graph" to true:
step_preprocess = False
step_construct_event_graph = False

# IF EVENT GRAPH IS ALREADY CONSTRUCTED:
# (5) set "step_construct_high_level_events" to true to construct high level events:
# and set "step_construct_clusters" to true to perform clustering and construct clusters:
step_construct_high_level_events = False
step_construct_clusters = True

step_add_task_instance_ids = False
# step_visualize_task_variants_colored = False
step_visualize_task_variants_colored = True

# ------------------------------ END CONFIG ---------------------------- #

# [1.a] CONSTRUCTION
if step_preprocess:
    PreprocessSelector.get_preprocessor(graph, gc.get_filename(), gc.get_column_names(), gc.get_separator(),
                                        gc.get_timestamp_format(), path_to_neo4j_import_directory).preprocess()

if step_construct_event_graph:
    EventGraphConstructor(gc.get_password(), path_to_neo4j_import_directory, graph) \
        .construct()

if step_construct_high_level_events:
    hle_constr = HighLevelEventConstructor(gc.get_password(), graph, gc.get_entity_labels(),
                                           gc.get_action_lifecycle_labels())
    hle_constr.construct()
    hle_constr.set_task_instance_ids()

# [1.b] CLUSTERING
if step_construct_clusters:
    tcm = TaskClusterModule(graph, ac.get_analysis_directory(), ac.get_min_variant_freq())
    # tcm.evaluate_silhouette_score(2, range(20, 50))
    cc = ClusterConstructor(gc.get_password(), graph, gc.get_entity_labels(), gc.get_action_lifecycle_labels())
    cc.remove_cluster_constructs()
    # cc.construct_clusters(tcm.encode_and_cluster(ac.get_cluster_min_variant_length(), ac.get_num_clusters()))
    cc.construct_clusters(tcm.encode_and_cluster_specific(ac.get_cluster_min_variant_length(),
                                                          ac.get_manual_clusters(), ac.get_num_clusters(),
                                                          ac.get_cluster_include_remainder(),
                                                          ac.get_clustering_instance_description()))

# [2] VISUALIZATION of TASK CLUSTER VARIANTS
if step_visualize_task_variants_colored:
    vv = VariantVisualizer(graph=graph, analysis_directory=ac.get_analysis_directory())
    vv.visualize_variants_colored()
