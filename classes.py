from __future__ import annotations
from collections import defaultdict


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

