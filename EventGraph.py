import pandas as pd
from neo4j import GraphDatabase
from neotime import DateTime
import datetime


class EventGraph:
    def __init__(self, password, entity_labels):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", password))
        self.entity_labels = entity_labels

    def query_variants(self, min_frequency):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (ti:TaskInstance)
                WITH ti.path AS path, ti.ID AS ID, size(ti.path) AS path_length
                WITH DISTINCT path, path_length, ID, COUNT (*) AS frequency WHERE frequency >= {min_frequency}
                RETURN path, path_length, ID, frequency
                '''
            # print(q)
            result = session.run(q)
            df_variants = pd.DataFrame([dict(record) for record in result])
        return df_variants

    def query_variants_in_cluster(self):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (ti:TaskInstance) WHERE EXISTS(ti.cluster)
                WITH ti.path AS path, ti.ID AS ID, ti.cluster AS cluster
                WITH DISTINCT path, ID, cluster, COUNT (*) AS frequency
                RETURN ID, path, frequency, cluster
                '''
            result = session.run(q)
            df_variants_in_cluster = pd.DataFrame([dict(record) for record in result])
        return df_variants_in_cluster

    def query_variants_in_cluster_decomposed(self, decomposed_property):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (ti:TaskInstance) WHERE EXISTS(ti.cluster)
                WITH ti.path AS path, ti.ID AS ID, ti.{decomposed_property} AS decomposed_property, ti.cluster AS cluster
                WITH DISTINCT path, decomposed_property, ID, cluster, COUNT (*) AS frequency
                RETURN cluster, ID, path, decomposed_property, frequency
                '''
            result = session.run(q)
            df_variants_in_cluster_decomposed = pd.DataFrame([dict(record) for record in result])
        return df_variants_in_cluster_decomposed

    def query_actor_task_path(self, actor):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.rID = "{actor}"
                WITH date.truncate('day', ti.start_time) AS day, ti.cluster AS task, ti.start_time AS start, ti.end_time AS end
                RETURN day, task, start, end ORDER BY start
                '''
            # print(q)
            result = session.run(q)
            df_actor_task_path = pd.DataFrame([dict(record) for record in result])
        return df_actor_task_path

    def query_task_list(self):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (tc:TaskCluster)
                WITH tc.Name AS task
                RETURN task
                '''
            # print(q)
            result = session.run(q)
            task_list = []
            for record in result:
                task_list.append(record['task'])
        return task_list

    def query_time_pending(self, current_task):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (ti1:TaskInstance)-[:DF_TI {{EntityType:'case'}}]->(ti2:TaskInstance)
                    -[:DF_TI {{EntityType:'case'}}]->(ti3:TaskInstance) WHERE ti2.cluster = "{current_task}"
                WITH duration.inSeconds(ti1.end_time, ti2.start_time) AS time_pending, ti3.rID AS next_actor, 
                    ti3.cluster AS next_task
                RETURN time_pending, next_actor, next_task
                '''
            result = session.run(q)
            df_time_pending = pd.DataFrame([dict(record) for record in result])
            for index, row in df_time_pending.iterrows():
                time_pending = row['time_pending']
                time_pending_seconds = time_pending.hours_minutes_seconds_nanoseconds[0] * 3600 + time_pending.hours_minutes_seconds_nanoseconds[1] * 60 + time_pending.hours_minutes_seconds_nanoseconds[2]
                df_time_pending.loc[index, 'time_pending_seconds'] = time_pending_seconds
        return df_time_pending

    def query_start_end_date(self):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (ti:TaskInstance)
                WITH min(ti.start_time) AS start_time
                RETURN start_time
                '''
            result = session.run(q)
            nst = result.single()[0]
            start_time = datetime.datetime(nst.year, nst.month, nst.day, nst.hour, nst.minute, int(nst.second)).date()
            # language=Cypher
            q = f'''
                MATCH (ti:TaskInstance)
                WITH max(ti.start_time) AS end_time
                RETURN end_time
                '''
            result = session.run(q)
            net = result.single()[0]
            end_time = datetime.datetime(net.year, net.month, net.day, net.hour, net.minute, int(net.second)).date()
        return start_time, end_time

    def query_actor_list(self, min_freq=0):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.cluster IS NOT NULL
                WITH DISTINCT ti.rID AS actor, COUNT(*) AS count WHERE count > {min_freq}
                RETURN actor
                '''
            result = session.run(q)
            actor_list = []
            for record in result:
                actor_list.append(record['actor'])
        return actor_list

    def query_colab_list(self):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (ti1:TaskInstance)-[:DF_TI]->(ti2:TaskInstance) WHERE ti1.rID <> ti2.rID AND ti1.rID <> "User_1" 
                    AND ti2.rID <> "User_1" AND ti1.cluster IS NOT NULL AND ti2.cluster IS NOT NULL
                WITH DISTINCT ti1.rID AS actor_1, ti2.rID AS actor_2, count(*) AS count WHERE count > 100
                RETURN actor_1, actor_2
                '''
            result = session.run(q)
            actor_list = []
            for record in result:
                actor_list.append([record['actor_1'], record['actor_2']])
        return actor_list

    def query_task_subgraph_nodes(self, start_date, end_date, exclude_cluster=""):
        where_exclude_cluster = ""
        if not exclude_cluster == "":
            where_exclude_cluster = f"AND ti.cluster <> \"{exclude_cluster}\""
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE date("{start_date}") <= date(ti.start_time) 
                    AND date(ti.end_time) <= date("{end_date}") AND ti.cluster IS NOT NULL {where_exclude_cluster}
                WITH ti.cluster AS task, ti.ID AS task_variant, ti.cID AS case, ti.rID AS actor,
                    duration.inSeconds(ti.start_time, ti.end_time) AS duration
                RETURN task, task_variant, case, actor, duration
                '''
            # print(q)
            result = session.run(q)
            df_subgraph_nodes = pd.DataFrame([dict(record) for record in result])
            for index, row in df_subgraph_nodes.iterrows():
                duration = row['duration']
                duration_seconds = duration.hours_minutes_seconds_nanoseconds[0] * 3600 + duration.hours_minutes_seconds_nanoseconds[1] * 60 + duration.hours_minutes_seconds_nanoseconds[2]
                df_subgraph_nodes.loc[index, 'duration'] = duration_seconds
        return df_subgraph_nodes

    def query_task_subgraph_edges(self, start_date, end_date, exclude_cluster=""):
        where_exclude_cluster = ""
        if not exclude_cluster == "":
            where_exclude_cluster = f"AND ti1.cluster <> \"{exclude_cluster}\" AND ti2.cluster <> \"{exclude_cluster}\""
        with self.driver.session() as session:
            q = f'''
                MATCH (ti1:TaskInstance)-[r:DF_TI]->(ti2:TaskInstance) 
                    WHERE date("{start_date}") <= date(ti1.end_time) AND date(ti2.start_time) <= date("{end_date}") 
                    AND ti1.cluster IS NOT NULL AND ti2.cluster IS NOT NULL {where_exclude_cluster}
                WITH ti1.cluster AS task_1, ti2.cluster AS task_2, ti1.ID AS task_variant_1, ti2.ID AS task_variant_2, 
                    ti1.cID AS case_1, ti2.cID AS case_2, ti1.rID AS actor_1, ti2.rID AS actor_2,
                    duration.inSeconds(ti1.end_time, ti2.start_time) AS duration, r.EntityType AS entity_type
                RETURN task_1, task_2, task_variant_1, task_variant_2, case_1, case_2, actor_1, actor_2, duration, 
                    entity_type
                '''
            # print(q)
            result = session.run(q)
            df_subgraph_edges = pd.DataFrame([dict(record) for record in result])
            for index, row in df_subgraph_edges.iterrows():
                duration = row['duration']
                duration_seconds = duration.hours_minutes_seconds_nanoseconds[0] * 3600 + duration.hours_minutes_seconds_nanoseconds[1] * 60 + duration.hours_minutes_seconds_nanoseconds[2]
                df_subgraph_edges.loc[index, 'duration'] = duration_seconds
        return df_subgraph_edges

    def query_event_subgraph_nodes(self, start_date, end_date):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (e:Event) WHERE date("{start_date}") <= date(e.timestamp) <= date("{end_date}")
                WITH e.activity AS activity, e.activity_lifecycle AS activity_lifecycle, e.case AS case,
                    e.resource AS actor
                RETURN activity, activity_lifecycle, case, actor
                '''
            # print(q)
            result = session.run(q)
            df_subgraph_nodes = pd.DataFrame([dict(record) for record in result])
        return df_subgraph_nodes

    def query_event_subgraph_edges(self, start_date, end_date):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (e1:Event)-[r:DF]->(e2:Event) 
                    WHERE date("{start_date}") <= date(e1.timestamp) 
                    AND date(e2.timestamp) <= date("{end_date}")
                WITH e1.activity AS activity_1, e2.activity AS activity_2, 
                    e1.activity_lifecycle AS activity_lifecycle_1, e2.activity_lifecycle AS activity_lifecycle_2, 
                    e1.case AS case_1, e2.case AS case_2, e1.resource AS actor_1, e2.resource AS actor_2,
                    duration.inSeconds(e1.timestamp, e2.timestamp) AS duration, r.EntityType AS entity_type
                RETURN activity_1, activity_2, activity_lifecycle_1, activity_lifecycle_2, 
                    case_1, case_2, actor_1, actor_2, duration, entity_type
                '''
            # print(q)
            result = session.run(q)
            df_subgraph_edges = pd.DataFrame([dict(record) for record in result])
            for index, row in df_subgraph_edges.iterrows():
                duration = row['duration']
                duration_seconds = duration.hours_minutes_seconds_nanoseconds[0] * 3600 + duration.hours_minutes_seconds_nanoseconds[1] * 60 + duration.hours_minutes_seconds_nanoseconds[2]
                df_subgraph_edges.loc[index, 'duration'] = duration_seconds
        return df_subgraph_edges


def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query).single()
        if result:
            return result
        else:
            return None
