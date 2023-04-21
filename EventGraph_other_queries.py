import pandas as pd
from neo4j import GraphDatabase


class EventGraph:
    def __init__(self, password, entity_labels):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", password))
        self.entity_labels = entity_labels

    def query_events_subset_filter(self, variant_id, period_filter, resources=""):
        variant_filter = f"WHERE ti.ID = {variant_id}"
        if resources != "":
            resource_filter = f"AND ti.rID IN {resources}"
        else:
            resource_filter = ""
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) {variant_filter} {period_filter} {resource_filter}
                WITH DISTINCT ti.cID AS case
                MATCH (e:Event {{case: case}})
                WITH e.case AS case, e.timestamp AS timestamp, e.resource AS resource, e.activity_lifecycle AS action
                RETURN case, action, timestamp, resource ORDER BY case, timestamp ASC
                '''
            result = session.run(q)
            df_event_log_filtered = pd.DataFrame([dict(record) for record in result])
            return df_event_log_filtered

    def query_variants(self, min_frequency):
        with self.driver.session() as session:
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
            q = f'''
                MATCH (ti:TaskInstance) WHERE EXISTS(ti.cluster)
                WITH ti.path AS path, ti.ID AS ID, ti.{decomposed_property} AS decomposed_property, ti.cluster AS cluster
                WITH DISTINCT path, decomposed_property, ID, cluster, COUNT (*) AS frequency
                RETURN cluster, ID, path, decomposed_property, frequency
                '''
            result = session.run(q)
            df_variants_in_cluster_decomposed = pd.DataFrame([dict(record) for record in result])
        return df_variants_in_cluster_decomposed

    def query_variant_frequencies_from_variant_ids(self, variant_ids):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.ID IN {variant_ids}
                WITH ti.ID AS variant
                WITH DISTINCT variant, COUNT (*) AS frequency
                RETURN variant, frequency ORDER BY frequency DESC
                '''
            # print(q)
            result = session.run(q)
            df_variant_variants = pd.DataFrame([dict(record) for record in result])
        return df_variant_variants

    def query_variant_frequencies_subset_filter(self, subset_filter):
        with self.driver.session() as session:
            q = f'''
                MATCH (e:Event)<-[:CONTAINS]-(ti:TaskInstance) {subset_filter[1]}
                WITH DISTINCT ti
                WITH ti.path AS path, ti.ID AS ID
                WITH DISTINCT ID, COUNT (*) AS {subset_filter[0]}
                RETURN ID, {subset_filter[0]}
                '''
            # print(q)
            result = session.run(q)
            df_subset_variant_frequencies = pd.DataFrame([dict(record) for record in result])
        return df_subset_variant_frequencies

    def query_cluster_variant_frequencies_subset_filter(self, subset_filter, variant_ids, cluster):
        if subset_filter[1] == "":
            variant_id_filter = f"WHERE ti.ID IN {variant_ids}"
        else:
            variant_id_filter = f"AND ti.ID IN {variant_ids}"
        with self.driver.session() as session:
            q = f'''
                MATCH (e:Event)<-[:CONTAINS]-(ti:TaskInstance) {subset_filter[1]} {variant_id_filter}
                WITH DISTINCT ti
                WITH ti.path AS path, ti.ID AS ID
                WITH DISTINCT ID, COUNT (*) AS {subset_filter[0]}_{cluster}
                RETURN ID, {subset_filter[0]}_{cluster}
                '''
            print(q)
            result = session.run(q)
            df_subset_variant_frequencies_in_cluster = pd.DataFrame([dict(record) for record in result])
        return df_subset_variant_frequencies_in_cluster

    def query_resource_frequencies_from_variant_id(self, variant_id):
        q = f'''
            MATCH (ti:TaskInstance) WHERE ti.ID = {variant_id}
            WITH ti.rID AS resource
            RETURN DISTINCT resource, COUNT (*) AS frequency
            '''
        # print(q)
        result = run_query(self.driver, q)
        df_resource_frequencies = pd.DataFrame([dict(record) for record in result])
        return df_resource_frequencies

    def query_resource_list_from_variant_ids(self, variant_ids):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.ID IN {variant_ids}
                WITH ti.rID AS resource
                RETURN DISTINCT resource
                '''
            # print(q)
            result = session.run(q)
            resources = []
            for record in result:
                resources.append(record['resource'])
        return resources

    def query_resource_list_from_variant_ids(self, variant_ids, min_frequency):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.ID IN {variant_ids}
                WITH DISTINCT ti.rID AS resource, count(*) AS frequency 
                WHERE frequency > {min_frequency}
                RETURN resource, frequency
                '''
            # print(q)
            result = session.run(q)
            resources = []
            for record in result:
                resources.append(record['resource'])
        return resources

    def query_resource_list_from_variant_ids_subset_filter(self, variant_ids, min_frequency, subset_filter):
        if subset_filter == "":
            variant_id_filter = f"WHERE ti.ID IN {variant_ids}"
        else:
            variant_id_filter = f"AND ti.ID IN {variant_ids}"
        with self.driver.session() as session:
            q = f'''
                MATCH (e:Event)<-[:CONTAINS]-(ti:TaskInstance) {subset_filter} {variant_id_filter} 
                WITH DISTINCT ti
                WITH DISTINCT ti.rID AS resource, count(*) AS frequency 
                WHERE frequency > {min_frequency}
                RETURN resource, frequency
                '''
            # print(q)
            result = session.run(q)
            resources = []
            for record in result:
                resources.append(record['resource'])
        return resources

    def query_resource_list_from_variant_ids_subset_filter_analysis_filter(self, variant_ids, min_frequency,
                                                                           subset_filter, analysis_filter):
        if subset_filter == "":
            variant_id_filter = f"WHERE ti.ID IN {variant_ids}"
        else:
            variant_id_filter = f"AND ti.ID IN {variant_ids}"
        with self.driver.session() as session:
            q = f'''
                MATCH (e:Event)<-[:CONTAINS]-(ti:TaskInstance) {subset_filter} {variant_id_filter} {analysis_filter}
                WITH DISTINCT ti
                WITH DISTINCT ti.rID AS resource, count(*) AS frequency 
                WHERE frequency > {min_frequency}
                RETURN resource, frequency
                '''
            # print(q)
            result = session.run(q)
            resources = []
            for record in result:
                resources.append(record['resource'])
        return resources

    def query_resource_frequency_from_variant_id(self, resource, variant_id):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.rID = "{resource}" AND ti.ID = {variant_id}
                RETURN count(ti) AS count
                '''
            # print(q)
            result = session.run(q)
            resource_frequency = result.single()[0]
        return resource_frequency

    def query_resource_frequency_from_variant_ids(self, resource, variant_ids):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.rID = "{resource}" AND ti.ID IN {variant_ids}
                RETURN count(ti) AS count
                '''
            # print(q)
            result = session.run(q)
            resource_frequency = result.single()[0]
        return resource_frequency

    def query_resource_frequency_from_variant_id_subset_filter(self, resource, variant_id, subset_filter):
        if subset_filter == "":
            variant_id_filter = f"WHERE ti.ID = {variant_id}"
        else:
            variant_id_filter = f"AND ti.ID = {variant_id}"
        with self.driver.session() as session:
            q = f'''
                MATCH (e:Event)<-[:CONTAINS]-(ti:TaskInstance) {subset_filter} {variant_id_filter} AND ti.rID = "{resource}" 
                WITH DISTINCT ti
                RETURN count(ti) AS count
                '''
            # print(q)
            result = session.run(q)
            resource_frequency = result.single()[0]
        return resource_frequency

    def query_resource_frequency_from_variant_id_subset_filter_analysis_filter(self, resource, variant_id,
                                                                               subset_filter, analysis_filter):
        if subset_filter == "":
            variant_id_filter = f"WHERE ti.ID = {variant_id}"
        else:
            variant_id_filter = f"AND ti.ID = {variant_id}"
        with self.driver.session() as session:
            q = f'''
                MATCH (e:Event)<-[:CONTAINS]-(ti:TaskInstance) {subset_filter} {variant_id_filter} {analysis_filter}
                AND ti.rID = "{resource}"
                WITH DISTINCT ti
                RETURN count(ti) AS count
                '''
            # print(q)
            result = session.run(q)
            resource_frequency = result.single()[0]
        return resource_frequency

    def query_resource_group_frequency_from_variant_id(self, resource_group, variant_id):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.rID IN {resource_group} AND ti.ID = {variant_id}
                RETURN count(ti) AS count
                '''
            # print(q)
            result = session.run(q)
            resource_group_frequency = result.single()[0]
        return resource_group_frequency

    def query_resource_group_frequency_from_variant_id_subset_filter(self, resource_group, variant_id, subset_filter):
        if subset_filter == "":
            variant_id_filter = f"WHERE ti.ID = {variant_id}"
        else:
            variant_id_filter = f"AND ti.ID = {variant_id}"
        with self.driver.session() as session:
            q = f'''
                MATCH (e:Event)<-[:CONTAINS]-(ti:TaskInstance) {subset_filter} {variant_id_filter} AND ti.rID IN {resource_group}
                WITH DISTINCT ti
                RETURN count(ti) AS count
                '''
            # print(q)
            result = session.run(q)
            resource_group_frequency = result.single()[0]
        return resource_group_frequency

    def query_resource_group_frequency_from_variant_id_subset_filter_analysis_filter(self, resource_group, variant_id,
                                                                                     subset_filter, analysis_filter):
        if subset_filter == "":
            variant_id_filter = f"WHERE ti.ID = {variant_id}"
        else:
            variant_id_filter = f"AND ti.ID = {variant_id}"
        with self.driver.session() as session:
            q = f'''
                MATCH (e:Event)<-[:CONTAINS]-(ti:TaskInstance) {subset_filter} {variant_id_filter} {analysis_filter}
                AND ti.rID IN {resource_group} 
                WITH DISTINCT ti
                RETURN count(ti) AS count
                '''
            # print(q)
            result = session.run(q)
            resource_group_frequency = result.single()[0]
        return resource_group_frequency

    def query_resource_total_frequency(self, resource):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.rID = "{resource}"
                RETURN count(ti)
                '''
            # print(q)
            result = session.run(q)
            resource_total_frequency = result.single()[0]
        return resource_total_frequency

    def query_resource_total_frequency_subset_filter(self, resource, subset_filter):
        if subset_filter == "":
            resource_id_filter = f"WHERE ti.rID = \"{resource}\""
        else:
            resource_id_filter = f"AND ti.rID = \"{resource}\""
        with self.driver.session() as session:
            q = f'''
                MATCH (e:Event)<-[:CONTAINS]-(ti:TaskInstance) {subset_filter} {resource_id_filter}
                WITH DISTINCT ti
                RETURN count(ti)
                '''
            # print(q)
            result = session.run(q)
            resource_total_frequency = result.single()[0]
        return resource_total_frequency

    # def query_resource_variant_ids_in_variant_ids(self, resource, variant_ids):
    #     with self.driver.session() as session:
    #         q = f'''
    #             MATCH (ti:TaskInstance) WHERE ti.ID IN {variant_ids} AND ti.rID = "{resource}"
    #             RETURN DISTINCT ti.ID AS ID ORDER BY ID ASC
    #             '''
    #         result = session.run(q)
    #         resource_cluster_ids = []
    #         for record in result:
    #             resource_cluster_ids.append(record['ID'])
    #     return resource_cluster_ids

    def query_variant_frequency_subset_filter(self, variant_id, subset_filter):
        if subset_filter == "":
            variant_id_filter = f"WHERE ti.ID = {int(variant_id)}"
        else:
            variant_id_filter = f"AND ti.ID = {int(variant_id)}"
        with self.driver.session() as session:
            q = f'''
                MATCH (e:Event)<-[:CONTAINS]-(ti:TaskInstance) {subset_filter} {variant_id_filter}
                WITH DISTINCT ti
                RETURN count(ti)
                '''
            result = session.run(q)
            total_frequency = result.single()[0]
        return total_frequency

    def query_requested_amounts(self):
        with self.driver.session() as session:
            q = f'''
                MATCH (e:Event)
                WITH e.RequestedAmount as req_amount, e.case AS case
                RETURN DISTINCT case, req_amount
                '''
            result = session.run(q)
            requested_amounts = []
            for record in result:
                requested_amounts.append(float(record['req_amount']))
        return requested_amounts

