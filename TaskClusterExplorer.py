import os
import pandas as pd
from sklearn import metrics

import VariantEncoderFactory
from EventGraph import EventGraph
from GraphConfigurator import GraphConfigurator


class TaskClusterExplorer:
    def __init__(self, graph, analysis_directory):
        print("Initializing task cluster evaluator...")
        self.graph = graph
        self.analysis_directory = analysis_directory
        self.output_directory_variants_clustered = os.path.join(self.analysis_directory, "variant_visualizations")

        self.gc = GraphConfigurator(graph)
        self.eg = EventGraph(self.gc.get_password(), self.gc.get_entity_labels())

        self.df_variants_clustered = self.eg.query_cluster_variants()

    def get_variants_clustered(self):
        return self.df_variants_clustered

    def get_cluster_list(self):
        cluster_list = list(self.df_variants_clustered['cluster'].unique())
        return cluster_list

    def evaluate_silhouette_task_cluster_overlap(self, cluster_pair):
        e = VariantEncoderFactory.get_variant_encoder(self.gc.get_name_data_set())
        df_variants_to_evaluate = self.df_variants_clustered[self.df_variants_clustered['cluster'].str.get(0) == "T"].copy()
        df_variants_encoded = e.encode(df_variants_to_evaluate)
        df_variants_to_evaluate.loc[:, 'cluster'] = df_variants_to_evaluate['cluster'].str.lstrip(
            "T").astype('int')
        df_variants_to_evaluate.loc[:, 'cluster_tasks_merged'] = df_variants_to_evaluate['cluster']
        df_variants_to_evaluate.loc[
            df_variants_to_evaluate['cluster_tasks_merged'] == cluster_pair[0], 'cluster_tasks_merged'] = \
            cluster_pair[1]
        s_score_tasks_merged = metrics.silhouette_score(df_variants_encoded.values,
                                                        df_variants_to_evaluate['cluster_tasks_merged'].values)
        print(f"Silhouette score tasks merged: {s_score_tasks_merged}")
        s_score_original = metrics.silhouette_score(df_variants_encoded.values,
                                                    df_variants_to_evaluate['cluster'].values)
        print(f"Silhouette score original: {s_score_original}")

    def common_actions_per_task_cluster_to_csv(self):
        cluster_list = list(self.df_variants_clustered['cluster'].unique())
        df_common_actions_per_cluster = pd.DataFrame(index=cluster_list, columns=['common_actions'])
        for cluster in cluster_list:
            df_cluster = self.df_variants_clustered[self.df_variants_clustered['cluster'] == cluster].copy()
            variants_in_cluster = list(df_cluster['path'])
            common_actions = list(set(variants_in_cluster[0]).intersection(*variants_in_cluster))
            df_common_actions_per_cluster.loc[cluster, 'common_actions'] = common_actions
        df_common_actions_per_cluster = df_common_actions_per_cluster.sort_index()
        df_common_actions_per_cluster.to_csv(f"{self.analysis_directory}\\variant_common_actions_per_cluster.csv")
