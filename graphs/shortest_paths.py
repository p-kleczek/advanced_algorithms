# -*- coding: utf-8 -*-

import sys
from utils.print_utils import print_2d
from utils.consts import INF
import settings

__author__ = 'pawel'

# Uwagi:
# (2) Wartość wyjściowa: tablica d[.][.] zawierająca długości najkrótszych ścieżek w grafie. Inicjalnie:
# d[x][y] = 0, gdy x==y,
# d[x][y] = +∞, gdy (x,y)∉E,
# d[x][y] = w(x,y), gdy (x,y)∈E
# (3) Tablica poprzednik[x][y] zawiera element poprzedzający węzeł y na najkrótszej ścieżce od węzła x.
#
# Floyd-Warshall(G,w)
#
# dla każdego wierzchołka u w V[G] wykonaj
#   dla każdego wierzchołka v1 w V[G] wykonaj
#     dla każdego wierzchołka v2 w V[G] wykonaj
#       jeżeli d[v1][v2] > d[v1][u] + d[u][v2] to
#         d[v1][v2] = d[v1][u] + d[u][v2]
#         poprzednik[v1][v2] = poprzednik[u][v2]

def floyd_warshall(graph):
    n = len(graph.vertices)
    distances = [[INF for i in xrange(n)] for j in xrange(n)]
    predecessors = [[None for i in xrange(n)] for j in xrange(n)]
    for v in graph.vertices:
        x = graph.get_vertex_position(v)
        distances[x][x] = 0
    print "[FLOYD] Vertices processed"
    for e in graph.get_edges():
        x = graph.get_vertex_position(e.vertex_from)
        y = graph.get_vertex_position(e.vertex_to)
        distances[x][y] = e.weight
        predecessors[x][y] = x
    print "[FLOYD] Edges processed"

    inx = 0
    total_iterations = len(graph.vertices) ** 3
    iterations_per_one_percent = total_iterations / 100
    print "[FLOYD] Total iterations = %d" % (len(graph.vertices) ** 3)
    for u_pos in xrange(graph.get_vertices_count()):
        for v1_pos in xrange(graph.get_vertices_count()):
            for v2_pos in xrange(graph.get_vertices_count()):
                old_distance = distances[v1_pos][u_pos] + distances[u_pos][v2_pos]
                if distances[v1_pos][v2_pos] > old_distance:
                    distances[v1_pos][v2_pos] = old_distance
                    predecessors[v1_pos][v2_pos] = predecessors[u_pos][v2_pos]
                inx += 1
                if iterations_per_one_percent == 0:
                    print "[FLOYD] %d%% finished" % (inx * 100 / total_iterations)
                elif inx % iterations_per_one_percent == 0:
                    print "[FLOYD] %d%% finished" % (inx / iterations_per_one_percent)
    return predecessors


def reconstruct_path(predecessors, u_inx, v_inx, graph):
    """
    Reconstructs path from u to v based on the predecessors matrix.

    :param predecessors: list of lists
    :param u_inx: int
    :param v_inx: int
    :return: list
    """
    if isinstance(predecessors[0], list):
        _path = reconstruct_path_2d(predecessors, u_inx, v_inx, graph)
    else:
        _path = reconstruct_path_1d(predecessors, u_inx, v_inx, graph)

    if not settings.INTEGER_VERTICES:
        _path = map(lambda pos: graph.vertices[pos].label, _path)
    return _path


def reconstruct_path_1d(predecessors, u_inx, v_inx, graph):
    """
    Reconstructs path from u to v based on the predecessors matrix.

    :param predecessors: list
    :param u_inx: Vertex
    :param v_inx: Vertex
    :return: list
    """
    if predecessors[v_inx] is None:
        return []
    graph_path = [v_inx]
    # Prevent infinity-loops
    inx = 0
    while u_inx != v_inx and inx < len(predecessors):
        v_inx = predecessors[v_inx]
        graph_path.append(v_inx)
        inx += 1
    return graph_path[::-1]


def reconstruct_path_2d(predecessors, u_inx, v_inx, graph):
    """
    Reconstructs path from u to v based on the predecessors matrix.

    :param predecessors: list of lists
    :param u_inx: Vertex
    :param v_inx: Vertex
    :return: list
    """
    if predecessors[u_inx][v_inx] is None:
        return []
    graph_path = [v_inx]
    # Prevent infinity-loops
    inx = 0
    while u_inx != v_inx and inx < len(predecessors):
        v_inx = predecessors[u_inx][v_inx]
        graph_path.append(v_inx)
        inx += 1
    return graph_path[::-1]

def bellman_ford(graph, source):
    """
    :param vertices: list
    :param edges: list
    :param source: Vertex
    :return: (weights, predecessors)
    """
    vertices = graph.vertices
    edges = graph.get_edges()

    cost = [0 for i in xrange(len(vertices))]
    predecessor = [None for i in xrange(len(vertices))]

    # Step 1: initialize graph
    for v in vertices:
        if settings.INTEGER_VERTICES:
            v_pos = v
        else:
            v_pos = graph.get_vertex_position(v)
        cost[v_pos] = 0 if v is source else INF

    # Step 2: relax edges repeatedly
    inx = 0
    total_iterations = (len(vertices) - 1) * len(edges)
    iterations_per_one_percent = total_iterations / 100
    print "[BELL] Total iterations = %d" % total_iterations
    for i in xrange(len(vertices)-1):
        for e in edges:
            if settings.INTEGER_VERTICES:
                u = e.vertex_from
                v = e.vertex_to
            else:
                u = graph.get_vertex_position(e.vertex_from)
                v = graph.get_vertex_position(e.vertex_to)
            w = e.weight
            if cost[u] + w < cost[v]:
                cost[v] = cost[u] + w
                predecessor[v] = u
            inx += 1
            if iterations_per_one_percent == 0:
                print "[BELL] %d%% finished" % (inx * 100 / total_iterations)
            elif inx % iterations_per_one_percent == 0:
                print "[BELL] %d%% finished" % (inx / iterations_per_one_percent)

    # Step 3: check for negative-weight cycles
    for e in edges:
        u = graph.get_vertex_position(e.vertex_from)
        v = graph.get_vertex_position(e.vertex_to)
        w = e.weight
        if cost[u] + w < cost[v]:
            raise RuntimeError("Graph contains a negative-weight cycle")

    return (cost, predecessor)
