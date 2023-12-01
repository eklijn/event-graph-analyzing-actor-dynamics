from performance.PerformanceRecorder import PerformanceRecorder
from neo4j import GraphDatabase


class HighLevelEventConstructor:

    def __init__(self, password, name_data_set, actor_label, case_label):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", password))
        self.name_data_set = name_data_set
        self.actor_label = actor_label
        self.case_label = case_label

    def construct(self):
        # create performance recorder
        pr = PerformanceRecorder(self.name_data_set, 'constructing_task_instance_nodes')
        construct(self.driver, self.actor_label, self.case_label, pr)
        pr.record_total_performance()
        pr.save_to_file()

    def set_task_instance_ids(self):
        # create performance recorder
        pr = PerformanceRecorder(self.name_data_set, 'setting_task_instance_ids')
        set_task_instance_ids(self.driver, pr)
        pr.record_total_performance()
        pr.save_to_file()


def construct(driver, actor_label, case_label, performance_recorder):
    # # combine resource and case directly follows relationships
    # query_combine_df_joint = f'''
    #     CALL apoc.periodic.iterate(
    #     "MATCH (e1:Event)-[:DF_{actor_label}]->(e2:Event)
    #      WHERE (e1)-[:DF_{case_label}]->(e2)
    #      RETURN e1,e2",
    #     "WITH e1,e2
    #         MERGE (e1)-[:DF_JOINT]->(e2)",
    #         {{batchSize:100}})'''
    # run_query(driver, query_combine_df_joint)
    # performance_recorder.record_performance('combine_df_joint')
    #
    # # check if the transactional lifecycle is recorded and combine with activity classifier into single property
    # # if len(action_lifecycle_label) == 2:
    # #     query_set_activity_lifecycle_property = f'''
    # #         CALL apoc.periodic.iterate(
    # #         "MATCH (e:Event) RETURN e",
    # #         "WITH e
    # #             SET e.activity_lifecycle = e.{action_lifecycle_label[0]}+'+'+e.{action_lifecycle_label[1]}",
    # #         {{batchSize:100}})'''
    # #     run_query(driver, query_set_activity_lifecycle_property)
    # #     performance_recorder.record_performance('set_activity_lifecycle_property')
    # #     action_lifecycle_label[0] = 'activity_lifecycle'
    #
    # # query and materialize task instances and relationships with events
    # query_create_ti_nodes = f'''
    #     CALL apoc.periodic.iterate(
    #     "CALL {{
    #         MATCH (e1:Event)-[:DF_JOINT]->() WHERE NOT ()-[:DF_JOINT]->(e1)
    #         MATCH ()-[:DF_JOINT]->(e2:Event) WHERE NOT (e2)-[:DF_JOINT]->()
    #         MATCH p=(e1)-[:DF_JOINT*]->(e2)
    #         RETURN p, e1, e2
    #         UNION
    #         MATCH (e:Event) WHERE (e)-[:CORR]->(:{actor_label})
    #         AND NOT ()-[:DF_JOINT]->(e) AND NOT (e)-[:DF_JOINT]->()
    #         MATCH p=(e) RETURN p, e AS e1, e AS e2
    #      }}
    #      RETURN [event in nodes(p) | event.activity+'+'+event.lifecycle] AS variant,
    #        nodes(p) AS events, e1.timestamp AS start_time, e2.timestamp AS end_time",
    #     "WITH variant, events, start_time, end_time
    #         CREATE (ti:TaskInstance {{variant:variant, start_time:start_time, end_time:end_time}})
    #         WITH ti, events
    #         UNWIND events AS e
    #             CREATE (e)<-[:CONTAINS]-(ti)",
    #     {{batchSize:100}})'''
    # run_query(driver, query_create_ti_nodes)
    # performance_recorder.record_performance('create_ti_nodes')
    #
    # # split task instances that span multiple days - create new nodes (multi action task instances)
    # query_split_ti_nodes_create_new_1 = f'''
    #         CALL apoc.periodic.iterate(
    #             "MATCH (ti:TaskInstance)-[:CONTAINS]->(e:Event) WHERE date(ti.start_time) <> date(ti.end_time)
    #              WITH ti, date(e.timestamp) AS date, e ORDER BY e.timestamp
    #              WITH DISTINCT ti, date, COLLECT(e) AS events
    #              WITH events[0] AS e_start, events[size(events)-1] AS e_end
    #              WITH e_start, e_end
    #              MATCH p=(e_start)-[:DF_JOINT*]->(e_end)
    #              WITH p, e_start AS e1, e_end AS e2
    #              RETURN [event in nodes(p) | event.activity+'+'+event.lifecycle] AS variant,
    #                 nodes(p) AS events, e1.timestamp AS start_time, e2.timestamp AS end_time",
    #             "WITH variant, events, start_time, end_time
    #                 CREATE (ti:TaskInstance {{variant:variant, start_time:start_time, end_time:end_time}})
    #                 WITH ti, events
    #                 UNWIND events AS e
    #                 CREATE (e)<-[:CONTAINS]-(ti)",
    #             {{batchSize:100}})'''
    # run_query(driver, query_split_ti_nodes_create_new_1)
    # performance_recorder.record_performance('split_ti_nodes_create_new_1')
    #
    # # split task instances that span multiple days - create new nodes (single action task instances)
    # query_split_ti_nodes_create_new_2 = f'''
    #             CALL apoc.periodic.iterate(
    #             "MATCH (ti:TaskInstance)-[:CONTAINS]->(e:Event) WHERE date(ti.start_time) <> date(ti.end_time)
    #              WITH ti, date(e.timestamp) AS date, e ORDER BY e.timestamp
    #              WITH DISTINCT ti, date, COLLECT(e) AS events
    #              WITH events[0] AS e_start, events[size(events)-1] AS e_end
    #              WITH e_start, e_end
    #              MATCH (e_start) MATCH (e_end) WHERE e_start = e_end
    #              MATCH p=(e_start)
    #              WITH p, e_start AS e1, e_end AS e2
    #              RETURN [event in nodes(p) | event.activity+'+'+event.lifecycle] AS variant,
    #                 nodes(p) AS events, e1.timestamp AS start_time, e2.timestamp AS end_time",
    #             "WITH variant, events, start_time, end_time
    #              CREATE (ti:TaskInstance {{variant:variant, start_time:start_time, end_time:end_time}})
    #              WITH ti, events
    #              UNWIND events AS e
    #              CREATE (e)<-[:CONTAINS]-(ti)",
    #             {{batchSize:100}})'''
    # run_query(driver, query_split_ti_nodes_create_new_2)
    # performance_recorder.record_performance('split_ti_nodes_create_new_2')
    #
    # # split task instances that span multiple days - remove old nodes
    # query_split_ti_nodes_remove_old = f'''
    #             CALL apoc.periodic.iterate(
    #             "MATCH (ti:TaskInstance) WHERE date(ti.start_time) <> date(ti.end_time)
    #              RETURN ti",
    #             "WITH ti
    #              DETACH DELETE ti",
    #             {{batchSize:100}})'''
    # run_query(driver, query_split_ti_nodes_remove_old)
    # performance_recorder.record_performance('split_ti_nodes_remove_old')
    #
    # # remove df_joint edges
    # query_remove_df_joint = f'''
    #         MATCH ()-[r:DF_JOINT]-()
    #         DELETE r'''
    # run_query(driver, query_remove_df_joint)
    # performance_recorder.record_performance('remove_df_joint')

    for entity in [case_label, actor_label]:
        # correlate task instances to entities
        query_correlate_ti_to_entity = f'''
            CALL apoc.periodic.iterate(
                "MATCH (ti:TaskInstance)-[:CONTAINS]->(:Event)-[:CORR]->(n:{entity})
                 RETURN DISTINCT ti, n",
                "WITH ti, n
                    CREATE (ti)-[:CORR]->(n)",
                {{batchSize:100}})'''
        run_query(driver, query_correlate_ti_to_entity)
        performance_recorder.record_performance(f'correlate_ti_to_entity_({entity[0]})')

        # create DF-relationships between task instances
        query_create_df_ti = f'''
            CALL apoc.periodic.iterate(
                "MATCH (n:{entity})
                 MATCH (ti:TaskInstance)-[:CORR]->(n)
                 WITH n, ti AS nodes ORDER BY ti.start_time, ID(ti)
                 WITH n, COLLECT (nodes) as nodeList
                 UNWIND range(0, size(nodeList)-2) AS i
                 RETURN n, nodeList[i] as ti_first, nodeList[i+1] as ti_second",
                "WITH n, ti_first, ti_second
                    MERGE (ti_first)-[df:DF_TI_{entity}]->(ti_second)",
                {{batchSize:100}})'''
        run_query(driver, query_create_df_ti)
        performance_recorder.record_performance(f'create_df_ti_({entity})')


def set_task_instance_ids(driver, performance_recorder):
    # set task instance ids
    query_set_ti_ids = f'''
        CALL apoc.periodic.iterate(
        "MATCH (ti:TaskInstance)
         WITH DISTINCT ti.variant AS variant, count(*) AS count
         ORDER BY count DESC
         WITH collect(variant) as variants
         UNWIND range(0, size(variants)-1) as pos
         WITH variants[pos] AS variant, pos+1 AS rank
         MATCH (ti:TaskInstance) WHERE ti.variant = variant
         RETURN ti, rank",
        "WITH ti, rank
         SET ti.ID = rank",
        {{batchSize:100}})'''
    run_query(driver, query_set_ti_ids)
    performance_recorder.record_performance('set_task_instance_id')


def run_query(driver, query):
    print(query)
    with driver.session() as session:
        result = session.run(query).single()
        if result:
            return result.value()
        else:
            return None
