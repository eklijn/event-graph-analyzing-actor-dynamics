#####################################################
################ CLUSTER SETTINGS ###################
#####################################################

# SUBSET FILTER
min_variant_freq = {}

# CLUSTER SETTINGS
num_clusters = {}

cluster_min_variant_length = {}
manual_clusters = {}
cluster_include_remainder = {}
leftover_cluster = {}

for graph in ["bpic2017_susp_res"]:
    min_variant_freq[graph] = 10
    num_clusters[graph] = 21
    cluster_min_variant_length[graph] = 2
    manual_clusters[graph] = {"m01": [1, 25, 107, 139, 175, 186, 189, 191, 273, 295, 337, 346],
                              "m02": [2, 57, 87, 129, 180, 214, 217, 218, 324, 384],
                              "m03": [3, 33, 124, 138, 165, 194, 195, 212, 221, 240, 271, 310, 317, 319, 359],
                              "m04": [7, 9, 45, 65, 150, 160, 228, 229, 231, 239, 270, 279, 326],
                              "m05": [20, 299],
                              "m06": [50, 78, 145, 196],
                              "m07": [56, 197, 269, 378]}
    cluster_include_remainder[graph] = True
    leftover_cluster[graph] = "T05"

for graph in ["operators"]:
    min_variant_freq[graph] = 25
    num_clusters[graph] = 17
    cluster_min_variant_length[graph] = 2
    manual_clusters[graph] = {"m01": [8],
                              "m02": [54],
                              "m03": [75]}
    cluster_include_remainder[graph] = True
    leftover_cluster[graph] = ""
