import unittest
from graphs.graph import ListGraph, Vertex, read_graph, MatrixGraph, Edge
from graphs.shortest_paths import reconstruct_path, floyd_warshall

__author__ = 'pawel'


class FloydWarshallTest(unittest.TestCase):
    def setUp(self):
        self.g = ListGraph()
        read_graph('../../data/test_floyd_warshall.graph', self.g)

    def test_simple(self):
        actual_predecessors = floyd_warshall(self.g)

        expected_predecessors = [
            [None, 0, 1],
            [None, None, 1],
            [None, None, None]
        ]
        self.assertListEqual(actual_predecessors, expected_predecessors)


class ReconstructPathTest(unittest.TestCase):
    def test_simple(self):
        # 1 -[10]-> 2
        # 2 -[20]-> 3

        graph = MatrixGraph()
        graph.add_edge(Edge(1, 1, 2, 10))
        graph.add_edge(Edge(1, 2, 1, 20))

        pred = [
            [None, 1, 2],
            [None, None, 2],
            [None, None, None]
        ]

        self.assertListEqual(reconstruct_path(pred, 1, 1, graph), [])
        self.assertListEqual(reconstruct_path(pred, 1, 2, graph), [1, 2])
        self.assertListEqual(reconstruct_path(pred, 1, 3, graph), [1, 2, 3])
        self.assertListEqual(reconstruct_path(pred, 2, 1, graph), [])
        self.assertListEqual(reconstruct_path(pred, 2, 2, graph), [])
        self.assertListEqual(reconstruct_path(pred, 2, 3, graph), [2, 3])
        self.assertListEqual(reconstruct_path(pred, 3, 1, graph), [])
        self.assertListEqual(reconstruct_path(pred, 3, 2, graph), [])
        self.assertListEqual(reconstruct_path(pred, 3, 3, graph), [])
