from GraphConfigurator import GraphConfigurator
# from modules.bottleneck_analysis.BottleNeckConfigurator import BottleNeckConfigurator
from modules.bottleneck_analysis import initial_analysis
from query_engines.bottleneck_analysis_qe import BottleneckAnalysisQueryEngine


# --------------------------- BEGIN CONFIG ----------------------------- #
# TO START:
# specify the name of the graph:
graph = "bpic2017_susp_res"
# and configure all the settings related to this graph name in "graph_confs_old.py"
gc = GraphConfigurator(graph)
qe = BottleneckAnalysisQueryEngine(gc.get_password())
# c_confs = BottleNeckConfigurator(graph)

step_initial_analysis = True

# ------------------------------ END CONFIG ---------------------------- #

# CLUSTERING
if step_initial_analysis:
    initial_analysis.analyze_actor_edge_durations(qe)
