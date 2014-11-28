from datetime import datetime
from graphs.flow import *

from graphs.graph import *
from graphs.search import *
from graphs.shortest_paths import *
import settings
from utils.print_utils import print_2d


__author__ = 'pawel'


def lab2():
    def measure_performance(graph):
        # read_graph('data/floyd_warshall_2.graph', graph)
        read_graph('data/duzy_graf.txt', graph)
        print "Graph read"
        start_time = datetime.now()
        pred = floyd_warshall(graph)
        print "Graph processed"
        end_time = datetime.now()

        filename = "stats/floyd_warshall/" + graph.__class__.__name__
        f = open(filename, 'w')
        for v in graph.vertices:
            f.write(str(v) + " ")
        f.write('\n')
        for row in pred:
            for item in row:
                f.write(str(item) + " ")
            f.write('\n')
        f.close()
        return end_time - start_time, pred

    # t_matrix, _ = measure_performance(MatrixGraph())
    graph = ListGraph()
    t_list, predecessors = measure_performance(graph)
    # print "R = %.2f" % (t_list.total_seconds() / t_matrix.total_seconds())
    # R = 0.96

    from_label = 109  #109
    to_label = 609    #609
    inx_from = graph.get_vertex_position(graph.get_vertex(from_label))
    inx_to = graph.get_vertex_position(graph.get_vertex(to_label))
    _path = reconstruct_path(predecessors, inx_from, inx_to, graph)
    data = {
        'from': from_label,
        'to': to_label,
        'path': _path
    }
    print "Path (%(from)d -> %(to)d): %(path)s" % data
    # [109, 713, 870, 614, 808, 609]


def lab3():
    def measure_performance(graph):
        if settings.DEBUG:
            read_graph('data/floyd_warshall_2.graph', graph)
        else:
            read_graph('data/duzy_graf.txt', graph)
        print "Graph read"
        start_time = datetime.now()

        if settings.DEBUG:
            source = graph.vertices[0]
        else:
            source = graph.get_vertex(109)
        weights, pred = bellman_ford(graph, source)

        print "Graph processed"
        end_time = datetime.now()

        if not settings.DEBUG:
            filename = "stats/bellman_ford/" + graph.__class__.__name__
            f = open(filename, 'w')
            for v in graph.vertices:
                f.write(str(v) + " ")
            f.write('\n')
            for item in pred:
                f.write(str(item) + " ")
            f.close()
        return end_time - start_time, pred, weights

    # if not debug:
    #     t_matrix, _, _ = measure_performance(MatrixGraph())
    graph = ListGraph()
    t_list, predecessors, weights = measure_performance(graph)

    # if not debug:
    #     print "R = %.2f" % (t_list.total_seconds() / t_matrix.total_seconds())
        # R = 0.96

    if settings.DEBUG:
        from_label = 0
        to_label = 2
    else:
        from_label = 109
        to_label = 609

    if settings.INTEGER_VERTICES:
        inx_from = from_label
        inx_to = to_label
    else:
        inx_from = graph.get_vertex_position(graph.get_vertex(from_label))
        inx_to = graph.get_vertex_position(graph.get_vertex(to_label))
    _path = reconstruct_path(predecessors, inx_from, inx_to, graph)
    data = {
        'from': from_label,
        'to': to_label,
        'path': _path
    }
    print "Path (%(from)d -> %(to)d): %(path)s" % data
    # Path (109 -> 609): [109, 713, 870, 614, 808, 609]

    for i in xrange(len(graph.vertices)):
        if settings.INTEGER_VERTICES:
            data = {
                'from': from_label,
                'to': i,
                'cost': weights[i]
            }
        else:
            data = {
                'from': from_label,
                'to': graph.vertices[i].label,
                'cost': weights[i]
            }
        print "Cost (%(from)d -> %(to)d): %(cost)s" % data


def lab4():
    graph = ListGraph()
    if settings.DEBUG:
        read_graph('data/floyd_warshall_2.graph', graph)
        print max_flow(graph, 0, 2)
    else:
        read_graph('data/duzy_graf.txt', graph)
        print "Graph read"
        print max_flow(graph, 109, 609)
#         10738

lab4()
