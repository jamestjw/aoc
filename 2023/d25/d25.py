# from graph import *
import networkx as nx
import sys
import re
import math

file = open(sys.argv[1]).read().strip().split("\n")
edges = [re.findall(r"\w+", line) for line in file]

num_edges = sum(len(l) - 1 for l in edges)
vertices = list({e for l in edges for e in l})

G = nx.Graph()
G.add_nodes_from(vertices)

for e in edges:
    src = e[0]
    dests = e[1:]

    for dest in dests:
        G.add_edge(src, dest, capacity=1)

v1 = vertices[0]
for v2 in vertices[1:]:
    cut, partition = nx.minimum_cut(G, v1, v2)
    print(cut, math.prod([len(s) for s in partition]))
    if cut == 3:
        break
