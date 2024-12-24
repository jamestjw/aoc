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
    return k, L


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
    _, degen_ordering = get_degeneracy_ordering(vertices, adjacency)
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
