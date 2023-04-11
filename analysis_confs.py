#####################################################
############# EXPLANATION OF SETTINGS ###############
#####################################################

# SUBSET FILTER
min_variant_freq = {}

# CLUSTER SETTINGS
num_clusters = {}

cluster_min_variant_length = {}
cluster_variants_to_exclude = {}
cluster_include_remainder = {}

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
    min_variant_freq[graph] = 10
    num_clusters[graph] = 20
    cluster_min_variant_length[graph] = 2
    cluster_variants_to_exclude[graph] = []
    cluster_include_remainder[graph] = False

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


for graph in ["operators"]:
    min_variant_freq[graph] = 25
    num_clusters[graph] = 17
    cluster_min_variant_length[graph] = 2
    cluster_variants_to_exclude[graph] = [8, 54, 75]
    cluster_include_remainder[graph] = True

    decomposition_property[graph] = "tbd"

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
