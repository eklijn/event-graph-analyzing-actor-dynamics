import pandas as pd
from performance.PerformanceRecorder import PerformanceRecorder
from neo4j import GraphDatabase


class ClusterConstructor:

    def __init__(self, password, name_data_set, case_label, actor_label):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", password))
        self.name_data_set = name_data_set
        self.case_label = case_label
        self.actor_label = actor_label

    def construct_clusters(self, df_variants_clustered, use_apoc=False):
        pr = PerformanceRecorder(self.name_data_set, 'constructing_clusters')
        if use_apoc:
            construct_clusters_apoc(df_variants_clustered, self.driver, pr)
        else:
            construct_clusters(df_variants_clustered, self.driver, pr)
        pr.record_total_performance()
        pr.save_to_file()

    def remove_cluster_constructs(self, use_apoc=True):
        if use_apoc:
            remove_cluster_constructs_apoc(self.driver)
        else:
            remove_cluster_constructs(self.driver)


def construct_clusters_apoc(df_variants_clustered, driver, performance_recorder):
    for index, row in df_variants_clustered.iterrows():
        # write cluster as property to task instance nodes
        if not pd.isna(row['cluster']):
            query_write_clusters_to_task_instances = f'''
                CALL apoc.periodic.iterate(
                "MATCH (ti:TaskInstance) WHERE ti.variant = {row['variant']}
                 RETURN ti",
                "WITH ti
                 SET ti.cluster = "{row['cluster']}"",
                {{batchSize:100}})'''
            run_query(driver, query_write_clusters_to_task_instances)
    performance_recorder.record_performance("write_clusters_to_task_instances")

    # create cluster nodes
    query_create_cluster_nodes = f'''
        CALL apoc.periodic.iterate(
        "MATCH (ti:TaskInstance) WHERE ti.cluster IS NOT NULL 
         RETURN DISTINCT ti.cluster AS cluster, count(*) AS cluster_count",
        "WITH cluster, cluster_count
         MERGE (tc:TaskCluster {{Name:cluster, count:cluster_count}})",
        {{batchSize:100}})'''
    run_query(driver, query_create_cluster_nodes)
    performance_recorder.record_performance("create_cluster_nodes")

    # link task instance nodes to corresponding cluster nodes
    query_link_task_instances_to_clusters = f'''
        CALL apoc.periodic.iterate(
        "MATCH (tc:TaskCluster)
         MATCH (ti:TaskInstance) WHERE ti.cluster = tc.Name
         RETURN tc, ti",
        "WITH tc, ti
         CREATE (ti)-[:OBSERVED]->(tc)",
        {{batchSize:100}})'''
    run_query(driver, query_link_task_instances_to_clusters)
    performance_recorder.record_performance("link_task_instances_to_clusters")
    print("COMPLETED constructing clusters")


def construct_clusters(df_variants_clustered, driver, performance_recorder):
    for index, row in df_variants_clustered.iterrows():
        # write cluster as property to task instance nodes
        if not pd.isna(row['cluster']):
            query_write_clusters_to_task_instances = f'''
                MATCH (ti:TaskInstance) WHERE ti.variant = {row['variant']}
                CALL {{
                    WITH ti
                    SET ti.cluster = "{row['cluster']}"
                }} IN TRANSACTIONS OF 100 ROWS'''
            run_query(driver, query_write_clusters_to_task_instances)
    performance_recorder.record_performance("write_clusters_to_task_instances")

    # create cluster nodes
    query_create_cluster_nodes = f'''
        MATCH (ti:TaskInstance) WHERE ti.cluster IS NOT NULL
        WITH DISTINCT ti.cluster AS cluster, count(*) AS cluster_count
        CALL {{
            WITH cluster, cluster_count
            MERGE (tc:TaskCluster {{Name:cluster, count:cluster_count}})
        }} IN TRANSACTIONS OF 1000 ROWS'''
    run_query(driver, query_create_cluster_nodes)
    performance_recorder.record_performance("create_cluster_nodes")

    # link task instance nodes to corresponding cluster nodes
    query_link_task_instances_to_clusters = f'''
       MATCH (tc:TaskCluster)
       MATCH (ti:TaskInstance) WHERE ti.cluster = tc.Name
       CALL {{
           WITH tc, ti
           CREATE (ti)-[:OBSERVED]->(tc)
       }} IN TRANSACTIONS OF 1000 ROWS'''
    run_query(driver, query_link_task_instances_to_clusters)
    performance_recorder.record_performance("link_task_instances_to_clusters")
    print("COMPLETED constructing clusters")


