import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean
import statsmodels.api as sm
import os

from GraphConfigurator import GraphConfigurator
from AnalysisConfigurator import AnalysisConfigurator
from EventGraph import EventGraph

graph = "bpic2017_case_attr"

gc = GraphConfigurator(graph)
ac = AnalysisConfigurator(graph)
eg = EventGraph(gc.get_password(), gc.get_entity_labels())

analysis_directory = os.path.join(ac.get_analysis_directory(), "distr_time_pending")
os.makedirs(analysis_directory, exist_ok=True)

df_time_pending = eg.query_time_pending("T05")

# list of next actors who frequently follow with the same task (=T04)
list_next_actors = ["User_112", "User_113", "User_114", "User_116", "User_117", "User_118", "User_119", "User_120",
                    "User_121", "User_122", "User_123", "User_125", "User_126"]

df_time_pending_t04 = df_time_pending[(df_time_pending['next_task'] == "T04") & (df_time_pending['next_actor'].isin(list_next_actors))]
fig, ax = plt.subplots(figsize=(18, 16))
boxplot = df_time_pending_t04.groupby('next_actor').plot(kind='kde', ax=ax)
# boxplot = df_time_pending_t04.boxplot(column=['time_pending_seconds'], by='next_actor')
plt.show()

df_time_pending_T04_grouped = df_time_pending_t04.groupby('next_actor').agg(
    count=('time_pending_seconds', 'size'), mean_time_pending=('time_pending_seconds', 'mean'))

df_p_values_next_actors_i_j = pd.DataFrame(index=list_next_actors, columns=list_next_actors)

for i in range(len(list_next_actors)):
    for j in range(len(list_next_actors)):
        if list_next_actors[i] is not list_next_actors[j]:
            actor_i = list_next_actors[i]
            actor_j = list_next_actors[j]
            list_durations_actor_i = \
            df_time_pending[(df_time_pending['next_actor'] == actor_i) & (df_time_pending['next_task'] == "T04")][
                'time_pending_seconds'].to_list()
            list_durations_actor_j = \
            df_time_pending[(df_time_pending['next_actor'] == actor_j) & (df_time_pending['next_task'] == "T04")][
                'time_pending_seconds'].to_list()
            d_actor_i = sm.stats.DescrStatsW(list_durations_actor_i)
            d_actor_j = sm.stats.DescrStatsW(list_durations_actor_j)
            cm = sm.stats.CompareMeans(d_actor_i, d_actor_j)
            t_test = cm.ttest_ind(alternative='two-sided')
            df_p_values_next_actors_i_j.loc[actor_i, actor_j] = t_test[1]
            df_time_pending_T04_grouped.loc[actor_i, f"p_value_{actor_j}"] = t_test[1]

df_p_values_next_actor_i_remainder = pd.DataFrame(index=list_next_actors, columns=['p_value'])
for i in range(len(list_next_actors)):
    actor_i = list_next_actors[i]
    list_durations_actor_i = \
    df_time_pending[(df_time_pending['next_actor'] == actor_i) & (df_time_pending['next_task'] == "T04")][
        'time_pending_seconds'].to_list()
    list_durations_remainder = \
    df_time_pending[(df_time_pending['next_actor'] != actor_i) & (df_time_pending['next_task'] == "T04")][
        'time_pending_seconds'].to_list()
    d_actor_i = sm.stats.DescrStatsW(list_durations_actor_i)
    d_remainder = sm.stats.DescrStatsW(list_durations_remainder)
    cm = sm.stats.CompareMeans(d_actor_i, d_remainder)
    t_test = cm.ttest_ind(alternative='two-sided')
    df_p_values_next_actor_i_remainder.loc[actor_i, 'p_value'] = t_test[1]
    df_time_pending_T04_grouped.loc[actor_i, f"p_value_remainder"] = t_test[1]

# df_time_pending_T04_grouped.to_csv(f"{analysis_directory}\\time_pending_next_actors_T04.csv")
