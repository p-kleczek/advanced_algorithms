from graphs.graph import MatrixGraph, Vertex, Edge, ListGraph, Graph, read_graph

import unittest


class GraphTest(unittest.TestCase):
    V1_LABEL = 1
    V2_LABEL = 2
    V3_LABEL = 3
    V4_LABEL = 4
    V5_LABEL = 5

    E1_LABEL = 1
    E2_LABEL = 2
    E3_LABEL = 3

    v1 = Vertex(V1_LABEL)
    v2 = Vertex(V2_LABEL)
    v3 = Vertex(V3_LABEL)
    v4 = Vertex(V4_LABEL)
    v5 = Vertex(V5_LABEL)

    e1 = Edge(E1_LABEL, v1, v2, 3)
    e2 = Edge(E2_LABEL, v2, v1, 5)
    e3 = Edge(E3_LABEL, v4, v5, 10)

    def setUp(self):
        self.g = Graph()

    def test_get_vertex(self):
        self.g.add_vertex(self.v1)
        self.assertEqual(self.g.get_vertex(self.V1_LABEL), self.v1)

    def test_get_edge_ends(self):
        self.assertTupleEqual(self.g.get_edge_ends(self.e1), (self.v1, self.v2))

    def test_get_vertices_count(self):
        self.assertEqual(self.g.get_vertices_count(), 0)
        self.g.add_vertex(self.v1)
        self.assertEqual(self.g.get_vertices_count(), 1)
        self.g.add_vertex(self.v2)
        self.assertEqual(self.g.get_vertices_count(), 2)

    def test_get_vertex_position(self):
        self.g.add_vertex(self.v1)
        self.g.add_vertex(self.v2)
        self.g.add_vertex(self.v3)
        self.assertEqual(self.g.get_vertex_position(self.v1), 0)
        self.assertEqual(self.g.get_vertex_position(self.v2), 1)
        self.assertEqual(self.g.get_vertex_position(self.v3), 2)


class MatrixGraphTest(GraphTest):
    def setUp(self):
        self.g = MatrixGraph()

    def test_add_vertex_once(self):
        self.g.add_vertex(self.v1)
        self.assertListEqual([self.v1], self.g.vertices)
        self.assertListEqual([[None]], self.g.matrix)

    def test_add_vertex_twice(self):
        self.g.add_vertex(self.v1)
        self.g.add_vertex(self.v2)
        self.assertListEqual([self.v1, self.v2], self.g.vertices)
        self.assertListEqual([[None, None], [None, None]], self.g.matrix)

    def test_delete_vertex(self):
        self.g.add_vertex(self.v1)
        self.g.add_vertex(self.v2)
        self.g.delete_vertex(self.v1)
        self.assertListEqual([self.v2], self.g.vertices)
        self.assertListEqual([[None]], self.g.matrix)

    def test_add_edge(self):
        self.g.add_edge(self.e1)
        self.assertListEqual(self.g.vertices, [self.v1, self.v2])
        self.assertListEqual(self.g.matrix, [[None, self.e1], [None, None]])

    def test_delete_edge(self):
        self.g.add_edge(self.e1)
        self.g.delete_edge(self.e1)
        self.assertListEqual(self.g.vertices, [self.v1, self.v2])
        self.assertListEqual(self.g.matrix, [[None, None], [None, None]])

    def test_delete_edge_one_remaining(self):
        self.g.add_edge(self.e1)
        self.g.add_edge(self.e2)
        self.g.delete_edge(self.e2)
        self.assertListEqual(self.g.vertices, [self.v1, self.v2])
        self.assertListEqual(self.g.matrix, [[None, self.e1], [None, None]])

    def test_get_neighbors(self):
        self.g.add_edge(self.e1)
        self.g.add_vertex(self.v3)
        self.assertListEqual(self.g.get_neighbors(self.v1), [self.v2])
        self.assertListEqual(self.g.get_neighbors(self.v3), [])

    def test_get_neighbors_exhaustive(self):
        self.g.add_edge(self.e1)
        self.g.add_edge(self.e2)
        self.g.add_edge(self.e3)
        self.g.add_vertex(self.v3)
        self.assertListEqual(self.g.get_neighbors(self.v1), [self.v2])
        self.assertListEqual(self.g.get_neighbors(self.v2), [self.v1])
        self.assertListEqual(self.g.get_neighbors(self.v3), [])
        self.assertListEqual(self.g.get_neighbors(self.v4), [self.v5])
        self.assertListEqual(self.g.get_neighbors(self.v5), [self.v4])

    def test_get_incoming_edges(self):
        self.g.add_edge(self.e1)
        self.g.add_edge(self.e2)
        self.assertListEqual(self.g.get_incoming_edges(self.v2), [self.e1])

    def test_get_outgoing_edges(self):
        self.g.add_edge(self.e1)
        self.g.add_edge(self.e2)
        self.assertListEqual(self.g.get_outgoing_edges(self.v2), [self.e2])

    def test_get_edge(self):
        self.g.add_edge(self.e1)
        self.assertEqual(self.g.get_edge(self.E1_LABEL), self.e1)

    def test_get_edges_count(self):
        self.assertEqual(self.g.get_edges_count(), 0)
        self.g.add_edge(self.e1)
        self.assertEqual(self.g.get_edges_count(), 1)
        self.g.add_edge(self.e2)
        self.assertEqual(self.g.get_edges_count(), 2)

    def test_is_neighbors(self):
        self.g.add_edge(self.e1)
        self.g.add_vertex(self.v3)
        self.assertTrue(self.g.is_neighbors(self.v1, self.v2))
        self.assertTrue(self.g.is_neighbors(self.v2, self.v1))
        self.assertFalse(self.g.is_neighbors(self.v3, self.v1))
        self.assertFalse(self.g.is_neighbors(self.v3, self.v2))

    def test_acceptance(self):
        read_graph('../../data/graf.txt', self.g)
        control_sum = sum([e.weight for e in self.g.get_edges() if e.vertex_from < e.vertex_to])
        self.assertEqual(control_sum, 4790)


