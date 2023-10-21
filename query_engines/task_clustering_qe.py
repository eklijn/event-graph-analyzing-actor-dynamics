import pandas as pd
from neo4j import GraphDatabase


class ClusterQueryEngine:
    def __init__(self, password):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", password))

    def query_variants(self, min_frequency):
        with self.driver.session() as session:
            # language=Cypher
            q = f'''
                MATCH (ti:TaskInstance)
                WITH ti.variant AS variant, ti.ID AS ID, size(ti.variant) AS variant_length
                WITH DISTINCT variant, variant_length, ID, COUNT (*) AS frequency WHERE frequency >= {min_frequency}
                RETURN variant, variant_length, ID, frequency
                '''
            # print(q)
            result = session.run(q)
            df_variants = pd.DataFrame([dict(record) for record in result])
        return df_variants

def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query).single()
        if result:
            return result
        else:
            return None
