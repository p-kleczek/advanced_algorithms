from graphs.graph import MatrixGraph, Edge, ListGraph, read_graph

__author__ = 'pawel'

lg = ListGraph()
mg = MatrixGraph()

filename = 'data/graf.txt'
read_graph(filename, lg)
read_graph(filename, mg)

print 'MATRIX graph'
print mg
print "\nControl sum = %s " % sum([e.weight for e in mg.get_edges() if e.vertex_from < e.vertex_to])
print
print 'LIST graph'
print lg
print "\nControl sum = %s " % sum([e.weight for e in lg.get_edges() if e.vertex_from < e.vertex_to])