class ListGraphTest(GraphTest):
    def setUp(self):
        self.g = ListGraph()

    def test_add_vertex_once(self):
        self.g.add_vertex(self.v1)
        self.assertListEqual([self.v1], self.g.vertices)
        self.assertListEqual([[]], self.g.adj_list)

    def test_add_vertex_twice(self):
        self.g.add_vertex(self.v1)
        self.g.add_vertex(self.v2)
        self.assertListEqual([self.v1, self.v2], self.g.vertices)
        self.assertListEqual([[], []], self.g.adj_list)

    def test_delete_vertex(self):
        self.g.add_vertex(self.v1)
        self.g.add_vertex(self.v2)
        self.g.delete_vertex(self.v1)
        self.assertListEqual(self.g.vertices, [self.v2])
        self.assertListEqual(self.g.adj_list, [[]])

    def test_add_edge(self):
        self.g.add_edge(self.e1)
        self.assertListEqual(self.g.vertices, [self.v1, self.v2])
        self.assertListEqual(self.g.adj_list, [[self.e1], []])

    def test_delete_edge(self):
        self.g.add_edge(self.e1)
        self.g.delete_edge(self.e1)
        self.assertListEqual(self.g.vertices, [self.v1, self.v2])
        self.assertListEqual(self.g.adj_list, [[], []])

    def test_delete_edge_one_remaining(self):
        self.g.add_edge(self.e1)
        self.g.add_edge(self.e2)
        self.g.delete_edge(self.e2)
        self.assertListEqual(self.g.vertices, [self.v1, self.v2])
        self.assertListEqual(self.g.adj_list, [[self.e1], []])

    def test_get_neighbors(self):
        self.g.add_edge(self.e1)
        self.g.add_vertex(self.v3)
        self.assertListEqual(self.g.get_neighbors(self.v1), [self.v2])
        self.assertListEqual(self.g.get_neighbors(self.v3), [])

    def test_get_neighbors_exhaustive(self):
        self.g.add_edge(self.e1)
        self.g.add_edge(self.e2)
        self.g.add_edge(self.e3)
        self.g.add_vertex(self.v3)
        self.assertListEqual(self.g.get_neighbors(self.v1), [self.v2])
        self.assertListEqual(self.g.get_neighbors(self.v2), [self.v1])
        self.assertListEqual(self.g.get_neighbors(self.v3), [])
        self.assertListEqual(self.g.get_neighbors(self.v4), [self.v5])
        self.assertListEqual(self.g.get_neighbors(self.v5), [self.v4])

    def test_get_incoming_edges(self):
        self.g.add_edge(self.e1)
        self.g.add_edge(self.e2)
        self.assertListEqual(self.g.get_incoming_edges(self.v2), [self.e1])

    def test_get_outgoing_edges(self):
        self.g.add_edge(self.e1)
        self.g.add_edge(self.e2)
        self.assertListEqual(self.g.get_outgoing_edges(self.v2), [self.e2])

    def test_get_edge(self):
        self.g.add_edge(self.e1)
        self.assertEqual(self.g.get_edge(self.E1_LABEL), self.e1)

    def test_get_vertices_count(self):
        self.assertEqual(self.g.get_vertices_count(), 0)
        self.g.add_vertex(self.v1)
        self.assertEqual(self.g.get_vertices_count(), 1)
        self.g.add_vertex(self.v2)
        self.assertEqual(self.g.get_vertices_count(), 2)

    def test_get_edges_count(self):
        self.assertEqual(self.g.get_edges_count(), 0)
        self.g.add_edge(self.e1)
        self.assertEqual(self.g.get_edges_count(), 1)
        self.g.add_edge(self.e2)
        self.assertEqual(self.g.get_edges_count(), 2)

    def test_is_neighbors(self):
        self.g.add_edge(self.e1)
        self.g.add_vertex(self.v3)
        self.assertTrue(self.g.is_neighbors(self.v1, self.v2))
        self.assertTrue(self.g.is_neighbors(self.v2, self.v1))
        self.assertFalse(self.g.is_neighbors(self.v3, self.v1))
        self.assertFalse(self.g.is_neighbors(self.v3, self.v2))

    def test_acceptance(self):
        read_graph('../../data/graf.txt', self.g)
        control_sum = sum([e.weight for e in self.g.get_edges() if e.vertex_from < e.vertex_to])
        self.assertEqual(control_sum, 4790)
