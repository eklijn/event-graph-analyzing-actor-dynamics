#####################################################
############# EXPLANATION OF SETTINGS ###############
#####################################################

# SETTING FOR PREPROCESSING
# if no preprocessing is done, empty strings can be assigned
filename = {}  # name of the csv file to build the graph from
column_names = {}  # names of the columns in the csv file for [case, activity, timestamp, resource(, lifecycle)] (in this order)
separator = {}  # separator used in csv file
timestamp_format = {}  # format of the timestamps recorded in the csv file

# GRAPH SETTINGS
password = {}  # password of neo4j database
actor_label = {}  # labels used in the graph for: actor node and df_actor edge
case_label = {}  # labels used in the graph for: case node and df_case edge
case_attr_labels = {}  # labels used for process instance attributes

# SETTINGS FOR VISUALIZING:
name_data_set = {}  # name of the data set, used for configuring the node labels when visualizing subgraphs (only available for bpic2014 and bpic2017)

#####################################################
############ CONFIGURATION OF SETTINGS ##############
#####################################################

# -------------- BPIC 2017 SETTINGS -----------------

for graph in ["bpic2017_susp_res"]:
    filename[graph] = "bpic2017"
    name_data_set[graph] = "bpic2017"
    column_names[graph] = ["case", "event", "time", "org:resource", "lifecycle:transition"]
    separator[graph] = ","
    timestamp_format[graph] = "%Y/%m/%d %H:%M:%S.%f"
    password[graph] = "bpic2017"

    actor_label[graph] = "Resource"
    case_label[graph] = "CaseAWO"

    case_attr_labels[graph] = ["ApplicationType", "LoanGoal", "RequestedAmount", "OfferID"]
    if graph in ["bpic2017_case_attr", "bpic2017_ek_offer_id", "bpic2017_susp_res"]:
        column_names[graph] += case_attr_labels[graph]

# -------------- BPIC 2014 SETTINGS -----------------

for graph in ["bpic2014_single_ek"]:
    filename[graph] = "bpic2014_incident_activity"
    name_data_set[graph] = "bpic2014"
    column_names[graph] = ["Incident ID", "IncidentActivity_Type", "DateStamp", "Assignment Group"]
    separator[graph] = ";"
    timestamp_format[graph] = "%d-%m-%Y %H:%M:%S"

    password[graph] = "bpic2014"

    actor_label[graph] = "Resource"  # default: needs to be adapted
    case_label[graph] = "Case"  # default: needs to be adapted

# -------------- OPERATORS SETTINGS -----------------

for graph in ["operators"]:
    filename[graph] = "data_Omron"
    name_data_set[graph] = "operators"
    column_names[graph] = ["product_id", "event", "completeTime", "operator"]
    separator[graph] = ","
    timestamp_format[graph] = "%Y/%m/%d %H:%M:%S.%f"
    password[graph] = "operators"

    actor_label[graph] = "Resource"  # default: needs to be adapted
    case_label[graph] = "Case"  # default: needs to be adapted
