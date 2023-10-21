from GraphConfigurator import GraphConfigurator
from AnalysisConfigurator import AnalysisConfigurator
from modules.preprocessing import PreprocessSelector
from modules.ekg_construction.EventGraphConstructor import EventGraphConstructor
from modules.ekg_construction.HighLevelEventConstructor import HighLevelEventConstructor
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

# --------------------------- CONSTRUCTION ----------------------------- #
# IF STARTING FROM SCRATCH (without event graph constructed in neo4j)
# (1) create graph in Neo4j (with same password as specified in "graph_confs_old.py")
#     and allocate enough memory: set dbms.memory.heap.max_size=20G
# (2) install APOC plugin
# (3) specify path to import directory of neo4j database:
path_to_neo4j_import_directory = 'C:\\Users\\s111402\\.Neo4jDesktop\\relate-data\\dbmss\\' \
                                 'dbms-d43d0e64-67de-4c4b-8f5a-d167a6ca0de0\\import\\'
# (4) set "step_preprocess" and "step_create_event_graph" to true:
step_preprocess = False
step_construct_event_graph = True

# IF EVENT GRAPH IS ALREADY CONSTRUCTED:
# (5) set "step_construct_task_instances" to true to construct task instances:
step_construct_task_instances = True

step_add_task_instance_ids = True

# ------------------------------ END CONFIG ---------------------------- #

# [1.a] CONSTRUCTION
if step_preprocess:
    PreprocessSelector.get_preprocessor(graph, gc.get_filename(), gc.get_column_names(), gc.get_separator(),
                                        gc.get_timestamp_format(), path_to_neo4j_import_directory).preprocess()

if step_construct_event_graph:
    EventGraphConstructor(gc.get_password(), path_to_neo4j_import_directory, graph) \
        .construct()

if step_construct_task_instances:
    hle_constr = HighLevelEventConstructor(gc.get_password(), graph, gc.get_entity_labels(),
                                           gc.get_action_lifecycle_labels())
    hle_constr.construct()
    hle_constr.set_task_instance_ids()