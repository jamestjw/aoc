"""
This file contains a code attempt for advent of code day 16
"""


import re
import networkx as nx
import matplotlib.pyplot as plt
from itertools import chain

if __name__ == "__main__":
    my_tests = open("input.txt", "r", encoding="utf-8").read().splitlines()
    my_tests = open("smol.txt", "r", encoding="utf-8").read().splitlines()
    my_tests = [
        (int(re.search("(\d+)", x).groups()[0]), re.findall("[A-Z]{2}", x))
        for x in my_tests
    ]
    # rate, valvename, adjacent_to
    my_tests = [(rate, valves[0], valves[1:]) for rate, valves in my_tests]
    valves = {name: (rate, adjacent) for rate, name, adjacent in my_tests}
    edges = list(
        chain(*[[(name, adj) for adj in adjs] for name, (_, adjs) in valves.items()])
    )

    G = nx.DiGraph(directed=True)
    G.add_edges_from(edges)

    colors = ["yellow" if valves[node][0] > 0 else "green" for node in G.nodes()]
    colors[list(G.nodes()).index('AA')] = 'red'
    label_dict = {node: f"{node}\n{valves[node][0]}" if valves[node][0] > 0 else node for node in G.nodes()}
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color=colors)
    nx.draw_networkx_edges(G, pos, edge_color="r", arrows=None)
    nx.draw_networkx_labels(G, pos,labels=label_dict)

    plt.show()
