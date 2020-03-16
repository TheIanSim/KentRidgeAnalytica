import unittest
from classes import Graph, Node, Simulation


class TestNode(unittest.TestCase):
    def setUp(self):
        self.test_node_0 = Node(0, 0.1, 1, 1, 1, 1, 1, 1)
        self.test_node_1 = Node(1, 0.1, 1, 1, 1, 1, 1, 1)

    def test_add_neighbour(self):
        strength: int = 20
        self.assertTrue(len(self.test_node_0.neighbours) == 0)
        self.assertTrue(len(self.test_node_1.neighbours) == 0)
        self.test_node_0.add_neighbour(self.test_node_1, strength)
        self.assertTrue(self.test_node_0.neighbours[1] == strength)
        self.assertTrue(1 in self.test_node_0.neighbours)
        self.assertTrue(len(self.test_node_1.neighbours) == 0)


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.test_graph = Graph()
        self.test_node_0 = Node(0, 0.1, 1, 1, 1, 1, 1, 1)
        self.test_node_1 = Node(1, 0.1, 1, 1, 1, 1, 1, 1)

    def test_add_vertex(self):
        # add the two test nodes
        self.test_graph.add_vertex(self.test_node_0)
        self.test_graph.add_vertex(self.test_node_1)

        # see if they are in the graph vertex dictionary
        self.assertEqual(len(self.test_graph.vertices), 2)
        self.assertTrue(0 in self.test_graph.vertices)
        self.assertTrue(1 in self.test_graph.vertices)

        # if node already in graph, do not allow adding
        with self.assertRaises(AssertionError):
            self.test_graph.add_vertex(self.test_node_0)

    def test_add_edge(self):
        n0, n1 = self.test_node_0, self.test_node_1
        strength: int = 10
        self.test_graph.add_vertex(n0)
        self.test_graph.add_vertex(n1)
        self.test_graph.add_edge(n0, n1, strength)
        self.assertTrue(1 in n0.neighbours)
        self.assertTrue(0 in n1.neighbours)

        # check bidirectional strength
        self.assertEqual(n0.neighbours[1], strength)
        self.assertEqual(n1.neighbours[0], strength)

        # do not allow adding the same edge
        with self.assertRaises(AssertionError):
            self.test_graph.add_edge(n0, n1, strength)
        with self.assertRaises(AssertionError):
            self.test_graph.add_edge(n1, n0, strength)

    def test_remove_vertex(self):
        n0, n1 = self.test_node_0, self.test_node_1
        n2 = Node(2, 0.1, 1, 1, 1, 1, 1, 1)
        self.test_graph.add_vertex(n0)
        self.test_graph.add_vertex(n1)
        self.test_graph.add_vertex(n2)
        self.test_graph.add_edge(n0, n1, 5)
        self.test_graph.add_edge(n1, n2, 15)
        self.test_graph.add_edge(n2, n0, 25)

        self.test_graph.remove_vertex(0)

        # test_node_0 no longer in neighbours dicts
        self.assertFalse(0 in n1.neighbours)
        self.assertFalse(0 in n2.neighbours)

        # neighbours edges intact
        self.assertTrue(2 in n1.neighbours)
        self.assertTrue(1 in n2.neighbours)

        self.assertFalse(0 in self.test_graph.vertices)

        # try to remove something that is removed
        with self.assertRaises(AssertionError):
            self.test_graph.remove_vertex(0)

        self.test_graph.remove_vertex(1)
        self.assertFalse(1 in n2.neighbours)

    def test_get_node(self):
        self.test_graph.add_vertex(self.test_node_0)
        self.assertEqual(self.test_graph.get_node(0), self.test_node_0)
        with self.assertRaises(AssertionError):
            self.test_graph.get_node(1)


class TestSimulation(unittest.TestCase):
    def setUp(self):
        self.test_graph = Graph()
        self.test_node_0 = Node(0, 0.1, 1, 1, 1, 1, 1, 1)
        self.test_node_1 = Node(1, 0.2, 2, 2, 2, 2, 2, 2)
        self.test_node_2 = Node(2, 0.3, 1, 2, 3, 4, 5, 6)
        self.test_graph.add_vertex(self.test_node_0)
        self.test_graph.add_vertex(self.test_node_1)
        self.test_graph.add_vertex(self.test_node_2)
        self.test_graph.add_edge(self.test_node_0, self.test_node_1, 30)
        self.test_graph.add_edge(self.test_node_1, self.test_node_2, 50)

        self.test_sim = Simulation()
        self.test_sim.load_graph(self.test_graph)

    def test_spread(self):
        res1 = min(1, Simulation.sigmoid(30) * 0.15)
        res2 = min(1, Simulation.sigmoid(60) * 0.25 * 1.2)
        self.assertAlmostEqual(Simulation.spread(self.test_node_0, self.test_node_1), res1)
        self.assertAlmostEqual(Simulation.spread(self.test_node_1, self.test_node_2), res2)

    def test_calc_new_score(self):
        res = (
            Simulation.spread(self.test_node_0, self.test_node_1)
            + Simulation.spread(self.test_node_2, self.test_node_1)
        ) / 2
        self.assertAlmostEqual(self.test_sim.calc_new_score(self.test_node_1), res)

    def test_run_one_timestep(self):
        print(self.test_sim.graph.get_scores())
        self.test_sim.run_one_timestep()
        print(self.test_sim.graph.get_scores())


if __name__ == "__main__":
    unittest.main()
