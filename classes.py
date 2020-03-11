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
        self.neighbours[neighbour] = strength


class Graph:
    def __init__(self) -> None:
        self.vertices = {}

    def add_vertex(self, v: Node) -> None:
        self.vertices[v.user_id] = v

    def add_edge(self, v1: Node, v2: Node, strength: int) -> None:
        assert v1 in self.vertices
        assert v2 in self.vertices

        self.vertices[v1].add_neighbour(v2, strength)
        self.vertices[v2].add_neighbour(v1, strength)

    def remove_vertex(self, node_id: int) -> None:
        node: Node = self.vertices[node_id]
        for n in node.neighbours:
            del n.neighbours[node_id]
        del self.vertices[node_id]

    def get_node(self, node_id: int) -> Node:
        return self.vertices[node_id]

