from __future__ import annotations
from collections import defaultdict
import math


class Node:
    def __init__(
        self,
        user_id: int,
        score: float,
        education: int,
        age: int,
        gender: int,
        language: int,
        locale: int,
        horoscope: int,
    ) -> None:
        self.user_id = user_id
        self.score = score
        self.education = education
        self.age = age
        self.gender = gender
        self.language = language
        self.locale = locale
        self.horoscope = horoscope
        self.neighbours = defaultdict()

    def add_neighbour(self, neighbour: Node, strength: int) -> None:
        # check if neighbour is already in dictionary
        assert neighbour.user_id not in self.neighbours
        self.neighbours[neighbour.user_id] = strength


class Graph:
    def __init__(self) -> None:
        self.vertices = {}

    def get_scores(self):
        return dict([(v, self.vertices[v].score) for v in self.vertices])

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


class Simulation:
    def __init__(self):
        self.graph = Graph()

    def load_graph(self, graph):
        self.graph = graph

    #=================== IO STUFF ==============================

    def load_vertices_from_file(self, file_name):
        # TODO
        pass

    def load_edges_from_file(self, file_name):
        # TODO
        pass

    def data_out_to_file(self, filename):
        # TODO
        pass

    #===========================================================

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    @staticmethod
    def spread(source: Node, target: Node) -> float:
        assert target.user_id in source.neighbours, "target not in source neighbours"
        if source != target:
            multiplier = 1
            similarity_bonuns = 1.2
            for att in ["education", "age"]:
                if getattr(source, att) == getattr(target, att):
                    multiplier *= similarity_bonuns
            num_msgs = source.neighbours[target.user_id]
            new_target_score = (source.score + target.score) / 2
            new_target_score = (
                new_target_score * Simulation.sigmoid(num_msgs) * multiplier
            )
            new_target_score = min(1, new_target_score)
            return new_target_score

    def calc_new_score(self, vertex: Node) -> float:
        total = []
        for n_id in vertex.neighbours:
            n = self.graph.vertices[n_id]
            total.append(Simulation.spread(vertex, n))
        return sum(total) / len(total)

    def run_one_timestep(self):
        # check if graph is empty
        assert self.graph.vertices, "graph empty"
        new_node_scores = {}

        for vertex_id in self.graph.vertices:
            if vertex_id not in new_node_scores:
                vertex = self.graph.vertices[vertex_id]
                vertex_new_score = self.calc_new_score(vertex)
                new_node_scores[vertex_id] = vertex_new_score

        for vertex_id in self.graph.vertices:
            v = self.graph.vertices[vertex_id]
            v.score = new_node_scores[v.user_id]


