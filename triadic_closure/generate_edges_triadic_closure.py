import csv
import numpy as np

EDGE_TABLE_FILE = '../Database 1B.csv'
NUMBER_OF_NODES = 180
NEW_EDGE_TABLE_FILE = './Edge_Table_Triadic_Closure.csv'

def get_edge_list():
    with open(EDGE_TABLE_FILE, "r") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader, None) # remove the header row
        edge_list = list(reader) # list of lists
        edge_list = [[int(x) for x in edge] for edge in edge_list]
        return edge_list

def get_adj_matrix(edge_list):
    adj_matrix = [[0] * NUMBER_OF_NODES for _ in range(NUMBER_OF_NODES)]
    for source, target, _ in edge_list:
        adj_matrix[source][target] = 1
        adj_matrix[target][source] = 1
    return adj_matrix

def filter_for_strong_edges(edge_list, percentile=90):
    num_messages_per_link = [edge[-1] for edge in edge_list]
    num_messages_threshold = np.percentile(num_messages_per_link, percentile)
    return [edge for edge in edge_list if edge[-1] >= num_messages_threshold]

def get_adj_list(edges):
    adj_list = {}
    for source, target, num_msgs in edges:
        if source not in adj_list: adj_list[source] = {}
        if target not in adj_list: adj_list[target] = {}
        adj_list[source][target] = num_msgs
        adj_list[target][source] = num_msgs
    return adj_list

def get_new_links_via_triadic_closure(adj_list, adj_matrix):
    new_links = {}
    for neighbours in adj_list.values():
        if len(neighbours) <= 1: continue # ensure that this node has >1 strong link

        neighbours_list = list(neighbours.items())
        for i in range(len(neighbours_list)-1):
            for j in range(i+1, len(neighbours_list)):
                n1, m1 = neighbours_list[i]
                n2, m2 = neighbours_list[j]
                if adj_matrix[n1][n2] == 1: continue # ensure that link does not already exist
                
                node_pair = (n1, n2) if n1 < n2 else (n2, n1)
                if node_pair not in new_links: new_links[node_pair] = 0
                estimated_msg_cnt = round(np.mean([m1, m2]) * 0.3, 2)
                new_links[node_pair] += estimated_msg_cnt
    
    new_links_list = [[pair[0], pair[1], num_msg] for pair, num_msg in new_links.items()]
    return new_links_list

def create_new_edge_table(new_links):
    with open(NEW_EDGE_TABLE_FILE, 'w') as fw:
        writer = csv.writer(fw)
        with open(EDGE_TABLE_FILE, "r") as fr:
            reader = csv.reader(fr, delimiter=",")
            writer.writerows(list(reader))
        writer.writerows(new_links)

def main():
    edge_list = get_edge_list()
    adj_matrix = get_adj_matrix(edge_list)
    strong_edges = filter_for_strong_edges(edge_list=edge_list, percentile=75)
    strong_edges_adj_list = get_adj_list(strong_edges)
    new_links = get_new_links_via_triadic_closure(strong_edges_adj_list, adj_matrix)
    create_new_edge_table(new_links)

if __name__ == "__main__":
    main()
