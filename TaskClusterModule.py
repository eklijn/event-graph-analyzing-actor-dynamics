import os
import pandas as pd
from os import path
import matplotlib.pyplot as plt
from sklearn import metrics
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering

from GraphConfigurator import GraphConfigurator
from EventGraph import EventGraph
import VariantEncoderFactory


class TaskClusterModule:
    def __init__(self, graph, analysis_directory, min_variant_freq):
        print("Initializing task cluster module...")
        self.graph = graph
        self.analysis_directory = analysis_directory
        self.min_variant_freq = min_variant_freq
        self.affinity = "euclidean"
        self.linkage = "ward"

        self.meta_directory = f"meta-output\\"
        self.gc = GraphConfigurator(graph)
        self.eg = EventGraph(self.gc.get_password(), self.gc.get_entity_labels())

        if path.exists(f"{self.meta_directory}variants_{graph}_F{min_variant_freq}.pkl"):
            self.df_variants = pd.read_pickle(f"{self.meta_directory}variants_{graph}_F{min_variant_freq}.pkl")
        else:
            self.df_variants = self.eg.query_variants(min_frequency=min_variant_freq)
            self.df_variants.to_pickle(
                f"{self.meta_directory}variants_{graph}_F{min_variant_freq}.pkl")

    def encode_and_cluster(self, min_variant_length, num_clusters):
        if path.exists(
                f"{self.meta_directory}variants_clustered_{self.graph}_F{self.min_variant_freq}_C{num_clusters}_L{min_variant_length}.pkl"):
            df_variants_clustered = pd.read_pickle(
                f"{self.meta_directory}variants_clustered_{self.graph}_F{self.min_variant_freq}_C{num_clusters}_L{min_variant_length}.pkl")
        else:
            e = VariantEncoderFactory.get_variant_encoder(self.gc.get_name_data_set())
            df_variants_to_cluster = self.df_variants[self.df_variants['path_length'] >= min_variant_length]
            df_variants_encoded = e.encode(df_variants_to_cluster)
            df_clusters = cluster(df_variants_encoded, num_clusters, self.affinity, self.linkage)
            df_variants_clustered = pd.concat([self.df_variants, df_clusters], axis=1)
            os.makedirs(self.meta_directory, exist_ok=True)
            df_variants_clustered.to_pickle(
                f"{self.meta_directory}variants_clustered_{self.graph}_F{self.min_variant_freq}_C{num_clusters}_L{min_variant_length}.pkl")
        return df_variants_clustered

    def encode_and_cluster_specific(self, min_variant_length, manual_clusters, num_clusters,
                                    include_remainder, clustering_instance_description):
        if path.exists(f"{self.meta_directory}variants_clustered_{self.graph}_{clustering_instance_description}.pkl"):
            df_variants_clustered = pd.read_pickle(
                f"{self.meta_directory}variants_clustered_{self.graph}_{clustering_instance_description}.pkl")
        else:
            e = VariantEncoderFactory.get_variant_encoder(self.gc.get_name_data_set())
            manually_clustered_variants = [item for sublist in list(manual_clusters.values()) for item in sublist]
            df_variants_to_cluster = self.df_variants[self.df_variants['path_length'] >= min_variant_length]
            # df_variants_to_cluster = self.df_variants[
            #     (self.df_variants['path_length'] >= min_variant_length) & (
            #         ~self.df_variants['ID'].isin(manually_clustered_variants))]
            df_variants_encoded = e.encode(df_variants_to_cluster)
            df_clusters = cluster(df_variants_encoded, num_clusters, self.affinity, self.linkage)
            df_variants_clustered = pd.concat([self.df_variants, df_clusters], axis=1)
            A_id = 1
            for index, row in df_variants_clustered.iterrows():
                if row['ID'] in manually_clustered_variants:
                    variant_key = \
                    [key for key, corresponding_list in manual_clusters.items() if row['ID'] in corresponding_list][0]
                    df_variants_clustered.loc[index, 'cluster'] = variant_key
                elif pd.isna(row['cluster']):
                    if include_remainder:
                        if row['path_length'] == 1:
                            df_variants_clustered.loc[index, 'cluster'] = f"A{str(A_id).zfill(2)}"
                            A_id += 1
                else:
                    df_variants_clustered.loc[index, 'cluster'] = f"T{str(int(row['cluster'])).zfill(2)}"

            # self.df_variants_clustered.rename(columns={"cluster": f"{self.clustering_instance_description}"})
            os.makedirs(self.meta_directory, exist_ok=True)
            df_variants_clustered.to_pickle(
                f"{self.meta_directory}variants_clustered_{self.graph}_{clustering_instance_description}.pkl")
        return df_variants_clustered

    def evaluate_silhouette_score(self, min_variant_length, list_num_clusters):
        e = VariantEncoderFactory.get_variant_encoder(self.gc.get_name_data_set())
        df_variants_to_cluster = self.df_variants[self.df_variants['path_length'] >= min_variant_length]
        df_variants_encoded = e.encode(df_variants_to_cluster)
        for num_clusters in list_num_clusters:
            silhouette_score = get_silhouette_score(df_variants_encoded, num_clusters, self.affinity, self.linkage)
            print(f"Number of clusters: {num_clusters} \t\t Silhouette score: {silhouette_score}")

    def evaluate_silhouette_score_specific(self, min_variant_length, extra_variants_to_exclude, list_num_clusters):
        e = VariantEncoderFactory.get_variant_encoder(self.gc.get_name_data_set())
        df_variants_to_cluster = self.df_variants[
            (self.df_variants['path_length'] >= min_variant_length) & (
                ~self.df_variants['ID'].isin(extra_variants_to_exclude))]
        df_variants_encoded = e.encode(df_variants_to_cluster)
        for num_clusters in list_num_clusters:
            silhouette_score = get_silhouette_score(df_variants_encoded, num_clusters, self.affinity, self.linkage)
            print(f"Number of clusters: {num_clusters} \t\t Silhouette score: {silhouette_score}")

    def evaluate_dendrogram(self, min_variant_length, extra_variants_to_exclude):
        e = VariantEncoderFactory.get_variant_encoder(self.gc.get_name_data_set())
        df_variants_to_cluster = self.df_variants[
            (self.df_variants['path_length'] >= min_variant_length) & (
                ~self.df_variants['ID'].isin(extra_variants_to_exclude))]
        df_variants_encoded = e.encode(df_variants_to_cluster)
        fig = plt.figure(figsize=(25, 10))
        dn = dendrogram(linkage(df_variants_encoded.values, 'ward'))
        plt.show()


def cluster(df_variants_encoded, num_clusters, affinity, linkage):
    clusters = AgglomerativeClustering(n_clusters=num_clusters, affinity=affinity, linkage=linkage) \
        .fit_predict(df_variants_encoded.values)
    index = list(df_variants_encoded.index.values)
    df_clusters = pd.DataFrame(index=index, data={'cluster': clusters})
    return df_clusters


def get_silhouette_score(df_variants_encoded, num_clusters, affinity, linkage):
    clusters = AgglomerativeClustering(n_clusters=num_clusters, affinity=affinity, linkage=linkage) \
        .fit_predict(df_variants_encoded.values)
    s_score = metrics.silhouette_score(df_variants_encoded.values, clusters)
    return s_score
