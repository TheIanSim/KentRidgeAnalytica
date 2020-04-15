#Reads original CSV inputs and runs "what if scenerios"
#Generates new CSV to simulate on

import csv
import pandas as pd

#Reads Nodes

file1 = "../Database 1A.csv"
file2 =  "../Database 1B.csv"
file3 = "Gephi_Centrality_Scores.csv"
BAD_GUYS = [160, 6, 51, 178]
BAD_GUYS_MODULARITY_CLASS = [0,5,2,10]
GOOD_GUYS = [8, 50, 32, 63, 45, 109, 167, 86]

def storeCSV(file1, file2):
    with open(file1, mode='r') as infile:
        reader = csv.reader(infile)
        nodes = {}
        for rows in reader:
            k = rows[0]
            if(k == "User ID"):
                v = [rows[0],rows[1], rows[2], rows[3],rows[4], rows[5], rows[6]]
            else:
                v = [int(rows[0]),rows[1], rows[2], rows[3],rows[4], rows[5], rows[6]]
            nodes[k] = v
        #print(nodes)

    with open(file2, mode='r') as infile:
        reader = csv.reader(infile)
        edges = {}
        for rows in reader:
            source = rows[0]; target = rows[1]; messages = rows[2]
            #undirected graph assumption
            #Ignore first row
            if source != "Source":
                if source in edges:
                    if target not in edges[source]:
                        edges[source][target] =int(messages)
                else:
                    edges[source] = {target: int(messages)}
                
                if target in edges:
                    if source not in edges[target]:
                        edges[target][source] = int(messages)
                else:
                    edges[target] = {source: int(messages)}
    return nodes, edges

nodes, edges = storeCSV(file1, file2)

#Calculate new field for node = Average Conversation Messages
def calculate_average_messages(nodes, edges):
    for row in nodes:
        if row == "User ID":
            nodes[row].append("Average Conversation")

        else:
            if row in edges:
                averageMessages = round(sum(edges[row].values())/len(edges[row]))
                nodes[row].append(averageMessages)
    return nodes, edges

nodes, edges = calculate_average_messages(nodes, edges)

#What ifs
#Q1 Most central node in each cluster is removed excluding
    #Step 1: calculate most central nodes to remove
    #Determined by Total Centrality Score and Average Messages'
    #Assumes data is sorted

def read_centrality_scores_table(file3, nodes):
    centrality_table = pd.read_csv(file3)
    #drop unnecessary columns to cut down data usage
    keep_columns = ["Id", "component number", "modularity class","Degree", "Total Centrality Score"]
    centrality_table = centrality_table[keep_columns]
    nodes_df = pd.DataFrame.from_dict(nodes, orient='index', columns = [
        "Id","Gender", "Age", "Horoscope", "Language (Native)", "Locale (Current)", "Education (Attained)", "Average Conversation"])
    nodes_df = nodes_df[nodes_df.Gender != 'Gender'] #drop first row
    nodes_df['Id'] = nodes_df['Id'].astype(int) #force index into <class 'pandas.core.indexes.range.RangeIndex'>
    nodes_df = nodes_df.reset_index(drop=True)
    nodes_df["Average Conversation"] = nodes_df["Average Conversation"].astype(int)
    nodes_df = nodes_df[["Average Conversation"]]
    centrality_table = centrality_table.merge(nodes_df, how = "left", left_index = True, right_index = True)
    #print(centrality_table)
    return centrality_table

centrality_table = read_centrality_scores_table(file3, nodes)

