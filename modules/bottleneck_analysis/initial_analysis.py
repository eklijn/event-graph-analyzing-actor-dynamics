import pandas as pd
from os import path

from GraphConfigurator import GraphConfigurator

meta_directory = "modules\\bottleneck_analysis\\meta-output\\"


def analyze_actor_edge_durations(query_engine):
    # if path.exists(f"{meta_directory}actor_edge_dynamics.pkl"):
    #     df_actor_edge_dynamics = pd.read_pickle(f"{meta_directory}actor_edge_dynamics.pkl")
    # else:
    #     df_actor_edge_dynamics = query_engine.get_actor_edge_duration_and_dynamics()
    #     df_actor_edge_dynamics.to_pickle(f"{meta_directory}actor_edge_dynamics.pkl")
    df_actor_edge_dynamics = query_engine.get_actor_edge_duration_and_dynamics()
    df_actor_edge_dynamics_actor_longest = df_actor_edge_dynamics[
        df_actor_edge_dynamics['dfr_duration'] > df_actor_edge_dynamics['dfc_duration']]
    print(f"Number actor longest: {len(df_actor_edge_dynamics_actor_longest)}")
    df_actor_edge_dynamics_case_longest = df_actor_edge_dynamics[
        df_actor_edge_dynamics['dfc_duration'] > df_actor_edge_dynamics['dfr_duration']]
    print(f"Number case longest: {len(df_actor_edge_dynamics_case_longest)}")
    df_actor_edge_dynamics_per_actor = df_actor_edge_dynamics_case_longest.groupby(['current_actor']).agg({'dfc_duration_seconds': ['min', 'max', 'mean']})
    print()
