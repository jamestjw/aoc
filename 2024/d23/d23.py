import sys
from collections import defaultdict

sys.path.insert(0, "../..")

from lib.graph.clique import get_maximum_clique

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


maximal_clique = get_maximum_clique(list(connections.keys()), connections)
print("part2", ",".join(sorted(maximal_clique)))
