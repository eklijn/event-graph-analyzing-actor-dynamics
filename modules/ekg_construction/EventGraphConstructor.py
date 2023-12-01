import pandas as pd
from performance.PerformanceRecorder import PerformanceRecorder
from neo4j import GraphDatabase


class EventGraphConstructor:

    def __init__(self, password, import_directory, filename, actor_label, case_label):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", password))
        self.filename = filename
        self.file_name = f'{filename}.csv'
        print("Load data from "+self.file_name)
        self.csv_data_set = pd.read_csv(f'{import_directory}{filename}.csv')
        self.event_attributes = self.csv_data_set.columns
        self.actor_label = actor_label
        self.case_label = case_label

    def construct(self):
        # create performance recorder
        pr = PerformanceRecorder(self.filename, 'constructing_event_graph')

        query_clean_db_relations = f'MATCH ()-[rel]->() CALL {{WITH rel DELETE rel}} IN TRANSACTIONS OF 1000 ROWS'
        run_query(self.driver, query_clean_db_relations)
        pr.record_performance(f"clean_DB_relations")

        query_clean_db_nodes = f'MATCH (n) CALL {{WITH n DELETE n}} IN TRANSACTIONS OF 1000 ROWS'
        run_query(self.driver, query_clean_db_nodes)
        pr.record_performance(f"clean_DB_nodes")

        query_create_event_nodes = f'LOAD CSV WITH HEADERS FROM \"file:///{self.file_name}\" as line\n'
        query_create_event_nodes += 'CALL {\n'
        query_create_event_nodes += ' WITH line\n'
        for attr in self.event_attributes:
            if attr == 'idx':
                value = f'toInteger(line.{attr})'
            elif attr in ['timestamp', 'start', 'end']:
                value = f'datetime(line.{attr})'
            else:
                value = 'line.' + attr
            if self.event_attributes.get_loc(attr) == 0:
                new_line = f' CREATE (e:Event {{{attr}: {value},'
            elif self.event_attributes.get_loc(attr) == len(self.event_attributes) - 1:
                new_line = f' {attr}: {value}, LineNumber: linenumber()}})'
            else:
                new_line = f' {attr}: {value},'
            query_create_event_nodes = query_create_event_nodes + new_line
        query_create_event_nodes += '\n'
        query_create_event_nodes += '} IN TRANSACTIONS OF 1000 ROWS;'
        run_query(self.driver, query_create_event_nodes)
        pr.record_performance("import_event_nodes")

        # query_filter_events = f'MATCH (e:Event) WHERE e.lifecycle in ["SUSPEND","RESUME", "ATE_ABORT", "SCHEDULE", "WITHDRAW"] DELETE e'
        # query_filter_events = f'CALL {{MATCH (e:Event) WHERE e.lifecycle in ["SUSPEND","RESUME"] DELETE e}} IN TRANSACTIONS OF 1000 ROWS'
        # run_query(self.driver, query_filter_events)
        # pr.record_performance(f"filter_events_SUSPEND_RESUME")

        construct_from_events(self.driver, self.actor_label, self.case_label, pr)

        pr.record_total_performance()
        pr.save_to_file()


def construct_from_events(driver, actor_label, case_label, performance_recorder):
    for entity in [actor_label, case_label]:
        query_create_entity_nodes = f'''
            CALL apoc.periodic.iterate(
            "MATCH (e:Event) WITH DISTINCT e.{entity} AS id 
            RETURN id",
            "WITH id
                CREATE (n:Entity:{entity} {{sysId:id}})",
            {{batchSize:1000}})'''
        run_query(driver, query_create_entity_nodes)
        performance_recorder.record_performance(f"create_entity_nodes_({entity})")

        query_correlate_events_to_entity = f'''
            CALL apoc.periodic.iterate(
            "MATCH (e:Event) WHERE e.{entity} IS NOT NULL 
            MATCH (n:{entity}) WHERE e.{entity} = n.sysId RETURN e,n",
            "WITH e,n
                CREATE (e)-[:CORR]->(n)",
            {{batchSize:1000}})'''
        run_query(driver, query_correlate_events_to_entity)
        performance_recorder.record_performance(f"correlate_events_to_{entity}s")

        query_create_directly_follows = f'''
            CALL apoc.periodic.iterate(
                "MATCH (n:{entity})
                MATCH (n)<-[:CORR]-(e:Event)
                WITH n, e AS nodes ORDER BY e.timestamp, ID(e)
                WITH n, collect(nodes) AS event_node_list
                UNWIND range(0, size(event_node_list)-2) AS i
                RETURN n, event_node_list[i] AS e1, event_node_list[i+1] AS e2",
            "WITH n,e1,e2
                MERGE (e1)-[df:DF_{entity}]->(e2)",
            {{batchSize:100}})'''
        run_query(driver, query_create_directly_follows)
        performance_recorder.record_performance(f"create_directly_follows_({entity})")


def run_query(driver, query):
    print(query)
    with driver.session() as session:
        result = session.run(query).single()
        if result:
            return result.value()
        else:
            return None
