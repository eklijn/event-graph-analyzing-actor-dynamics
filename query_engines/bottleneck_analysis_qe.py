import pandas as pd
from neo4j import GraphDatabase


class BottleneckAnalysisQueryEngine:
    def __init__(self, password):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", password))

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
