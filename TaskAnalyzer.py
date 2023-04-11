import os
import numpy as np
import pandas as pd
from os import path
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
import dataframe_image as dfi
import statsmodels.api as sm
from statistics import mean
import math

from EventGraph import EventGraph
from GraphConfigurator import GraphConfigurator

plot_colors_variants = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c']
plot_colors_variants_appendix = ['#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928']
plot_colors_variants_appendix = ['#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#10486e', '#8c0e0f']
plot_colors_resources = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02']


class TaskAnalyzer:
    def __init__(self, graph, analysis_directory, clustering_instance_description):
        print("Initializing task analyzer...")
        self.graph = graph
        self.analysis_directory = analysis_directory
        self.clustering_instance_description = clustering_instance_description

        self.output_directory_plots = os.path.join(self.analysis_directory, "plots")
        self.meta_directory = f"meta-output\\variants\\"

        self.gc = GraphConfigurator(graph)
        self.eg = EventGraph(self.gc.get_password(), self.gc.get_entity_labels())

        # if path.exists(f"{self.meta_directory}variants_{graph}_{min_variant_freq}.pkl"):
        #     self.df_variants = pd.read_pickle(f"{self.meta_directory}variants_{graph}_{min_variant_freq}.pkl")
        # else:
        #     self.df_variants = self.eg.query_variant_variants_and_frequencies(min_frequency=min_variant_freq)
        #
        self.df_variants_clustered = pd.read_pickle(
            f"{self.meta_directory}variants_{self.graph}_{self.clustering_instance_description}.pkl")


    ######################################################
    ################### TREND ANALYSIS ###################
    ######################################################

    def plot_variant_trends_per_cluster(self, clusters):
        for cluster in clusters:
            variant_ids_in_cluster = self.df_variants_clustered.loc[
                self.df_variants_clustered['cluster'] == cluster, 'ID'].tolist()

            df_tasks_per_date = self.eg.query_task_instances_per_date_from_variant_ids(variant_ids_in_cluster)
            nr_columns = 5
            total_plots = len(variant_ids_in_cluster)
            if total_plots < nr_columns:
                nr_columns = total_plots
            nr_rows = int(math.ceil(total_plots / nr_columns))
            height = nr_rows * 4
            width = nr_columns * 6
            current_plot = 0
            fig, ax = plt.subplots(ncols=nr_columns, nrows=nr_rows, figsize=(width, height),
                                   constrained_layout=True, sharex=True, sharey=True)
            for row in range(0, nr_rows):
                for column in range(0, nr_columns):
                    if nr_columns == 1:
                        current_ax = ax
                    elif nr_rows == 1:
                        current_ax = ax[column]
                    else:
                        current_ax = ax[row, column]
                    if current_plot < total_plots:
                        current_task_column = df_tasks_per_date.iloc[:, current_plot].copy()
                        current_task_column.plot(ax=current_ax, color='tab:blue', xlabel="", fontsize=12, legend=True)
                        current_plot += 1
                    else:
                        current_ax.axis('off')
            plt.savefig(f"{self.analysis_directory}\\trend_analysis\\cluster_{cluster}.png")

    def plot_variant_trends_paper(self):
        variant_sets = [[1, 2], [3, 4], [5, 6]]
        ax_titles = ["C8", "C11", "C14"]
        x_labels = ['Jan\n2016', '', 'Mar', '', 'May', '', 'Jul', '', 'Sep', '', 'Nov', '', 'Jan\n2017', '']
        # x_labels = ['Jan\n2016', '', '', 'Apr', '', '', 'Jul', '', '', 'Oct', '', '', 'Jan\n2017', '']
        fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(13, 4), sharex=True)
        sigma = 0.1
        df_task_instances_per_date = self.eg.query_task_instances_per_date_from_variant_ids([25, 37, 4, 9, 1, 3])
        df_task_instances_per_date = df_task_instances_per_date.rename(
            columns={25: 'V1', 37: 'V2', 4: 'V3', 9: 'V4', 1: 'V5', 3: 'V6'})
        # df_task_instances_per_date = df_task_instances_per_date.rename(columns={25: 1, 37: 2, 4: 3, 9: 4, 1: 5, 3: 6})

        for index, variant_set in enumerate(variant_sets):
            current_ax = ax[index]
            for variant in variant_set:
                variant_str = f"V{variant}"
                df_task_instances_per_date[variant_str] = gaussian_filter1d(
                    df_task_instances_per_date[variant_str], sigma=sigma, mode='nearest')
                df_task_instances_per_date[variant_str] \
                    .plot(ax=current_ax, color=plot_colors_variants[variant - 1], legend=True)

            current_ax.legend(fontsize=16)
            current_ax.set_title(ax_titles[index], fontsize=18, fontweight='bold')
            current_ax.set_xticklabels(x_labels, fontsize=16)
            current_ax.tick_params(axis='y', labelsize=16)
            # if index == 1:
            #     current_ax.set_xlabel('Date', size=18)
            # else:
            #     current_ax.set_xlabel('', size=18)
            current_ax.set_xlabel('', size=18)
            # if index == 0:
            #     current_ax.set_ylabel('Number of executions', size=18)
        plt.tight_layout()
        labels = current_ax.get_xticklabels()
        plt.savefig(f"{self.analysis_directory}\\trend_analysis\\PAPER_concept_drift_clusters_8_11_14.png")
        plt.show()

    def plot_variant_trends_paper_appendix(self):
        variant_sets = [[7, 8], [9, 10], [11], [12]]
        ax_titles = ["C7", "C12", "C8", "C14"]
        x_labels = ['Jan\n2016', '', 'Mar', '', 'May', '', 'Jul', '', 'Sep', '', 'Nov', '', 'Jan\n2017', '']
        # x_labels = ['Jan\n2016', '', '', 'Apr', '', '', 'Jul', '', '', 'Oct', '', '', 'Jan\n2017', '']
        fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(10, 8), sharex=True)
        sigma = 0.1
        df_task_instances_per_date = self.eg.query_task_instances_per_date_from_variant_ids([27, 29, 8, 34, 49, 22])
        df_task_instances_per_date = df_task_instances_per_date.rename(
            columns={27: 'V7', 29: 'V8', 8: 'V9', 34: 'V10', 49: 'V11', 22: 'V12'})
        # df_task_instances_per_date = df_task_instances_per_date.rename(columns={27: 7, 29: 8, 8: 9, 34: 10, 49: 11, 22: 12})

        plot_nr = 0
        ax_nr = 0
        for current_ax in ax.ravel():
            for variant in variant_sets[ax_nr]:
                variant_str = f"V{variant}"
                df_task_instances_per_date[variant_str] = gaussian_filter1d(
                    df_task_instances_per_date[variant_str], sigma=sigma, mode='nearest')
                df_task_instances_per_date[variant_str] \
                    .plot(ax=current_ax, color=plot_colors_variants_appendix[plot_nr], legend=True)
                plot_nr += 1

                current_ax.legend(fontsize=16)
                current_ax.set_title(ax_titles[ax_nr], fontsize=18, fontweight='bold')
                current_ax.set_xticklabels(x_labels, fontsize=16)
                current_ax.tick_params(axis='y', labelsize=16)
                current_ax.tick_params(axis='x', labelsize=16)
                current_ax.set_xlabel('', size=18)
                # current_ax.set_xlabel('Date', size=18)
                # if ax_nr == 0 or ax_nr == 2:
                #     current_ax.set_ylabel('Number of executions', size=18)
            ax_nr += 1

        labels = current_ax.get_xticklabels()
        plt.savefig(f"{self.analysis_directory}\\trend_analysis\\PAPER_APP_concept_drift_clusters_7_12_8_14.png")
        plt.show()

    def plot_variant_trends_variant_subset(self, variant_ids, line_styles, resources):
        fig, ax = plt.subplots(figsize=(16, 8))
        sigma = 0.1
        file_name_resources = ""
        file_name_variant_ids = ""
        for r_index, resource in enumerate(resources):
            file_name_resources += f"_{resource[5:]}"
            for p_index, variant_id in enumerate(variant_ids):
                freq = self.eg.query_resource_frequency_from_variant_id(resource, variant_id)
                file_name_variant_ids += f"_{variant_id}"
                if freq != 0:
                    df_task_instances_per_date = self.eg. \
                        query_task_instances_per_date_per_resource_from_variant_id(variant_id, resource)
                    df_task_instances_per_date[f"variant_{variant_id}_{resource}"] = gaussian_filter1d(
                        df_task_instances_per_date[f"variant_{variant_id}_{resource}"], sigma=sigma, mode='nearest')
                    # df_task_instances_per_date[f"variant_{variant_id}_{resource}"] = \
                    #     df_task_instances_per_date[f"variant_{variant_id}_{resource}"].rolling(sigma).median()
                    df_task_instances_per_date[f"variant_{variant_id}_{resource}"] \
                        .plot(ax=ax, linestyle=line_styles[p_index], color=plot_colors_resources[r_index], legend=True)
        ax.set_title(f"Trends of elementary task executions {variant_ids} for resources {resources}", size=16,
                     weight='bold')
        ax.set_xlabel('Date', size=12)
        ax.set_ylabel('Number of executions', size=12)
        plt.savefig(f"{self.output_directory_plots}\\variant_trend_P{file_name_variant_ids}_R{file_name_resources}.png")
        plt.show()
        os.makedirs(self.output_directory_plots, exist_ok=True)

    def plot_variant_trends_variants_resources_paper(self):
        resources = ["User_29", "User_30", "User_68", "User_100"]
        x_labels = ['Jan\n2016', 'Mar', 'May', 'Jul', 'Sep', 'Nov', 'Jan\n2017']
        # ax_titles = ["V7", "V8"]
        ax_titles = ["V3", "V4"]
        # variant_ids = [27, 29]
        variant_ids = [4, 9]
        unit = 'week'
        # unit = 'month'
        fig, ax = plt.subplots(ncols=len(variant_ids), nrows=1, figsize=(9.5, 4), sharex=True, )
        sigma = 1.5
        file_name_resources = ""
        file_name_variant_ids = ""
        for p_index, variant_id in enumerate(variant_ids):
            if len(variant_ids) == 1:
                current_ax = ax
            else:
                current_ax = ax[p_index]
            file_name_variant_ids += f"_{variant_id}"
            file_name_resources = ""
            for r_index, resource in enumerate(resources):
                file_name_resources += f"_{resource[5:]}"
                resource_str = f"{resource[0]}{resource[5:]}"
                freq = self.eg.query_resource_frequency_from_variant_id(resource, variant_id)
                if freq != 0:
                    df_task_instances_per_date = self.eg. \
                        query_task_instances_per_date_per_resource_from_variant_id(variant_id, resource, unit)
                    df_task_instances_per_date = df_task_instances_per_date.rename(
                        columns={resource: resource_str})
                    df_task_instances_per_date[resource_str] = gaussian_filter1d(
                        df_task_instances_per_date[resource_str], sigma=sigma, mode='nearest')
                    df_task_instances_per_date[resource_str] \
                        .plot(ax=current_ax, color=plot_colors_resources[r_index], legend=True)
            current_ax.tick_params(axis='y', labelsize=16)
            current_ax.legend(fontsize=12)
            current_ax.set_xticklabels(x_labels, rotation=0, fontsize=16, horizontalalignment='center')
            current_ax.set_title(ax_titles[p_index], size=18, fontweight='bold')
            # current_ax.set_xlabel('Date', size=18)
            current_ax.set_xlabel('', size=18)
            # if p_index == 0:
            #     current_ax.set_ylabel('Number of executions', size=18)
        plt.tight_layout()
        plt.draw()
        labels = current_ax.get_xticklabels()
        plt.savefig(
            f"{self.analysis_directory}\\trend_analysis\\PAPER_resources_{file_name_variant_ids}_R{file_name_resources}.png")
        plt.show()

    def plot_variant_trends_variants_resources(self, variant_ids, resources):
        fig, ax = plt.subplots(ncols=1, nrows=len(variant_ids), figsize=(6, (len(variant_ids) * 4)),
                               constrained_layout=True, sharex=True, )
        sigma = 1
        file_name_resources = ""
        file_name_variant_ids = ""
        for p_index, variant_id in enumerate(variant_ids):
            if len(variant_ids) == 1:
                current_ax = ax
            else:
                current_ax = ax[p_index]
            file_name_variant_ids += f"_{variant_id}"
            file_name_resources = ""
            for r_index, resource in enumerate(resources):
                file_name_resources += f"_{resource[5:]}"
                freq = self.eg.query_resource_frequency_from_variant_id(resource, variant_id)
                if freq != 0:
                    df_task_instances_per_date = self.eg. \
                        query_task_instances_per_date_per_resource_from_variant_id(variant_id, resource)
                    df_task_instances_per_date[f"{resource}"] = gaussian_filter1d(
                        df_task_instances_per_date[f"{resource}"], sigma=sigma, mode='nearest')
                    df_task_instances_per_date[f"{resource}"] \
                        .plot(ax=current_ax, color=self.plot_colors[r_index], legend=True)
            current_ax.set_title(f"variant {variant_id}", size=12)
            current_ax.set_xlabel('Date', size=12)
            current_ax.set_ylabel('Number of executions', size=12)
        plt.savefig(f"{self.analysis_directory}\\trend_analysis\\P{file_name_variant_ids}_R{file_name_resources}.png")
        plt.show()

    ######################################################
    ############# HANDOVER OF WORK ANALYSIS ##############
    ######################################################

    # def plot_handover_of_work_durations(self, ):

    ######################################################
    ############## CASE ATTRIBUTE ANALYSIS ###############
    ######################################################

    def plot_heatmap_case_attributes_per_cluster(self, case_attribute, clusters=""):
        if clusters == "":
            clusters = range(0, self.num_clusters)

        case_attribute_name = case_attribute[0]
        case_attribute_values = case_attribute[1]
        column_tuples = []
        for case_attribute_value in case_attribute_values:
            column_tuples.append((case_attribute_name, case_attribute_value[0]))

        for cluster in clusters:
            variant_ids_in_cluster = self.df_variants_clustered.loc[
                self.df_variants_clustered['cluster'] == cluster, 'ID'].tolist()
            df_cluster_stats = pd.DataFrame(index=variant_ids_in_cluster,
                                            columns=pd.MultiIndex.from_tuples(column_tuples))

            for variant_id in variant_ids_in_cluster:
                for case_attribute_value in case_attribute_values:
                    frequency = self.eg.query_variant_frequency_subset_filter(variant_id, case_attribute_value[1])
                    df_cluster_stats.loc[variant_id, (case_attribute_name, case_attribute_value[0])] = int(frequency)

            df_cluster_stats.sort_index(inplace=True)
            df_cluster_stats.columns.names = ["Case attribute", "Value"]
            df_cluster_stats.index.names = ["variant"]
            df_cluster_stats_transposed = df_cluster_stats.transpose()
            df_cluster_stats_transposed_for_log = df_cluster_stats_transposed.applymap(lambda x: 1 if x == 0 else x)
            gmap = np.log(df_cluster_stats_transposed_for_log.astype(float))

            df_cluster_stats_style = df_cluster_stats_transposed.apply(pd.to_numeric).style.background_gradient(
                cmap='Blues', axis=None, gmap=gmap)
            df_cluster_stats_style.format('{:.0f}').set_properties(
                **{'font-size': '11pt', 'border-color': 'black', 'border-style': 'solid', 'border-width': '1px',
                   'border-collapse': 'collapse'})
            dfi.export(df_cluster_stats_style, f"{self.analysis_directory}\\case_attribute_analysis\\"
                                               f"inter_cluster\\heatmap_{case_attribute_name}_cluster{cluster}.png")

    def plot_heatmap_case_attributes_across_groups(self, group_type, groups_to_compare, case_attribute):
        str_groups = f"{str(groups_to_compare[0])}"
        for group in groups_to_compare[1:]:
            str_groups += f"_{str(group)}"
        case_attribute_name = case_attribute[0]
        case_attribute_values = case_attribute[1]
        column_tuples = []
        for case_attribute_value in case_attribute_values:
            column_tuples.append((case_attribute_name, case_attribute_value[0]))
        index = [str(group) for group in groups_to_compare]

        df_group_stats = pd.DataFrame(index=index, columns=pd.MultiIndex.from_tuples(column_tuples))

        for group in groups_to_compare:
            for case_attribute_value in case_attribute_values:
                variant_ids_in_group = []
                if group_type == 'Cluster':
                    if isinstance(group, list):
                        for g in group:
                            variant_ids_in_group.extend(self.df_variants_clustered
                                                        .loc[self.df_variants_clustered['cluster'] == g, 'ID']
                                                        .tolist())
                    else:
                        variant_ids_in_group.extend(self.df_variants_clustered
                                                    .loc[self.df_variants_clustered['cluster'] == group, 'ID']
                                                    .tolist())
                elif group_type == 'variant':
                    if isinstance(group, list):
                        variant_ids_in_group = group
                    else:
                        variant_ids_in_group = [group]

                group_frequency = 0
                for variant_id in variant_ids_in_group:
                    variant_frequency = self.eg.query_variant_frequency_subset_filter(variant_id,
                                                                                      case_attribute_value[1])
                    group_frequency += int(variant_frequency)
                df_group_stats.loc[str(group), (case_attribute_name, case_attribute_value[0])] = int(group_frequency)
        df_group_stats.sort_index(inplace=True)
        df_group_stats.columns.names = ["Case attribute", "Value"]
        df_group_stats.index.names = [group_type]
        df_group_stats_transposed = df_group_stats.transpose()
        df_group_stats_transposed_for_log = df_group_stats_transposed.applymap(lambda x: 1 if x == 0 else x)
        gmap = np.log(df_group_stats_transposed_for_log.astype(float))
        df_group_stats_style = df_group_stats_transposed.apply(pd.to_numeric).style.background_gradient(
            cmap='Blues', axis=None, gmap=gmap)
        df_group_stats_style.format('{:.0f}').set_properties(
            **{'font-size': '11pt', 'border-color': 'black', 'border-style': 'solid', 'border-width': '1px',
               'border-collapse': 'collapse'})
        dfi.export(df_group_stats_style,
                   f"{self.analysis_directory}\\case_attribute_analysis\\"
                   f"across_groups\\heatmap_{case_attribute_name}_{group_type}_{str_groups}.png")

    ######################################################
    ################# RESOURCE ANALYSIS ##################
    ######################################################

    def plot_heatmap_resources_across_groups(self, group_type, groups_to_compare, resources_int_list,
                                             groups_description="", resources_description=""):
        str_groups = f"{str(groups_to_compare[0])}"
        for group in groups_to_compare[1:]:
            str_groups += f"_{str(group)}"

        str_resources = f"{str(resources_int_list[0])}"
        for resource in resources_int_list[1:]:
            str_resources += f"_{str(resource)}"

        columns = [str(group) for group in groups_to_compare]
        index = resources_int_list
        df_group_stats = pd.DataFrame(index=index, columns=columns)
        for resource in resources_int_list:
            for group in groups_to_compare:
                variant_ids_in_group = []
                if group_type == 'Cluster':
                    if isinstance(group, list):
                        for g in group:
                            variant_ids_in_group.extend(self.df_variants_clustered
                                                        .loc[self.df_variants_clustered['cluster'] == g, 'ID']
                                                        .tolist())
                    else:
                        variant_ids_in_group.extend(self.df_variants_clustered
                                                    .loc[self.df_variants_clustered['cluster'] == group, 'ID']
                                                    .tolist())
                elif group_type == 'variant':
                    if isinstance(group, list):
                        variant_ids_in_group = group
                    else:
                        variant_ids_in_group = [group]

                group_frequency = self.eg.query_resource_frequency_from_variant_ids(f"User_{int(resource)}",
                                                                                    variant_ids_in_group)
                df_group_stats.loc[resource, str(group)] = int(group_frequency)
        df_group_stats.sort_index(inplace=True)
        df_group_stats.columns.names = [group_type]
        df_group_stats.index.names = ['Resource']
        df_group_stats_for_log = df_group_stats.applymap(lambda x: 1 if x == 0 else x)
        gmap = np.log(df_group_stats_for_log.astype(float))
        df_group_stats_style = df_group_stats.apply(pd.to_numeric).style.background_gradient(
            cmap='Blues', axis=None, gmap=gmap)
        df_group_stats_style.format('{:.0f}').set_properties(
            **{'font-size': '11pt', 'border-color': 'black', 'border-style': 'solid', 'border-width': '1px',
               'border-collapse': 'collapse'})
        if groups_description == "":
            dfi.export(df_group_stats_style,
                       f"{self.analysis_directory}\\resource_analysis\\heatmap_{group_type}_{str_groups}_R_{str_resources}.png")
        else:
            dfi.export(df_group_stats_style,
                       f"{self.analysis_directory}\\resource_analysis\\heatmap_{group_type}_{groups_description}_R_{resources_description}.png")

    # TODO:
    #     # def plot_heatmap_resources_per_clusters(self):

    ######################################################
    ################ PERFORMANCE ANALYSIS ################
    ######################################################

    def plot_boxplot_case_duration_across_groups(self, group_type, groups_to_compare):
        str_groups = f"{str(groups_to_compare[0])}"
        for group in groups_to_compare[1:]:
            str_groups += f"_{str(group)}"

        columns = [str(group) for group in groups_to_compare]
        df_group_durations = pd.DataFrame()

        for group in groups_to_compare:
            if isinstance(group, list):
                variant_ids_in_group_list = []
                for g in group:
                    if group_type == 'Cluster':
                        variant_ids_in_group = self.df_variants_clustered.loc[
                            self.df_variants_clustered['cluster'] == g, 'ID'].tolist()
                        print(variant_ids_in_group)

                    elif group_type == 'variant':
                        variant_ids_in_group = [g]
                        print(variant_ids_in_group)
                    variant_ids_in_group_list.append(variant_ids_in_group)
                if len(group) == 3:
                    durations = self.eg.query_case_durations_from_variant_ids_three_sets(variant_ids_in_group_list[0],
                                                                                         variant_ids_in_group_list[1],
                                                                                         variant_ids_in_group_list[2])
                elif len(group) == 2:
                    durations = self.eg.query_case_durations_from_variant_ids_two_sets(variant_ids_in_group_list[0],
                                                                                       variant_ids_in_group_list[1])
            else:
                variant_ids_in_group = []
                if group_type == 'Cluster':
                    variant_ids_in_group.extend(self.df_variants_clustered
                                                .loc[self.df_variants_clustered['cluster'] == group, 'ID']
                                                .tolist())
                    print(variant_ids_in_group)
                elif group_type == 'variant':
                    variant_ids_in_group = [group]
                    print(variant_ids_in_group)
                durations = self.eg.query_case_durations_from_variant_ids(variant_ids_in_group)
            print(f"Average duration group {group}: {mean(durations)}")

            sr_durations = pd.DataFrame({str(group): durations})
            df_group_durations = pd.concat([df_group_durations, sr_durations], axis=1)
        df_group_durations.plot.kde(linewidth=0.7)
        plt.xlabel("Duration (days)")
        plt.savefig(
            f"{self.analysis_directory}\\performance_analysis\\kde_{group_type}_{str_groups}_duration.png")
        plt.show()
        df_group_durations.plot.box()
        plt.xlabel(group_type)
        plt.ylabel("Duration (days)")
        plt.savefig(
            f"{self.analysis_directory}\\performance_analysis\\box_plot_{group_type}_{str_groups}_duration.png")
        plt.show()
        if len(groups_to_compare) == 2:
            d_group_1 = sm.stats.DescrStatsW(df_group_durations[str(groups_to_compare[0])].dropna())
            d_group_2 = sm.stats.DescrStatsW(df_group_durations[str(groups_to_compare[1])].dropna())
            cm = sm.stats.CompareMeans(d_group_1, d_group_2)
            t_test = cm.ttest_ind(alternative='two-sided')
            print(f"P-value: {t_test[1]}")

    def plot_boxplot_case_duration_group_and_remainder(self, group_type, group):
        str_group = f"{str(group)}"
        columns = [str(group), f"not in {str(group)}"]
        df_group_durations = pd.DataFrame()

        variant_ids_in_group = []
        if group_type == 'Cluster':
            for g in group:
                variant_ids_in_group.extend(self.df_variants_clustered
                                            .loc[self.df_variants_clustered['cluster'] == g, 'ID']
                                            .tolist())
                print(variant_ids_in_group)
        elif group_type == 'variant':
            variant_ids_in_group = group
            print(variant_ids_in_group)
        durations_in_group = self.eg.query_case_durations_from_variant_ids(variant_ids_in_group)
        durations_not_in_group = self.eg.query_case_durations_outside_variant_ids(variant_ids_in_group)

        sr_durations = pd.DataFrame({str(group): durations_in_group})
        df_group_durations = pd.concat([df_group_durations, sr_durations], axis=1)
        sr_durations = pd.DataFrame({f"not in {str(group)}": durations_not_in_group})
        df_group_durations = pd.concat([df_group_durations, sr_durations], axis=1)

        df_group_durations.plot.kde(linewidth=0.7)
        plt.xlabel("Duration (days)")
        plt.savefig(
            f"{self.analysis_directory}\\performance_analysis\\kde_{group_type}_{group}_not{group}_duration.png")
        plt.show()
        df_group_durations.plot.box()
        plt.xlabel(group_type)
        plt.ylabel("Duration (days)")
        plt.savefig(
            f"{self.analysis_directory}\\performance_analysis\\box_plot_{group_type}_{group}_not{group}_duration.png")
        plt.show()
        d_group_1 = sm.stats.DescrStatsW(df_group_durations[str(group)].dropna())
        d_group_2 = sm.stats.DescrStatsW(df_group_durations[f"not in {str(group)}"].dropna())
        cm = sm.stats.CompareMeans(d_group_1, d_group_2)
        t_test = cm.ttest_ind(alternative='two-sided')
        print(f"P-value: {t_test[1]}")

    ######################################################
    ############ variant FREQUENCY ANALYSIS ##############
    ######################################################

    def plot_cluster_bar_chart(self):
        for cluster in range(0, self.num_clusters):
            variant_ids_in_cluster = self.df_variants_clustered.loc[
                self.df_variants_clustered['cluster'] == cluster, 'ID'].tolist()
            df_variants_frequencies = self.eg.query_variant_frequencies_from_variant_ids(variant_ids_in_cluster)
            ax = df_variants_frequencies.plot.barh(x='frequency', y='variant')
            plt.savefig(f"{self.analysis_directory}\\cluster_statistics\\cluster{cluster}_variant_frequencies.png")

    ######################################################
    ################# EXTRACT SUB-LOGS ###################
    ######################################################

    # def extract_local_cluster_log(self, cluster):
