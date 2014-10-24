# -*- coding: utf-8 -*-

import sys

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
    INF = sys.maxint
    n = len(graph.vertices)
    distances = [[[INF] * n] * n]
    predecessors = [[[None] * n] * n]
    for v in graph.vertices:
        x = graph.get_vertex_position(v)
        distances[x][x] = 0
    for e in graph.get_edges():
        x = graph.get_vertex_position(e.vertex_from)
        y = graph.get_vertex_position(e.vertex_to)
        distances[x][y] = e.weight
        predecessors[x][y] = e.vertex_from

    for u in graph.vertices:
        u_pos = graph.get_vertex_position(u)
        for v1 in graph.vertices:
            v1_pos = graph.get_vertex_position(v1)
            for v2 in graph.vertices:
                v2_pos = graph.get_vertex_position(v2)
                old_distance = distances[v1_pos][u_pos] + distances[u_pos][v2_pos]
                if distances[v1_pos][v2_pos] > old_distance:
                    distances[v1_pos][v2_pos] = old_distance
                    predecessors[v1_pos][v2_pos] = predecessors[u_pos][v2_pos]
    return predecessors


floyd_warshall(None)