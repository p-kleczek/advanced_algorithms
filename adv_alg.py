from graphs.graph import MatrixGraph, read_graph
from graphs.shortest_paths import floyd_warshall, reconstruct_path
from utils.print_utils import print_2d

__author__ = 'pawel'

g = MatrixGraph()
read_graph('data/floyd_warshall_2.graph', g)
# print 'G'
# print g

pred = floyd_warshall(g)
# print g

print_2d(pred)

# print graph_path(pred, 0, 3)
for i in xrange(g.get_vertices_count()):
    for j in xrange(g.get_vertices_count()):
        # print i, j
        pth = reconstruct_path(pred, i, j)
        if pth:
            print pth
