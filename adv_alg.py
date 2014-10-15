from graphs.graph import MatrixGraph, Edge, ListGraph

__author__ = 'pawel'

# g = ListGraph()
g = MatrixGraph()

_id = 1
with open('data/graf.txt') as f:
    for line in f:
        vals = line.strip().split(', ')
        e = Edge(_id, int(vals[0]), int(vals[1]), int(vals[2]))
        _id += 1
        g.add_edge(e)

print g