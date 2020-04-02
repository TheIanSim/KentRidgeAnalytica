#from __future__ import annotations
from collections import defaultdict
import math
import pandas as pd


class Node:
    def __init__(
        self,
        user_id: int,
        score: float,
        gender: int,
        age: int,
        horoscope: int,
        language: int,
        locale: int,
        education: int,
 
    ) -> None:
        self.user_id = user_id
        self.score = score #note that this attribute is hard coded as 0.1 by default in the load_vertices method instead of being read from the excel file like the others
        self.gender = gender
        self.age = age
        self.horoscope = horoscope
        self.language = language
        self.locale = locale
        self.education = education
        self.neighbours = defaultdict()

    #removed class check of neighbour: Node to resolve NameError: name 'Node' is not defined.
    def add_neighbour(self, neighbour, strength: int) -> None:
        # check if neighbour is already in dictionary
        assert neighbour.user_id not in self.neighbours
        self.neighbours[neighbour.user_id] = strength


class Graph:
    def __init__(self) -> None:
        self.vertices = {}

    def get_scores(self):
        return dict([(v, self.vertices[v].score) for v in self.vertices])
    
    def get_total_infected(self):
        scores = self.get_scores()
        max = len(scores)
        total = 0
        for key in scores:
            total += scores[key]
        return total/max

    def add_vertex(self, v: Node) -> None:
        # do not allow adding if already inside
        assert v.user_id not in self.vertices
        self.vertices[v.user_id] = v

    def add_edge(self, v1: Node, v2: Node, strength: int) -> None:
        # check both nodes are in the graph first
        assert v1.user_id in self.vertices
        assert v2.user_id in self.vertices
        # add edge strength to both (symmetric relationship)
        self.vertices[v1.user_id].add_neighbour(v2, strength)
        self.vertices[v2.user_id].add_neighbour(v1, strength)

    def remove_vertex(self, node_id: int) -> None:
        # check node is in graph
        assert node_id in self.vertices
        node: Node = self.vertices[node_id]
        # remove node from node's neighbours adjacency dictionary
        for neigh_id in node.neighbours:
            neighbour = self.vertices[neigh_id]
            del neighbour.neighbours[node_id]
        del self.vertices[node_id]

    def get_node(self, node_id: int) -> Node:
        assert node_id in self.vertices
        return self.vertices[node_id]

    def set_bad_guy(self, node_id: int, bad_guy_score: float) -> Node:
        assert node_id in self.vertices
        self.vertices[node_id].score = bad_guy_score

    def set_good_guys(self, good_guys: list):
        good_guy_score = -1
        for good_guy in good_guys:
            assert good_guy in self.vertices
            self.vertices[good_guy].score = good_guy_score

class Simulation:
    def __init__(self,bad_guys, good_guys, good_guys_enter_timestep):
        self.graph = Graph()
        self.output = Output()
        self.bad_guys = bad_guys
        self.good_guys = good_guys
        self.good_guys_enter_timestep = good_guys_enter_timestep

    def load_graph(self, graph):
        self.graph = graph

    #=================== IO STUFF ==============================

    def load_vertices_from_file(self, file_name, bad_guys):
        bad_guy_score = 1
        civilian_score = 0
        Nodes = pd.read_csv(file_name)
        Network = self.graph
        for index, row in Nodes.iterrows():
            new_node = Node(row.iloc[0], civilian_score, row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6])
            Network.add_vertex(new_node)
        for bad_guy in bad_guys:
            Network.set_bad_guy(bad_guy, bad_guy_score)

    def load_edges_from_file(self, file_name):
        Edges = pd.read_csv(file_name)
        for index, row in Edges.iterrows():
            source = self.graph.get_node(row.iloc[0])
            target = self.graph.get_node(row.iloc[1])
            source.add_neighbour(target,row.iloc[2])
            target.add_neighbour(source,row.iloc[2])

    def remove_all_singular_nodes(self):
        nodes_to_remove = []
        for node_id, node in self.graph.vertices.items():
            if len(node.neighbours) == 0:
                nodes_to_remove.append(node.user_id)
        print(nodes_to_remove)
        for node_id in nodes_to_remove:
            self.graph.remove_vertex(node_id)
                

    def data_out_to_file(self, filename):
        self.output.df.to_csv(filename)

    #===========================================================

    @staticmethod
    def sigmoid(x):
        return 2 / (1 + math.exp(-x/100)) + 1

    @staticmethod
    def spread(source: Node, target: Node) -> float:
        assert target.user_id in source.neighbours, "target not in source neighbours"
        if source != target:
            multiplier = 1
            similarity_bonuns = 1.05
            for att in ["education", "age", "gender"]:
                if getattr(source, att) == getattr(target, att):
                    multiplier *= similarity_bonuns
            num_msgs = source.neighbours[target.user_id]
            #new_target_score = (source.score + target.score) / 2
            new_target_score = (
                target.score * Simulation.sigmoid(num_msgs) * multiplier
            )
            if new_target_score >= 0: 
                new_target_score = min(1, new_target_score)
            else:
                new_target_score = max(-1, new_target_score)
            return new_target_score

    def calc_new_score(self, vertex: Node, current_timestep: int) -> float:
        if vertex.user_id in self.bad_guys:
            return vertex.score
        elif current_timestep >= self.good_guys_enter_timestep and vertex.user_id in self.good_guys:
            return vertex.score
        total = []
        for n_id in vertex.neighbours:
            n = self.graph.vertices[n_id]
            total.append(Simulation.spread(vertex, n))
            #total.append(vertex.score)
        if len(total) == 0:
            return vertex.score
        else:
            out = sum(total) / len(total)
            modified_out = out * 0.1 + 0.9 * vertex.score
            return modified_out

    def run_one_timestep(self, current_timestep: int):
        # check if graph is empty
        assert self.graph.vertices, "graph empty"
        new_node_scores = {}

        for vertex_id in self.graph.vertices:
            if vertex_id not in new_node_scores:
                vertex = self.graph.vertices[vertex_id]
                vertex_new_score = self.calc_new_score(vertex, current_timestep)
            #total.append(vertex.score)
                new_node_scores[vertex_id] = round(vertex_new_score,5) # round to 5 decimal places

        for vertex_id in self.graph.vertices:
            v = self.graph.vertices[vertex_id]
            v.score = new_node_scores[v.user_id]
        if current_timestep > 98:
            print('Final Scores:')
            print(self.graph.get_scores())
        print(self.graph.get_total_infected())
        #print(self.graph.get_scores()[0])

class Output:
    def __init__(self) -> None:
        df = pd.DataFrame(columns=['Id','Label','Timeset','Score'])
        #df.set_index('Id')
        self.df = df

    def add_timestep_scores(self,score_dict : dict, timestep : int) -> None:
        output_df = self.df
        if timestep == 0: #first time stamp
            for k,v in score_dict.items():
                new_row = {'Id':k,'Label':k,'Timeset':[timestep],'Score':"["+str(timestep)+", "+str(v)+"]"}
                output_df = output_df.append(new_row, ignore_index=True)
            output_df.set_index('Id',inplace = True)
        else:

            for k,v in score_dict.items():
                output_df.loc[k,'Timeset'].append(timestep)
                output_df.loc[k,'Score'] = output_df.loc[k,'Score'] + "; ["+ str(timestep)+", "+str(v) +"]"
        self.df = output_df