def calculate_external_cluster_connections(edges, centrality_table):
    external_clusters = []
    external_friends = []
    for i in range(len(centrality_table)) : 
        if centrality_table.loc[i,"component number"]!= 0:
            external_clusters.append(0)
            external_friends.append(0)
        else:
            node_id = str(centrality_table.loc[i,"Id"])
            cluster_id = centrality_table.loc[i,"modularity class"]
            num_connections = 0
            cluster_connection_list = []
            neighbour_list = edges[node_id]
            for neighbour in neighbour_list:
                neighbour_id = int(neighbour)
                neighbour_cluster = centrality_table.iloc[neighbour_id]['modularity class']
                if neighbour_cluster!= cluster_id:
                    num_connections+=1
                    if neighbour_cluster not in cluster_connection_list:
                        cluster_connection_list.append(neighbour_cluster)
            external_clusters.append(len(cluster_connection_list))
            external_friends.append(num_connections)
    
    centrality_table["external_cluster_num"] = external_clusters
    centrality_table ["external_friends_num"] = external_friends
    #print(centrality_table)
    return centrality_table

centrality_table = calculate_external_cluster_connections(edges, centrality_table)

#Assumes good guys are in different clusters
def pick_nodes_per_cluster(GOOD_GUYS, centrality_table):
    removeNodesList = []
    #filter component class 1, 2 as they are disjointed from the main graph
    centrality_table =  centrality_table[ centrality_table['component number']==0]
    #print(centrality_table)
    cluster_list= centrality_table["modularity class"].unique()
    for cluster in cluster_list:
        filtered_table =  centrality_table[centrality_table['modularity class']==cluster]       
        rank_cols = ['Total Centrality Score', "Average Conversation",'external_cluster_num', 'external_friends_num']
        filtered_table['Rank'] = filtered_table.sort_values(rank_cols, ascending=False).groupby(rank_cols, sort=False).ngroup() + 1
        #Avoids removing good guy / bad guy nodes.
        #Removes 1 node per modularity class
        if filtered_table.iloc[0].Id not in BAD_GUYS and filtered_table.iloc[0].Id not in GOOD_GUYS:
            removeNodesList.append(filtered_table.iloc[1].Id)
        else:
            not_yet_removed = True
            while not_yet_removed:
                for i in range (1,len(filtered_table)):
                    if filtered_table.iloc[i].Id not in BAD_GUYS and filtered_table.iloc[i].Id not in GOOD_GUYS:
                        removeNodesList.append(filtered_table.iloc[i].Id)
                        break
                not_yet_removed = False
           
    remove_node_centrality  = centrality_table[centrality_table['Id'].isin(removeNodesList)]
    #print(remove_node_centrality) 
    return removeNodesList, remove_node_centrality

removeNodesList, remove_node_centrality = pick_nodes_per_cluster(BAD_GUYS, centrality_table)

#to see the impact of node removal, it could be best seen by simply removing the edges of the nodes
#method writes a csv called removed_central_nodes
#ensure no duplicates
def remove_nodes(removeNodesList, file2):
    fieldnames = ['Source', 'Target',"Conversation Messages"]
    written_dict = {}
    with open('removed_central_nodes.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        with open(file1, mode='r') as infile:
            reader = csv.reader(infile)
            for rows in reader:
                id = rows[0]
                if id== "User ID" or int(id) not in removeNodesList:
                    writer.writerow(rows)
    with open('removed_central_edges.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        with open(file2, mode='r') as infile:
            reader = csv.reader(infile)
            for rows in reader:
                source = rows[0]; target = rows[1]; messages = rows[2]
                if rows[0] == "Source" or ((int(source) not in removeNodesList) and (int(target) not in removeNodesList)):
                    if rows[0] == "Source":
                        writer.writerow(rows)
                    else:
                        source = int(rows[0]); target = int(rows[1]); messages = int(rows[2])
                        if source not in written_dict:
                            if target not in written_dict:
                                written_dict[source] = [target]
                                writer.writerow(rows)
                            elif source not in written_dict[target]:
                                written_dict[target].append(source)
                                writer.writerow(rows)
                        else:
                            if target not in written_dict[source]:
                                if target not in written_dict or source not in written_dict[target]: #no key
                                    written_dict[source].append(target)
                                    writer.writerow(rows)
remove_nodes(removeNodesList, file2)
