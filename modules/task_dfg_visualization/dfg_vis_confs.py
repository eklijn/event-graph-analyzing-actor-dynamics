#####################################################
############ DFG VISUALIZATION SETTINGS #############
#####################################################

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


for graph in ["bpic2017_case_attr",
              "bpic2017_offer_id"]:

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