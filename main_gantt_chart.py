import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import os
import datetime

from GraphConfigurator import GraphConfigurator
from AnalysisConfigurator import AnalysisConfigurator
from EventGraph import EventGraph

qual_color_list = ["#aec7e8", "#1f77b4", "#ffbb78", "#ff7f0e", "#98df8a", "#2ca02c", "#ff9896", "#d62728", "#c5b0d5",
                   "#9467bd", "#c49c94", "#8c564b", "#f7b6d2", "#e377c2", "#c7c7c7", "#7f7f7f", "#dbdb8d", "#bcbd22",
                   "#9edae5", "#17becf", "#86b4a9", "#39737c", "#ffff99", "#dec718"]


def get_color_dict_from_cluster_list(cluster_list):
    cluster_list_activities = []
    cluster_list_clusters = []
    for cluster in cluster_list:
        if cluster[0] == "A":
            cluster_list_activities.append(cluster)
        else:
            cluster_list_clusters.append(cluster)
    cluster_list_activities = sorted(cluster_list_activities)
    cluster_list_clusters = sorted(cluster_list_clusters)
    color_dict_clusters = dict(zip(cluster_list_clusters, qual_color_list[:len(cluster_list_clusters)]))
    color_list_activities = ["#000000"] * len(cluster_list_activities)
    color_dict_activities = dict(zip(cluster_list_activities, color_list_activities))
    color_dict = {**color_dict_activities, **color_dict_clusters}
    return color_dict


def add_color(row, based_on_column, color_dict):
    if pd.isna(row[based_on_column]):
        return "#696969"
    else:
        return color_dict[row[based_on_column]]


graph = "bpic2017_case_attr"
actor = "User_123"

gc = GraphConfigurator(graph)
ac = AnalysisConfigurator(graph)
eg = EventGraph(gc.get_password(), gc.get_entity_labels())

analysis_directory = os.path.join(ac.get_analysis_directory(), "actor_scheduled_time")
os.makedirs(analysis_directory, exist_ok=True)

df_gantt_chart = eg.query_actor_task_path(actor=actor)
df_gantt_chart['day'] = pd.to_datetime(df_gantt_chart['day'].astype(str), format='%Y-%m-%d')
df_gantt_chart['start'] = pd.to_datetime(df_gantt_chart['start'].astype(str), format='%Y-%m-%d %H:%M:%S.%f')
df_gantt_chart['end'] = pd.to_datetime(df_gantt_chart['end'].astype(str), format='%Y-%m-%d %H:%M:%S.%f')

for index, row in df_gantt_chart.iterrows():
    if not pd.isna(row['task']):
        if row['task'][0] == "A":
            df_gantt_chart.loc[index, 'end'] = df_gantt_chart.loc[index, 'end'] + datetime.timedelta(seconds=30)
    if row['end'] - row['start'] < datetime.timedelta(seconds=30):
        df_gantt_chart.loc[index, 'end'] = df_gantt_chart.loc[index, 'start'] + datetime.timedelta(seconds=30)

df_gantt_chart['start_time'] = df_gantt_chart['start'].apply(lambda d: d.time())
df_gantt_chart['end_time'] = df_gantt_chart['end'].apply(lambda d: d.time())
df_gantt_chart['start_time_in_hours'] = df_gantt_chart['start_time'].apply(
    lambda d: d.hour + d.minute / 60 + d.second / 3600)
df_gantt_chart['end_time_in_hours'] = df_gantt_chart['end_time'].apply(
    lambda d: d.hour + d.minute / 60 + d.second / 3600)
df_gantt_chart['hours_start_to_end'] = df_gantt_chart['end_time_in_hours'] - df_gantt_chart['start_time_in_hours']

earliest_start_hour = round(df_gantt_chart['start_time_in_hours'].min())

# derive colors for number of tasks and add to dataframe
color_dict = get_color_dict_from_cluster_list(eg.query_task_list())
df_gantt_chart['color'] = df_gantt_chart.apply(add_color, args=('task', color_dict), axis=1)

# filter color dictionary to only contain tasks for actor
actor_task_set = sorted(list(set(df_gantt_chart[~pd.isna(df_gantt_chart['task'])]['task'].to_list())))
color_dict_actor = {key: color_dict[key] for key in actor_task_set}

##### PLOT #####
fig, ax = plt.subplots(1, figsize=(16, 30))
ax.barh(df_gantt_chart['day'], df_gantt_chart.hours_start_to_end, left=df_gantt_chart.start_time_in_hours,
        color=df_gantt_chart.color)

# legend
legend_elements = [Patch(facecolor=color_dict_actor[i], label=i) for i in color_dict_actor]
plt.legend(handles=legend_elements)

# ticks
xticks = np.arange(0, df_gantt_chart['end_time_in_hours'].max()+1, 1)
xticks_minor = np.arange(0, df_gantt_chart['end_time_in_hours'].max()+1, 1)
ax.set_xticks(xticks)
ax.set_xticks(xticks_minor, minor=True)

plt.xlim(earliest_start_hour)
plt.grid(linestyle='--', linewidth=0.8)
plt.gca().invert_yaxis()
plt.savefig(f"{analysis_directory}\\{actor}")
plt.show()
