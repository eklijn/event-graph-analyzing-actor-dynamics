import pandas as pd
from neo4j import GraphDatabase


class BottleneckAnalysisQueryEngine:
    def __init__(self, password, actor_label, case_label):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", password))
        self.actor_label = actor_label
        self.case_label = case_label

    def get_workload_vs_avg_task_duration(self, task):
        with self.driver.session() as session:
            q = f'''
                MATCH ()-[df:WAIT_DF_TI_{self.case_label}]->(ti) WHERE df.count IS NOT NULL AND ti.cluster = "{task}"
                WITH df.count AS nr_waiting, duration.inSeconds(ti.start_time, ti.end_time) AS task_duration
                WITH DISTINCT nr_waiting, count(*) AS count, AVG(task_duration) AS avg_task_duration
                RETURN nr_waiting, count, avg_task_duration ORDER BY nr_waiting ASC
                '''
            result = session.run(q)
            df_workload_vs_task_duration = pd.DataFrame([dict(record) for record in result])
            for index, row in df_workload_vs_task_duration.iterrows():
                avg_task_duration = row['avg_task_duration']
                avg_task_duration_seconds = avg_task_duration.hours_minutes_seconds_nanoseconds[0] * 3600 + avg_task_duration.hours_minutes_seconds_nanoseconds[1] * 60 + avg_task_duration.hours_minutes_seconds_nanoseconds[2]
                df_workload_vs_task_duration.loc[index, 'avg_task_duration_seconds'] = avg_task_duration_seconds
                df_workload_vs_task_duration.drop(columns=['avg_task_duration'])
        return df_workload_vs_task_duration

    def get_workload_vs_task_duration(self, task):
        with self.driver.session() as session:
            q = f'''
                MATCH ()-[df:WAIT_DF_TI_{self.case_label}]->(ti)-[:CORR]->(n:{self.actor_label}) 
                    WHERE df.count IS NOT NULL AND ti.cluster = "{task}" AND n.sysId <> "User_1"
                WITH df.count AS nr_waiting, duration.inSeconds(ti.start_time, ti.end_time) AS task_duration
                RETURN nr_waiting, task_duration
                '''
            result = session.run(q)
            df_workload_vs_task_duration = pd.DataFrame([dict(record) for record in result])
            for index, row in df_workload_vs_task_duration.iterrows():
                task_duration = row['task_duration']
                task_duration_seconds = task_duration.hours_minutes_seconds_nanoseconds[0] * 3600 + task_duration.hours_minutes_seconds_nanoseconds[1] * 60 + task_duration.hours_minutes_seconds_nanoseconds[2]
                df_workload_vs_task_duration.loc[index, 'task_duration_seconds'] = task_duration_seconds
                df_workload_vs_task_duration.drop(columns=['task_duration'])
        return df_workload_vs_task_duration

    def get_actor_edge_duration_and_dynamics(self):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (tic:TaskInstance)-[dfc:DF_TI_CaseAWO]->(ti:TaskInstance)
                    <-[dfr:DF_TI_Resource]-(tir:TaskInstance)-[:CORR]->(n:Resource)
                WITH ti, duration.inSeconds(tic.end_time, ti.start_time) AS dfc_duration, 
                    duration.inSeconds(tir.end_time, ti.start_time) AS dfr_duration, 
                    n.sysId AS current_actor, ti.cluster AS current_task
                MATCH (ti:TaskInstance)-[:DF_TI_CaseAWO]->(ti_next)-[:CORR]->(n:Resource)
                RETURN current_task, current_actor, ti_next.cluster AS next_task, n.sysId AS next_actor, 
                    dfr_duration, dfc_duration
                '''
            # q = f'''
            #     MATCH (tic:TaskInstance)-[dfc:DF_TI_CaseAWO]->(ti:TaskInstance)
            #         <-[dfr:DF_TI_Resource]-(tir:TaskInstance)-[:CORR]->(n:Resource)
            #     WITH ti, duration.inSeconds(tic.end_time, ti.start_time) AS dfc_duration,
            #         duration.inSeconds(tir.end_time, ti.start_time) AS dfr_duration, tir.end_time AS time,
            #         n.sysId AS current_actor, ti.cluster AS current_task
            #     MATCH (ti:TaskInstance)-[:DF_TI_CaseAWO]->(ti_next)-[:CORR]->(n:Resource)
            #     RETURN time, current_task, current_actor, ti_next.cluster AS next_task, n.sysId AS next_actor,
            #         dfr_duration, dfc_duration
            #     '''
            # print(q)
            result = session.run(q)
            df_actor_edge_dynamics = pd.DataFrame([dict(record) for record in result])
            for index, row in df_actor_edge_dynamics.iterrows():
                dfr_duration = row['dfr_duration']
                dfc_duration = row['dfc_duration']
                dfr_duration_seconds = dfr_duration.hours_minutes_seconds_nanoseconds[0] * 3600 + dfr_duration.hours_minutes_seconds_nanoseconds[1] * 60 + dfr_duration.hours_minutes_seconds_nanoseconds[2]
                dfc_duration_seconds = dfc_duration.hours_minutes_seconds_nanoseconds[0] * 3600 + dfc_duration.hours_minutes_seconds_nanoseconds[1] * 60 + dfc_duration.hours_minutes_seconds_nanoseconds[2]
                df_actor_edge_dynamics.loc[index, 'dfr_duration_seconds'] = dfr_duration_seconds
                df_actor_edge_dynamics.loc[index, 'dfc_duration_seconds'] = dfc_duration_seconds
                df_actor_edge_dynamics.drop(columns=['dfr_duration', 'dfc_duration'])
        return df_actor_edge_dynamics

    def write_performance_state_to_task_instances(self):
        q = f'''
            CALL apoc.periodic.iterate(
            "MATCH (tic:TaskInstance)-[:DF_TI_CaseAWO]->(ti:TaskInstance)
             RETURN ti, tic.end_time AS waiting_start",
            "WITH ti, waiting_start
             MATCH p=(ti_first:TaskInstance)-[:DF_TI_Resource*]->(ti) WHERE ti_first.end_time > waiting_start
             RETURN ti, max(length(p))",
            {{batchSize:100}})
                '''

def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query).single()
        if result:
            return result
        else:
            return None
