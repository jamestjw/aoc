"""
This file contains a code attempt for advent of code day 12
"""

import numpy as np
from collections import defaultdict
import sys


def run(nodes, edges, source):
    """
    function Dijkstra(Graph, source)
        for each vertex v in Graph.Vertices:
            dist[v] ← INFINITY
            prev[v] ← UNDEFINED
            add v to Q
        dist[source] ← 0

        while Q is not empty:
            u ← vertex in Q with min dist[u]
            remove u from Q

            for each neighbor v of u still in Q:
                alt ← dist[u] + Graph.Edges(u, v)
                if alt < dist[v]:
                    dist[v] ← alt
                    prev[v] ← u

        return dist[], prev[]
    """
    dist = defaultdict(lambda: sys.maxsize)
    prev = defaultdict(lambda: None)
    unvisited = nodes.copy()

    dist[source] = 0

    while len(unvisited) > 0:
        u = min(unvisited, key=lambda x: dist[x])
        unvisited.remove(u)

        for neighbor in edges[u]:
            if neighbor in unvisited:
                alt = dist[u] + 1
                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    prev[neighbor] = u

    return dist


if __name__ == "__main__":
    lines = open("input.txt", "r", encoding="utf-8").read().splitlines()
    # lines = open("smol.txt", "r", encoding="utf-8").read().splitlines()
    grid = list(map(list, lines))
    numrows, numcols = len(grid), len(grid[0])
    S = next((i, row.index("S")) for i, row in enumerate(grid) if "S" in row)
    E = next((i, row.index("E")) for i, row in enumerate(grid) if "E" in row)
    grid[S[0]][S[1]] = "a"
    grid[E[0]][E[1]] = "z"
    grid = np.array(list(map(lambda x: [ord(x_) for x_ in x], grid)))

    nodes = []
    adjacency = defaultdict(list)

    for i in range(numrows):
        for j in range(numcols):
            nodes.append((i,j))
            for i_, j_ in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                new_i, new_j = i + i_, j + j_
                if new_i >= 0 and new_i < numrows and new_j >= 0 and new_j < numcols:
                    if (grid[new_i, new_j] - grid[i, j]) >= -1:
                        adjacency[(i,j)] += [(new_i, new_j)]

    a_coords = list(zip(*np.where(grid == ord("a"))))
    dist = run(nodes, adjacency, E)

    part1 = dist[S]
    part2 = min(dist[coord] for coord in a_coords)

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
