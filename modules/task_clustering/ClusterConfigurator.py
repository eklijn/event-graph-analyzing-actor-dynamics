from modules.task_clustering import cluster_confs


class ClusterConfigurator:
    def __init__(self, graph):
        self.graph = graph
        self.min_variant_freq = cluster_confs.min_variant_freq[self.graph]

        self.num_clusters = cluster_confs.num_clusters[self.graph]
        self.cluster_min_variant_length = cluster_confs.cluster_min_variant_length[self.graph]
        self.manual_clusters = cluster_confs.manual_clusters[self.graph]
        self.cluster_include_remainder = cluster_confs.cluster_include_remainder[self.graph]
        self.leftover_cluster = cluster_confs.leftover_cluster[self.graph]

        self.clustering_instance_description = f"V{self.min_variant_freq}_C{self.num_clusters}_" \
                                               f"L{self.cluster_min_variant_length}"

        if self.manual_clusters != "":
            self.clustering_instance_description += "_manual"

        if self.cluster_include_remainder:
            self.clustering_instance_description += "_Rinc"
        else:
            self.clustering_instance_description += "_Rexc"

    def get_analysis_directory(self):
        analysis_directory = f"modules\\task_clustering\\output\\{self.graph}\\{self.clustering_instance_description}"
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

    def get_clustering_instance_description(self):
        return self.clustering_instance_description
