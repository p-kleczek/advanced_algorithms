from graphs.graph import MatrixGraph, Edge, ListGraph

__author__ = 'pawel'

lg = ListGraph()
mg = MatrixGraph()

_id = 1
with open('data/graf.txt') as f:
    for line in f:
        vals = line.strip().split('; ')
        e = Edge(_id, int(vals[0]), int(vals[1]), int(vals[2]))
        _id += 1
        lg.add_edge(e)
        mg.add_edge(e)

print 'MATRIX graph'
print mg
print "\nControl sum = %s " % (sum ([e.weight for e in mg._get_edges() if e.vertex_from < e.vertex_to]), )
print
print 'LIST graph'
print lg
print "\nControl sum = %s " % (sum ([e.weight for e in lg._get_edges() if e.vertex_from < e.vertex_to]), )