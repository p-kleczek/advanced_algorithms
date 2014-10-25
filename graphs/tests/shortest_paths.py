import unittest
from graphs.graph import ListGraph, Vertex, read_graph
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
        # 1 -> 2
        # 2 -> 3
        pred = [
            [None, 0, 1],
            [None, None, 1],
            [None, None, None]
        ]

        self.assertListEqual(reconstruct_path(pred, 0, 0), [])
        self.assertListEqual(reconstruct_path(pred, 0, 1), [0, 1])
        self.assertListEqual(reconstruct_path(pred, 0, 2), [0, 1, 2])
        self.assertListEqual(reconstruct_path(pred, 1, 0), [])
        self.assertListEqual(reconstruct_path(pred, 1, 1), [])
        self.assertListEqual(reconstruct_path(pred, 1, 2), [1, 2])
        self.assertListEqual(reconstruct_path(pred, 2, 0), [])
        self.assertListEqual(reconstruct_path(pred, 2, 1), [])
        self.assertListEqual(reconstruct_path(pred, 2, 2), [])
