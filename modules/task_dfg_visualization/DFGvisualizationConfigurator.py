import dfg_vis_confs


class DFGVisualizationConfigurator:
    def __init__(self, graph):
        self.graph = graph
        self.dfg_exclude_clusters = dfg_vis_confs.dfg_exclude_clusters[self.graph]
        self.dfg_inter_show_threshold = dfg_vis_confs.dfg_inter_show_threshold[self.graph]
        self.dfg_inter_weight_threshold = dfg_vis_confs.dfg_inter_weight_threshold[self.graph]
        self.dfg_inter_print_description = dfg_vis_confs.dfg_inter_print_description[self.graph]
        self.dfg_inter_start_end_date = dfg_vis_confs.dfg_inter_start_end_date[self.graph]
        self.dfg_inter_resources = dfg_vis_confs.dfg_inter_resources[self.graph]

        self.dfg_inter_cd_comparison_start_end_dates = dfg_vis_confs.dfg_inter_cd_comparison_start_end_dates[self.graph]

        self.task_cluster_to_mine = dfg_vis_confs.task_cluster_to_mine[self.graph]

        self.dfg_resource_inter_resources = dfg_vis_confs.dfg_resource_inter_resources[self.graph]
        self.dfg_resource_inter_list_overlaid = dfg_vis_confs.dfg_resource_inter_list_overlaid[self.graph]
        self.dfg_resource_inter_show_threshold_over = dfg_vis_confs.dfg_resource_inter_show_threshold_over[self.graph]
        self.dfg_resource_inter_show_threshold_under = dfg_vis_confs.dfg_resource_inter_show_threshold_under[self.graph]
        self.dfg_resource_inter_start_end_date = dfg_vis_confs.dfg_resource_inter_start_end_date[self.graph]

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
