from functools import total_ordering
import itertools

__author__ = 'pawel'


@total_ordering
class Vertex(object):
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return str(self.label)

    def __eq__(self, other):
        return self.label == other.label

    def __le__(self, other):
        return self.label < other.label

@total_ordering
class Edge(object):
    def __init__(self, label, vertex_from, vertex_to, weight):
        self.label = label
        self.weight = weight
        self.vertex_to = vertex_to
        self.vertex_from = vertex_from

    def __str__(self):
        return "%s -[ %s ]-> %s" % (self.vertex_from, self.weight, self.vertex_to)

    def __eq__(self, other):
        return (self.vertex_from, self.vertex_to) == (other.vertex_from, other.vertex_to)

    def __le__(self, other):
        return (self.vertex_from, self.vertex_to) < (other.vertex_from, other.vertex_to)


class Graph(object):
    def __init__(self):
        self.vertices = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def delete_vertex(self, vertex):
        raise NotImplementedError()

    def add_edge(self, edge):
        if self.is_edge_exist(edge.vertex_from, edge.vertex_to):
            print 'WARNING: Edge %s -> %s already exist! (skipped)' % (edge.vertex_from, edge.vertex_to)
        else:
            self.add_edge_internal(edge)

    def delete_edge(self, edge):
        raise NotImplementedError()

    def get_neighbors(self, vertex):
        inc = [e.vertex_from for e in self.get_incoming_edges(vertex)]
        out = [e.vertex_to for e in self.get_outgoing_edges(vertex)]
        return list(set(inc) | set(out))

    def get_incoming_edges(self, vertex):
        raise NotImplementedError()

    def get_outgoing_edges(self, vertex):
        raise NotImplementedError()

    def get_adjacent_edges(self, vertex):
        return self.get_incoming_edges(vertex) + self.get_outgoing_edges(vertex)

    def get_vertex(self, vertex_id):
        return next(v for v in self.vertices if v.label == vertex_id)

    def get_edge(self, edge_id):
        raise NotImplementedError()

    @classmethod
    def get_edge_ends(cls, edge):
        return edge.vertex_from, edge.vertex_to

    def get_vertices_count(self):
        return len(self.vertices)

    def get_edges_count(self):
        raise NotImplementedError()

    def is_neighbors(self, vertex_1, vertex_2):
        return vertex_2 in self.get_neighbors(vertex_1)

    def is_edge_exist(self, vertex_from, vertex_to):
        raise NotImplementedError()

    def add_edge_internal(self, edge):
        raise NotImplementedError()


class MatrixGraph(Graph):

    def __init__(self):
        super(MatrixGraph, self).__init__()
        self.matrix = []

    def add_vertex(self, vertex):
        super(MatrixGraph, self).add_vertex(vertex)
        for row in self.matrix:
            row.append(None)
        self.matrix.append([None] * len(self.vertices))

    def delete_vertex(self, vertex):
        inx = self.vertices.index(vertex)
        self.vertices.remove(vertex)
        for row in self.matrix:
            del row[inx]
        del self.matrix[inx]

    def add_edge_internal(self, edge):
        try:
            inx_from = self.vertices.index(edge.vertex_from)
        except ValueError:
            self.add_vertex(edge.vertex_from)
            inx_from = self.vertices.index(edge.vertex_from)
        try:
            inx_to = self.vertices.index(edge.vertex_to)
        except ValueError:
            self.add_vertex(edge.vertex_to)
            inx_to = self.vertices.index(edge.vertex_to)

        self.matrix[inx_from][inx_to] = edge

    def delete_edge(self, edge):
        inx_from = self.vertices.index(edge.vertex_from)
        inx_to = self.vertices.index(edge.vertex_to)
        self.matrix[inx_from][inx_to] = None

    # def get_neighbors(self, vertex):
    #     inx = self.vertices.index(vertex)
    #     neighbors = []
    #     for (pos, elem) in enumerate(self.matrix[inx]):
    #         if elem:
    #             neighbors.append(self.vertices[pos])
    #     return neighbors

    def get_incoming_edges(self, vertex):
        inx = self.vertices.index(vertex)
        incoming_edges = []
        for i in xrange(len(self.vertices)):
            edge = self.matrix[i][inx]
            if edge:
                incoming_edges.append(edge)
        return incoming_edges

    def get_outgoing_edges(self, vertex):
        inx = self.vertices.index(vertex)
        row = filter(None, self.matrix[inx])
        outgoing = filter(lambda e: e.vertex_from == vertex, row)
        return outgoing

    def get_edge(self, edge_id):
        flat_matrix = list(itertools.chain.from_iterable(self.matrix))
        return filter(lambda e: e.label == edge_id, filter(None, flat_matrix))[0]

    def get_vertices_count(self):
        return len(self.vertices)

    def get_edges_count(self):
        flat_matrix = list(itertools.chain.from_iterable(self.matrix))
        return sum([x is not None for x in flat_matrix])

    # def is_neighbors(self, vertex_1, vertex_2):
    #     inx_1 = self.vertices.index(vertex_1)
    #     inx_2 = self.vertices.index(vertex_2)
    #     return self.matrix[inx_1][inx_2] or self.matrix[inx_2][inx_1]

    def is_edge_exist(self, vertex_from, vertex_to):
        try:
            inx_from = self.vertices.index(vertex_from)
        except ValueError:
            return False
        try:
            inx_to = self.vertices.index(vertex_to)
        except ValueError:
            return False

        return self.matrix[inx_from][inx_to]

    def __str__(self):
        # TODO sort edges (id_from / id_to)
        s = 'Vertices:\n    '
        s += ', '.join(map(str, self.vertices))
        s += '\nEdges:\n    '
        flat_matrix = filter(None, list(itertools.chain.from_iterable(self.matrix)))
        flat_matrix.sort()
        s += '\n    '.join(map(str, flat_matrix))
        return s