######################################################
##################### STATISTICS #####################
######################################################

    def query_variant_frequency_variant_subset(self, variant_ids):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.ID IN {variant_ids}
                RETURN count(ti)
                '''
            result = session.run(q)
            total_variant_frequency = result.single()[0]
        return total_variant_frequency

    def query_resource_frequency_variant_subset(self, variant_ids):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.ID IN {variant_ids}
                WITH DISTINCT ti.rID AS resource
                RETURN count(resource)
                '''
            result = session.run(q)
            total_resource_frequency = result.single()[0]
        return total_resource_frequency

    def query_durations_variant_subset(self, variant_ids):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.ID IN {variant_ids}
                WITH duration.inSeconds(ti.start_time, ti.end_time) AS duration
                RETURN duration
                '''
            result = session.run(q)
            durations = []
            for record in result:
                duration = record["duration"]
                duration_seconds = (duration.hours_minutes_seconds[0] * 3600) + \
                                   (duration.hours_minutes_seconds[1] * 60) + duration.hours_minutes_seconds[2]
                durations.append(duration_seconds)
        return durations

######################################################
##################### #PLOTTING ######################
######################################################

    def query_task_instances_per_date_per_resource_from_variant_id(self, variant_id, resource, unit):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.ID = {variant_id} AND ti.rID = "{resource}"
                WITH date.truncate('{unit}', ti.start_time) AS date, 
                ti.ID AS variant, count(ti.ID) AS {resource}
                RETURN date, {resource} ORDER BY date ASC
                '''
            # print(q)
            result = session.run(q)
            df_task_per_date = pd.DataFrame([dict(record) for record in result]).fillna(0)
            # df_task_per_date = pd.DataFrame([dict(record) for record in result]).pivot(index='date',
            #                                                                            columns=variant_id).fillna(0)
            # df_task_per_date.columns = [variant_id]
            df_task_per_date.index = pd.DatetimeIndex(df_task_per_date['date'].astype(str))
            df_task_per_date.drop(['date'], axis=1, inplace=True)
            return df_task_per_date

    def query_task_instances_per_date_from_variant_id(self, variant_id):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.ID = {variant_id}
                WITH date.truncate('week', ti.start_time) AS date, 
                ti.ID AS variant, count(ti.ID) AS variant_{variant_id}
                RETURN date, variant_{variant_id} ORDER BY date ASC
                '''
            # print(q)
            result = session.run(q)
            df_task_per_date = pd.DataFrame([dict(record) for record in result]).fillna(0)
            # df_task_per_date = pd.DataFrame([dict(record) for record in result]).pivot(index='date',
            #                                                                            columns=variant_id).fillna(0)
            # df_task_per_date.columns = [variant_id]
            df_task_per_date.index = pd.DatetimeIndex(df_task_per_date['date'].astype(str))
            df_task_per_date.drop(['date'], axis=1, inplace=True)
            return df_task_per_date

    def query_task_instances_per_date_from_variant_ids(self, variant_ids):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance) WHERE ti.ID IN {variant_ids}
                WITH date.truncate('week', ti.start_time) AS date, 
                ti.ID AS variant, count(ti.ID) AS count
                RETURN date, variant, count ORDER BY date ASC
                '''
            # print(q)
            result = session.run(q)
            # df_task_per_date = pd.DataFrame([dict(record) for record in result]).fillna(0)
            df_task_per_date = pd.DataFrame([dict(record) for record in result]).pivot(index='date',
                                                                                       columns='variant').fillna(0)
            df_task_per_date.columns = df_task_per_date.columns.droplevel(0)
            df_task_per_date.index = pd.DatetimeIndex(df_task_per_date.index.astype(str))
            # df_task_per_date.drop(['date'], axis=1, inplace=True)
            return df_task_per_date

    def query_case_durations_from_variant_ids(self, variant_ids):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance)-[:CORR]->(n:Entity)<-[:CORR]-(e:Event) 
                    WHERE ti.ID IN {variant_ids} AND n.EntityType = "case"
                WITH DISTINCT e.case AS case, duration.inSeconds(MIN(e.timestamp), MAX(e.timestamp)).minutes AS duration
                RETURN duration
                '''
            result = session.run(q)
            durations = []
            for record in result:
                duration = record["duration"]/60/24
                durations.append(duration)
        return durations

    def query_case_durations_outside_variant_ids(self, variant_ids):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti:TaskInstance)-[:CORR]->(n:Entity)<-[:CORR]-(e:Event) 
                    WHERE NOT ti.ID IN {variant_ids} AND n.EntityType = "case"
                WITH DISTINCT e.case AS case, duration.inSeconds(MIN(e.timestamp), MAX(e.timestamp)).minutes AS duration
                RETURN duration
                '''
            result = session.run(q)
            durations = []
            for record in result:
                duration = record["duration"]/60/24
                durations.append(duration)
        return durations

    def query_case_durations_from_variant_ids_two_sets(self, variant_ids_1, variant_ids_2):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti1:TaskInstance)-[:CORR]->(n:Entity)<-[:CORR]-(ti2:TaskInstance)
                    WHERE ti1.ID IN {variant_ids_1} AND ti2.ID IN {variant_ids_2} AND n.EntityType = "case"
                MATCH (e:Event)-[:CORR]->(n:Entity)
                WITH DISTINCT e.case AS case, duration.inSeconds(MIN(e.timestamp), MAX(e.timestamp)).minutes AS duration
                RETURN duration
                '''
            result = session.run(q)
            durations = []
            for record in result:
                duration = record["duration"]/60/24
                durations.append(duration)
        return durations

    def query_case_durations_from_variant_ids_three_sets(self, variant_ids_1, variant_ids_2, variant_ids_3):
        with self.driver.session() as session:
            q = f'''
                MATCH (ti1:TaskInstance) WHERE ti1.ID IN {variant_ids_1}
                MATCH (ti2:TaskInstance) WHERE ti2.ID IN {variant_ids_2} AND ti2.cID = ti1.cID  AND ID(ti1) <> ID(ti2)
                MATCH (ti3:TaskInstance) WHERE ti3.ID IN {variant_ids_3} AND ti3.cID = ti2.cID
                MATCH (n:Entity {{EntityType: 'case'}}) WHERE n.ID = ti3.cID
                MATCH (e:Event)-[:CORR]->(n)
                WITH DISTINCT e.case AS case, duration.inSeconds(MIN(e.timestamp), MAX(e.timestamp)).minutes AS duration
                RETURN duration
                '''
            result = session.run(q)
            durations = []
            for record in result:
                duration = record["duration"]/60/24
                durations.append(duration)
        return durations


def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query).single()
        if result:
            return result
        else:
            return None
