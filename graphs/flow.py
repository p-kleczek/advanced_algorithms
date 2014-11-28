from graphs.search import *
import settings

__author__ = 'pawel'


def ford_fulkerson(graph, source, target):
    if not settings.INTEGER_VERTICES:
        raise NotImplementedError()

    if not settings.SURPRESS_OUTPUT:
        print "Start Ford-Fulkerson..."

    n = len(graph.vertices)
    flow = [[0 for i in xrange(n)] for j in xrange(n)]

    path = dfs_path_residual(graph, flow, source, target)
    num_paths = 0
    while path:
        num_paths += 1
        min_capacity = min([edge.weight for edge in path])
        for edge in path:
            flow[edge.vertex_from][edge.vertex_to] = flow[edge.vertex_from][edge.vertex_to] + min_capacity
            flow[edge.vertex_to][edge.vertex_from] = flow[edge.vertex_to][edge.vertex_from] - min_capacity
        path = dfs_path_residual(graph, flow, source, target)

        if not settings.SURPRESS_OUTPUT:
            if num_paths % 100 == 0:
                print "Paths processed: ", num_paths

    return flow


def max_flow(graph, source, target):
    """
    :return: flow matrix, max_flow(source, target)
    """
    flow = ford_fulkerson(graph, source, target)
    print flow
    return flow, sum(flow[source])