class ListGraph(Graph):
    def __init__(self):
        super(ListGraph, self).__init__()
        self.adj_list = []

    def add_vertex(self, vertex):
        super(ListGraph, self).add_vertex(vertex)
        self.adj_list.append([])

    def delete_vertex(self, vertex):
        inx = self.vertices.index(vertex)
        self.vertices.remove(vertex)
        del self.adj_list[inx]
        for l in self.adj_list:
            [l.remove(e) for e in l if e.vertex_to == vertex]

    def add_edge_internal(self, edge):
        if not edge.vertex_from in self.vertices:
            self.vertices.append(edge.vertex_from)
            self.adj_list.append([])
        if not edge.vertex_to in self.vertices:
            self.vertices.append(edge.vertex_to)
            self.adj_list.append([])
        inx_from = self.vertices.index(edge.vertex_from)
        self.adj_list[inx_from].append(edge)

    def delete_edge(self, edge):
        inx = self.vertices.index(edge.vertex_from)
        self.adj_list[inx].remove(edge)

    # def get_neighbors(self, vertex):
    #     inx = self.vertices.index(vertex)
    #     neighbors = []
    #     [neighbors.append(e.vertex_to) for e in self.adj_list[inx]]  # outgoing
    #     for (i, l) in enumerate(self.adj_list):
    #         if any(e.vertex_to == vertex for e in l):
    #             neighbors.append(self.vertices[i])
    #     return neighbors

    def get_incoming_edges(self, vertex):
        flat_adj_list = list(itertools.chain.from_iterable(self.adj_list))
        return [e for e in flat_adj_list if e.vertex_to == vertex]

    def get_outgoing_edges(self, vertex):
        inx = self.vertices.index(vertex)
        return self.adj_list[inx]

    def get_edge(self, edge_id):
        flat_adj_list = list(itertools.chain.from_iterable(self.adj_list))
        return next(e for e in flat_adj_list if e.label == edge_id)

    def get_edges_count(self):
        return sum([len(l) for l in self.adj_list])

    def __str__(self):
        s = 'Vertices:\n    '
        s += ', '.join(map(str, self.vertices))
        s += '\nEdges:\n    '
        flat_matrix = filter(None, list(itertools.chain.from_iterable(self.adj_list)))
        flat_matrix.sort()
        s += '\n    '.join(map(str, flat_matrix))
        return s

    def is_edge_exist(self, vertex_from, vertex_to):
        try:
            inx_from = self.vertices.index(vertex_from)
        except ValueError:
            return False

        return any(e.vertex_to == vertex_to for e in self.adj_list[inx_from])