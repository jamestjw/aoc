from itertools import combinations
import math


def dist(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2


inp = [tuple(map(int, l.split(","))) for l in open(0).read().splitlines()]
pairs = list(combinations(inp, 2))
pairs_with_dist = [(p, dist(*p)) for p in pairs]
pairs_with_dist.sort(key=lambda x: x[1])


connections = 0
circuits = {p: {p} for p in inp}
# while connections < 1000:
while True:
    (p1, p2), dist = pairs_with_dist.pop(0)
    p1_circuit = circuits.get(p1, set())
    p2_circuit = circuits.get(p2, set())
    connections += 1
    # print(p1, p2, p1_circuit, p2_circuit)
    if p1_circuit == p2_circuit:
        continue
    new_circuit = p1_circuit | p2_circuit

    for c in new_circuit:
        circuits[c] = new_circuit

    if len(new_circuit) == len(inp):
        print(p1[0] * p2[0])
        # 6095621910
        break

# part 1
# print(math.prod(sorted([len(s) for s in set([tuple(v) for v in circuits.values()])], reverse=True)[:3]))
