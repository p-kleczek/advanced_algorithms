__author__ = 'pawel'


def dfs_paths(graph, start, goal, positive=False):
    # Operates on vertices
    """
    :param graph:
    :param start:
    :param goal:
    :param positive: if True, only edges with positive weights are considered
    :return:
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        adj_edges = graph.get_adjacent_edges(vertex)
        if positive:
            adj_edges = filter(lambda edge: edge.weight > 0, adj_edges)
        next_vertices = set([e.vertex_to for e in adj_edges])
        for next_vertex in next_vertices - set(path):
            if next_vertex == goal:
                yield path + [next_vertex]
            else:
                stack.append((next_vertex, path + [next_vertex]))


def dfs_path_residual(graph, flow, start, goal):
    stack = [(start, [])]
    visited = [start]
    while stack:
        (vertex, path) = stack.pop()
        if vertex == goal:
            return path
        adj_edges = graph.get_outgoing_edges(vertex)
        is_residual = lambda edge: edge.weight - flow[edge.vertex_from][edge.vertex_to]> 0
        not_visited = lambda edge: edge.vertex_to not in visited
        is_ok = lambda edge: is_residual(edge) and not_visited(edge)
        residual_edges = filter(is_ok, adj_edges)
        for edge in residual_edges:
            visited.append(edge.vertex_to)
            if edge.vertex_to == goal:
                # print 'path', path + [edge]
                return path + [edge]
            else:
                stack.append((edge.vertex_to, path + [edge]))
