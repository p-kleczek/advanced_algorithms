from abc import abstractmethod
from functools import total_ordering
import itertools
import settings
from utils.print_utils import print_2d

__author__ = 'pawel'


@total_ordering
class Vertex(object):
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return str(self.label)

    def __eq__(self, other):
        return self.label == other.label if other else False

    def __le__(self, other):
        return self.label < other.label if other else False


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
        """

        :param vertex:
        :return: index of vertex in the list
        """
        inserted = False
        if settings.INTEGER_VERTICES:
            if len(self.vertices) <= vertex:
                inserted = vertex - len(self.vertices) + 1
                self.vertices.extend([None for i in xrange(inserted)])
            self.vertices[vertex] = vertex
            return vertex, inserted
        else:
            if len(self.vertices) < vertex.label:
                inserted = vertex.label - len(self.vertices) + 1
                self.vertices.extend([None for i in xrange(vertex.label - len(self.vertices))])
            self.vertices[vertex.label-1] = vertex
            return vertex.label-1, inserted

    def delete_vertex(self, vertex):
        inx = self.vertices.index(vertex)
        self.vertices.remove(vertex)
        return inx

    def add_edge(self, edge):
        if self.is_edge_exist(edge.vertex_from, edge.vertex_to):
            if not settings.SURPRESS_WARNINGS:
                print 'WARNING: Edge %s -> %s already exist! (skipped)' % (edge.vertex_from, edge.vertex_to)
        else:
            self._add_edge_internal(edge)

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
        if settings.INTEGER_VERTICES:
            return vertex_id
        else:
            return next(v for v in self.vertices if v.label == vertex_id)

    def get_vertex_position(self, vertex):
        if settings.INTEGER_VERTICES:
            return vertex
        else:
            return self.vertices.index(vertex)

    def get_edge(self, edge_id):
        return [e for e in self.get_edges() if e.label == edge_id][0]

    @classmethod
    def get_edge_ends(cls, edge):
        return edge.vertex_from, edge.vertex_to

    def get_vertices_count(self):
        return len(self.vertices)

    def get_edges_count(self):
        return len(self.get_edges())

    def is_neighbors(self, vertex_1, vertex_2):
        return vertex_2 in self.get_neighbors(vertex_1)

    def is_edge_exist(self, vertex_from, vertex_to):
        raise NotImplementedError()

    def _add_edge_internal(self, edge):
        raise NotImplementedError()

    @abstractmethod
    def get_edges(self):
        pass

    def __str__(self):
        s = 'Vertices:\n    '
        s += ', '.join(map(str, self.vertices))
        s += '\nEdges:\n    '
        edges = filter(None, self.get_edges())
        edges.sort()
        s += '\n    '.join(map(str, edges))
        s += '\n'
        return s


class MatrixGraph(Graph):

    def __init__(self):
        super(MatrixGraph, self).__init__()
        self.matrix = []

    def add_vertex(self, vertex):
        inx, inserted = super(MatrixGraph, self).add_vertex(vertex)
        if settings.INTEGER_VERTICES:
            for i in xrange(inserted):
                [row.append(None) for row in self.matrix]
            for i in xrange(inserted):
                self.matrix.append([None] * len(self.vertices))
        else:
            if inserted:
                [row.append(None) for row in self.matrix]
                self.matrix.append([None] * len(self.vertices))
        return inx

    def delete_vertex(self, vertex):
        inx = super(MatrixGraph, self).delete_vertex(vertex)
        for row in self.matrix:
            del row[inx]
        del self.matrix[inx]

    def _add_edge_internal(self, edge):
        inx_from = self.add_vertex(edge.vertex_from)
        inx_to = self.add_vertex(edge.vertex_to)
        self.matrix[inx_from][inx_to] = edge

    def delete_edge(self, edge):
        inx_from = self.vertices.index(edge.vertex_from)
        inx_to = self.vertices.index(edge.vertex_to)
        self.matrix[inx_from][inx_to] = None

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

    def get_edges(self):
        return filter(None, list(itertools.chain.from_iterable(self.matrix)))


class ListGraph(Graph):
    def __init__(self):
        super(ListGraph, self).__init__()
        self.adj_list = []

    def add_vertex(self, vertex):
        inx, inserted = super(ListGraph, self).add_vertex(vertex)
        if inserted:
            self.adj_list.extend([[] for i in xrange(inserted)])
        return inx

    def delete_vertex(self, vertex):
        inx = super(ListGraph, self).delete_vertex(vertex)
        del self.adj_list[inx]
        [[l.remove(e) for e in l if e.vertex_to == vertex] for l in self.adj_list]

    def _add_edge_internal(self, edge):
        inx_from = self.add_vertex(edge.vertex_from)
        self.add_vertex(edge.vertex_to)
        self.adj_list[inx_from].append(edge)

    def delete_edge(self, edge):
        inx = self.vertices.index(edge.vertex_from)
        self.adj_list[inx].remove(edge)

    def get_incoming_edges(self, vertex):
        flat_adj_list = list(itertools.chain.from_iterable(self.adj_list))
        return [e for e in flat_adj_list if e.vertex_to == vertex]

    def get_outgoing_edges(self, vertex):
        if settings.INTEGER_VERTICES:
            inx = vertex
        else:
            inx = self.get_vertex_position(vertex)
        return self.adj_list[inx]

    def get_edges(self):
        return filter(None, list(itertools.chain.from_iterable(self.adj_list)))

    # TODO: test this method
    def is_edge_exist(self, vertex_from, vertex_to):
        if settings.INTEGER_VERTICES:
            inx_from = vertex_from
            try:
                self.adj_list[inx_from]
            except IndexError:
                return False
        else:
            try:
                inx_from = self.vertices.index(vertex_from)
            except ValueError:
                return False

        return any(e.vertex_to == vertex_to for e in self.adj_list[inx_from])


def read_graph(filename, graph):
    with open(filename) as f:
        _id = 1
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            vals = line.strip().split('; ')
            v_from_label = int(vals[0])
            v_to_label = int(vals[1])
            if settings.INTEGER_VERTICES:
                v_from = v_from_label
                v_to = v_to_label
            else:
                v_from = Vertex(v_from_label)
                v_to = Vertex(v_to_label)
            weight = int(vals[2])
            e = Edge(_id, v_from, v_to, weight)
            _id += 1
            graph.add_edge(e)
