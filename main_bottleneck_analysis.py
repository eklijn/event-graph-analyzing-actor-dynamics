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
qe = BottleneckAnalysisQueryEngine(gc.get_password(), gc.get_actor_label(), gc.get_case_label())
# c_confs = BottleNeckConfigurator(graph)

step_initial_analysis = False
step_analyze_workload_vs_task_duration = False

# ------------------------------ END CONFIG ---------------------------- #

if step_initial_analysis:
    initial_analysis.analyze_actor_edge_durations(qe)

if step_analyze_workload_vs_task_duration:
    initial_analysis.analyze_workload_vs_task_duration(qe, "T15")
