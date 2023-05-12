import analysis_confs


class AnalysisConfigurator:
    def __init__(self, graph):
        self.graph = graph
        self.min_variant_freq = analysis_confs.min_variant_freq[self.graph]

        self.num_clusters = analysis_confs.num_clusters[self.graph]
        self.cluster_min_variant_length = analysis_confs.cluster_min_variant_length[self.graph]
        self.manual_clusters = analysis_confs.manual_clusters[self.graph]
        self.cluster_include_remainder = analysis_confs.cluster_include_remainder[self.graph]
        self.leftover_cluster = analysis_confs.leftover_cluster[self.graph]
        self.decomposition_property = analysis_confs.decomposition_property[self.graph]
        self.tasks_overlap_test = analysis_confs.tasks_overlap_test[self.graph]
        # self.merged_task_cluster_to_mine = analysis_confs.merged_task_cluster_to_mine[self.graph]

        self.clustering_instance_description = f"V{self.min_variant_freq}_C{self.num_clusters}_" \
                                               f"L{self.cluster_min_variant_length}"

        if self.manual_clusters is not "":
            self.clustering_instance_description += "_manual"

        if self.cluster_include_remainder:
            self.clustering_instance_description += "_Rinc"
        else:
            self.clustering_instance_description += "_Rexc"

        self.dfg_exclude_clusters = analysis_confs.dfg_exclude_clusters[self.graph]
        self.dfg_inter_show_threshold = analysis_confs.dfg_inter_show_threshold[self.graph]
        self.dfg_inter_weight_threshold = analysis_confs.dfg_inter_weight_threshold[self.graph]
        self.dfg_inter_print_description = analysis_confs.dfg_inter_print_description[self.graph]
        self.dfg_inter_start_end_date = analysis_confs.dfg_inter_start_end_date[self.graph]
        self.dfg_inter_resources = analysis_confs.dfg_inter_resources[self.graph]

        self.dfg_inter_cd_comparison_start_end_dates = analysis_confs.dfg_inter_cd_comparison_start_end_dates[self.graph]

        self.task_cluster_to_mine = analysis_confs.task_cluster_to_mine[self.graph]

        self.dfg_resource_inter_resources = analysis_confs.dfg_resource_inter_resources[self.graph]
        self.dfg_resource_inter_list_overlaid = analysis_confs.dfg_resource_inter_list_overlaid[self.graph]
        self.dfg_resource_inter_show_threshold_over = analysis_confs.dfg_resource_inter_show_threshold_over[self.graph]
        self.dfg_resource_inter_show_threshold_under = analysis_confs.dfg_resource_inter_show_threshold_under[self.graph]
        self.dfg_resource_inter_start_end_date = analysis_confs.dfg_resource_inter_start_end_date[self.graph]

    def get_analysis_directory(self):
        analysis_directory = f"F:\\analysis_output\\{self.graph}\\{self.clustering_instance_description}"
        # analysis_directory = f"output\\{self.graph}\\{self.clustering_instance_description}"
        return analysis_directory

    def get_min_variant_freq(self):
        return self.min_variant_freq

    def get_num_clusters(self):
        return self.num_clusters

    def get_cluster_min_variant_length(self):
        return self.cluster_min_variant_length

    def get_manual_clusters(self):
        return self.manual_clusters

    def get_cluster_include_remainder(self):
        return self.cluster_include_remainder

    def get_leftover_cluster(self):
        return self.leftover_cluster

    def get_decomposition_property(self):
        return self.decomposition_property

    def get_tasks_overlap_test_integer(self):
        return self.tasks_overlap_test

    def get_tasks_overlap_test_string(self):
        tasks_overlap_test_string = []
        tasks_overlap_test_string.append(f"T{str(self.tasks_overlap_test[0]).zfill(2)}")
        tasks_overlap_test_string.append(f"T{str(self.tasks_overlap_test[1]).zfill(2)}")
        return tasks_overlap_test_string

    def get_clustering_instance_description(self):
        return self.clustering_instance_description

    def get_dfg_exclude_clusters(self):
        return self.dfg_exclude_clusters

    def get_dfg_inter_show_threshold(self):
        return self.dfg_inter_show_threshold

    def get_dfg_inter_weight_threshold(self):
        return self.dfg_inter_weight_threshold

    def get_dfg_inter_print_description(self):
        return self.dfg_inter_print_description

    def get_dfg_inter_start_end_date(self):
        return self.dfg_inter_start_end_date

    def get_dfg_inter_resources(self):
        return self.dfg_inter_resources

    def get_dfg_inter_cd_comparison_start_end_dates(self):
        return self.dfg_inter_cd_comparison_start_end_dates

    def get_task_cluster_to_mine(self):
        return self.task_cluster_to_mine

    def get_dfg_resource_inter_resources(self):
        return self.dfg_resource_inter_resources

    def get_dfg_resource_inter_list_overlaid(self):
        return self.dfg_resource_inter_list_overlaid

    def get_dfg_resource_inter_show_threshold_over(self):
        return self.dfg_resource_inter_show_threshold_over

    def get_dfg_resource_inter_show_threshold_under(self):
        return self.dfg_resource_inter_show_threshold_under

    def get_dfg_resource_inter_start_end_date(self):
        return self.dfg_resource_inter_start_end_date