def remove_cluster_constructs_apoc(driver):
    # remove cluster nodes and all attached relationships
    query_remove_cluster_nodes = f'''
        CALL apoc.periodic.iterate(
        "MATCH (tc:TaskCluster)
         RETURN tc", 
        "WITH tc
         DETACH DELETE tc",
        {{batchSize:100}})'''
    run_query(driver, query_remove_cluster_nodes)

    # remove cluster property from ti nodes
    query_remove_cluster_property = f'''
        CALL apoc.periodic.iterate(
        "MATCH (ti:TaskInstance)
         RETURN ti", 
        "WITH ti
         REMOVE ti.cluster",
        {{batchSize:100}})'''
    run_query(driver, query_remove_cluster_property)


def remove_cluster_constructs(driver):
    # remove cluster nodes and all attached relationships
    query_remove_cluster_nodes = f'''
        MATCH (tc:TaskCluster)
        CALL {{
            WITH tc
            DETACH DELETE tc
        }} IN TRANSACTIONS OF 1000 ROWS'''
    run_query(driver, query_remove_cluster_nodes)

    # remove cluster property from ti nodes
    query_remove_cluster_property = f'''
        MATCH (ti:TaskInstance)
        CALL {{
            WITH ti
            REMOVE ti.cluster
        }} IN TRANSACTIONS OF 1000 ROWS'''
    run_query(driver, query_remove_cluster_property)


def aggregate_df_between_clusters(driver, case_label, actor_label):
    entity_labels = [case_label, actor_label]
    for entity in entity_labels:
        # aggregate DF-relationships between clusters
        query_aggregate_directly_follows_clusters = f'''
            MATCH (tc1:TaskCluster)<-[:OBSERVED]-(ti1:TaskInstance)-[df:DF_TI_{entity}]->(ti2:TaskInstance)-[:OBSERVED]->(tc2:TaskCluster)
            MATCH (ti1)-[:CORR]->(n:{entity})<-[:CORR]-(ti2)
            WITH tc1, count(df) AS df_freq, tc2
            MERGE (tc1)-[rel2:DF_TC_{entity}]->(tc2) ON CREATE SET rel2.count=df_freq'''
        run_query(driver, query_aggregate_directly_follows_clusters)


def construct_artificial_start_end_case_resource(driver):
    # create artificial start and end nodes
    query_create_artificial_start_and_end = f'''
        CREATE (:TaskCluster {{Name:"start"}})
        CREATE (:TaskCluster {{Name:"end"}})'''
    run_query(driver, query_create_artificial_start_and_end)

    # connect artificial start and end for case perspective
    query_connect_artificial_start_case = f'''
        MATCH (tc:TaskCluster) WHERE NOT (:TaskCluster)-[:DF_TC {{EntityType:"case"}}]->(tc)
            AND NOT tc.Name IN ["start", "end"]
        WITH tc, tc.count AS count
        MATCH (start:TaskCluster {{Name:"start"}})
        WITH start, tc, count
        MERGE (start)-[df:DF_TC {{EntityType:"case", count:count}}]->(tc)'''
    run_query(driver, query_connect_artificial_start_case)
    query_connect_artificial_end_case = f'''
        MATCH (tc:TaskCluster) WHERE NOT (tc)-[:DF_TC {{EntityType:"case"}}]->(:TaskCluster)
            AND NOT tc.Name IN ["start", "end"]
        WITH tc, tc.count AS count
        MATCH (end:TaskCluster {{Name:"end"}})
        WITH end, tc, count
        MERGE (tc)-[df:DF_TC {{EntityType:"case", count:count}}]->(end)'''
    run_query(driver, query_connect_artificial_end_case)

    # connect artificial start and end for resource perspective
    query_connect_artificial_start_resource = f'''
        MATCH (ti0:TaskInstance)-[df:DF_TI {{EntityType:"resource"}}]->(ti1:TaskInstance)
            WHERE NOT date(ti0.end_time) = date(ti1.start_time) AND EXISTS(ti1.cluster)
        WITH DISTINCT ti1.cluster AS cluster, count(*) AS count
        MATCH (tc:TaskCluster {{Name:cluster}})
        WITH tc, count
        MATCH (start:TaskCluster {{Name:"start"}})
        WITH tc, start, count
        MERGE (start)-[df:DF_TC {{EntityType:"resource", count:count}}]->(tc)'''
    run_query(driver, query_connect_artificial_start_resource)
    query_connect_artificial_end_resource = f'''
        MATCH (ti0:TaskInstance)-[df:DF_TI {{EntityType:"resource"}}]->(ti1:TaskInstance) 
            WHERE NOT date(ti0.end_time) = date(ti1.start_time) AND EXISTS(ti0.cluster)
        WITH DISTINCT ti0.cluster AS cluster, count(*) AS count
        MATCH (tc:TaskCluster {{Name:cluster}})
        WITH tc, count
        MATCH (end:TaskCluster {{Name:"end"}})
        WITH tc, end, count
        MERGE (tc)-[df:DF_TC {{EntityType:"resource", count:count}}]->(end)'''
    run_query(driver, query_connect_artificial_end_resource)

def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query).single()
        if result:
            return result.value()
        else:
            return None
