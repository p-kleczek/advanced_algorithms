from datetime import datetime

from graphs.graph import MatrixGraph, read_graph, ListGraph
from graphs.shortest_paths import floyd_warshall, reconstruct_path


__author__ = 'pawel'


def lab2():
    def measure_performance(graph):
        read_graph('data/duzy_graf.txt', graph)
        print "Graph read"
        start_time = datetime.now()
        floyd_warshall(graph)
        print "Graph processed"
        end_time = datetime.now()
        return end_time - start_time

    t_matrix = measure_performance(MatrixGraph())
    t_list = measure_performance(ListGraph())
    print "R = %.2f" % (t_list.total_seconds() / t_matrix.total_seconds())
    # R = 1.01

    graph = MatrixGraph()
    read_graph('data/duzy_graf.txt', graph)
    predecessors = floyd_warshall(graph)

    # inx_from = graph.get_vertex_position(graph.get_vertex(109))
    # inx_to = graph.get_vertex_position(graph.get_vertex(609))
    # _path = reconstruct_path(predecessors, 0, 3)
    # print _path


lab2()
