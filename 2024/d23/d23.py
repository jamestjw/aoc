import sys
from collections import defaultdict

file = open(sys.argv[1]).read()
pairs = [e.split("-") for e in file.splitlines()]

connections = defaultdict(lambda: set())
for p1, p2 in pairs:
    connections[p1] |= {p2}
    connections[p2] |= {p1}

groups = []
for root, others in connections.items():
    for o in others:
        inter = (connections[o] - {root}) & (others - {o})
        for third in inter:
            groups.append(tuple(sorted([root, o, third])))


def has_t(group):
    return any(node.startswith("t") for node in group)


print("part1", len(list(filter(has_t, set(groups)))))


def get_degeneracy_ordering(vertices, adjacency):
    L = []
    d = {v: len(adjacency[v]) for v in vertices}
    D = [list() for _ in range(max(d.values()) + 1)]
    for v, degree in d.items():
        D[degree].append(v)
    k = 0
    for _ in range(len(vertices)):
        i, vs = next((i, vs) for i, vs in enumerate(D) if vs)
        k = max(k, i)
        v = vs.pop()
        L.insert(0, v)
        for w in adjacency[v] - set(L):
            D[d[w]].remove(w)
            d[w] -= 1
            D[d[w]].append(w)
    return L


def bron_kerbosch_with_pivot(r, p, x, adjacency, acc=[]):
    """
    r -- potential clique
    p -- remaining vertices
    x -- skipped vertices
    """
    if len(p) == 0 and len(x) == 0:
        return acc + [r]

    # Choose the node with the most neighbors to be the pivot,
    # this minimises the number of branches below
    pivot = sorted(p | x, key=lambda x: len(adjacency[x]))[-1]
    for v in list(p - set(adjacency[pivot])):
        acc = bron_kerbosch_with_pivot(
            r | {v}, p & adjacency[v], x & adjacency[v], adjacency, acc
        )
        p -= {v}
        x |= {v}
    return acc


# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
# Proven to be efficient for graphs of small degeneracy
def bron_kerbosch_with_ordering(vertices: list, adjacency: dict):
    degen_ordering = get_degeneracy_ordering(vertices, adjacency)
    p = set(vertices)
    r, x = set(), set()
    acc = []
    for v in degen_ordering:
        acc = bron_kerbosch_with_pivot(
            r | {v}, p & adjacency[v], x & adjacency[v], adjacency, acc
        )
        p -= {v}
        x |= {v}
    return acc


def bron_kerbosch(vertices: list, adjacency: dict):
    return bron_kerbosch_with_pivot(set(), set(vertices), set(), adjacency)


def get_maximum_clique(vertices, adjacency):
    cliques = bron_kerbosch(vertices, adjacency)
    maximal_clique = sorted(cliques, key=len)[-1]
    return maximal_clique


maximal_clique = get_maximum_clique(list(connections.keys()), connections)
print("part2", ",".join(sorted(maximal_clique)))
