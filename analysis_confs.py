#####################################################
############# EXPLANATION OF SETTINGS ###############
#####################################################

# SUBSET FILTER
min_variant_freq = {}

# CLUSTER SETTINGS
num_clusters = {}

cluster_min_variant_length = {}
manual_clusters = {}
cluster_include_remainder = {}
leftover_cluster = {}

decomposition_property = {}

# EVALUATION
tasks_overlap_test = {}

# SETTINGS FOR DFG
# inter-task dfg
dfg_exclude_clusters = {}
dfg_inter_show_threshold = {}
dfg_inter_weight_threshold = {}
dfg_inter_print_description = {}
dfg_inter_start_end_date = {}
dfg_inter_resources = {}

# inter-task dfg for concept drift comparison
dfg_inter_cd_comparison_start_end_dates = {}

# intra-tasks to visualize/mine
task_cluster_to_mine = {}

# intra-task dfg with resources overlaid
dfg_resource_inter_resources = {}
dfg_resource_inter_list_overlaid = {}
dfg_resource_inter_show_threshold_over = {}
dfg_resource_inter_show_threshold_under = {}
dfg_resource_inter_start_end_date = {}

# SETTINGS FOR ANALYSIS
# trend analysis


for graph in ["bpic2017_case_attr",
              "bpic2017_offer_id"]:
    min_variant_freq[graph] = 2
    num_clusters[graph] = 23
    cluster_min_variant_length[graph] = 2
    manual_clusters[graph] = {"m01": [16]}
    cluster_include_remainder[graph] = True
    leftover_cluster[graph] = 22

    decomposition_property[graph] = "offer_tracker"

    tasks_overlap_test[graph] = [8, 14]

    dfg_exclude_clusters[graph] = [3, 6]
    dfg_inter_show_threshold[graph] = 0
    dfg_inter_weight_threshold[graph] = 300
    dfg_inter_print_description[graph] = False
    # dfg_inter_start_end_date[graph] = ['2016-01-01', '2016-06-30']
    # dfg_inter_start_end_date[graph] = ['2016-08-01', '2017-02-01']
    dfg_inter_start_end_date[graph] = None
    dfg_inter_resources[graph] = None

    dfg_inter_cd_comparison_start_end_dates[graph] = [['2016-01-01', '2016-06-30'], ['2016-08-01', '2017-02-01']]

    task_cluster_to_mine[graph] = ["T02"]
    # task_cluster_to_mine[graph] = ""

    dfg_resource_inter_resources[graph] = ["User_29", "User_113"]
    dfg_resource_inter_list_overlaid[graph] = [["User_29"], ["User_113"]]
    dfg_resource_inter_show_threshold_over[graph] = 5
    dfg_resource_inter_show_threshold_under[graph] = 5
    dfg_resource_inter_start_end_date[graph] = ['2020-01-01', '2020-03-18']


for graph in ["bpic2017_susp_res"]:
    min_variant_freq[graph] = 10
    num_clusters[graph] = 21
    cluster_min_variant_length[graph] = 2
    manual_clusters[graph] = {"m01": [1, 25, 107, 138, 176, 185, 189, 192],
                              "m02": [2, 57, 87, 129, 179, 213, 216, 217],
                              "m03": [3, 33, 124, 139, 166, 194, 197, 211, 222, 238],
                              "m04": [7, 9, 45, 65, 150, 160, 225, 228, 233, 240],
                              "m05": [20],
                              "m06": [50, 78, 144, 196],
                              "m07": [56, 195, 268]}
    cluster_include_remainder[graph] = True
    leftover_cluster[graph] = "T05"

    decomposition_property[graph] = ""

    tasks_overlap_test[graph] = []

    dfg_exclude_clusters[graph] = []
    dfg_inter_show_threshold[graph] = 0
    dfg_inter_weight_threshold[graph] = 300
    dfg_inter_print_description[graph] = False
    # dfg_inter_start_end_date[graph] = ['2016-01-01', '2016-06-30']
    # dfg_inter_start_end_date[graph] = ['2016-08-01', '2017-02-01']
    dfg_inter_start_end_date[graph] = None
    dfg_inter_resources[graph] = None

    dfg_inter_cd_comparison_start_end_dates[graph] = [['2016-01-01', '2016-06-30'], ['2016-08-01', '2017-02-01']]

    task_cluster_to_mine[graph] = ["T02"]
    # task_cluster_to_mine[graph] = ""

    dfg_resource_inter_resources[graph] = ["User_29", "User_113"]
    dfg_resource_inter_list_overlaid[graph] = [["User_29"], ["User_113"]]
    dfg_resource_inter_show_threshold_over[graph] = 5
    dfg_resource_inter_show_threshold_under[graph] = 5
    dfg_resource_inter_start_end_date[graph] = ['2020-01-01', '2020-03-18']


for graph in ["operators"]:

    dfg_exclude_clusters[graph] = []
    dfg_inter_show_threshold[graph] = 25
    dfg_inter_weight_threshold[graph] = 50
    dfg_inter_print_description[graph] = False
    dfg_inter_start_end_date[graph] = None
    dfg_inter_resources[graph] = ["2"]
    # dfg_inter_resources[graph] = None

    dfg_inter_cd_comparison_start_end_dates[graph] = [['2016-01-01', '2016-06-30'], ['2016-08-01', '2017-02-01']]

    task_cluster_to_mine[graph] = ["T14"]

    dfg_resource_inter_resources[graph] = ["0"]
    # dfg_resource_inter_resources[graph] = ["0", "1", "2"]
    dfg_resource_inter_list_overlaid[graph] = [["0"]]
    # dfg_resource_inter_list_overlaid[graph] = [["0"], ["1"], ["2"]]
    dfg_resource_inter_show_threshold_over[graph] = 5
    dfg_resource_inter_show_threshold_under[graph] = 5
    dfg_resource_inter_start_end_date[graph] = ['2020-01-01', '2020-03-18']
    # dfg_resource_inter_start_end_date[graph] = ['2020-03-19', '2020-05-27']

    # analysis_trend[graph]
