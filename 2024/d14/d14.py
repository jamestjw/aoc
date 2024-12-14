import sys
import math
import re
from collections import defaultdict

file = open(sys.argv[1]).read()
lines = [list(map(int, re.findall(r"-?\d+", e))) for e in file.strip().splitlines()]


max_x = 101
max_y = 103


def calc_metric(counts):
    q1, q2, q3, q4 = [0] * 4
    for coords, c in counts.items():
        x, y = coords
        if 0 <= x < max_x // 2 and 0 <= y < max_y // 2:
            q1 += c
        elif 0 <= x < max_x // 2 and max_y / 2 < y:
            q2 += c
        elif max_x / 2 < x and 0 <= y < max_y // 2:
            q3 += c
        elif max_x / 2 < x and max_y // 2 < y:
            q4 += c

    return math.prod([q1, q2, q3, q4])


def pp_grid(d):
    val = set(d.values())
    for j in range(max_y):
        for i in range(max_x):
            print("*" if (i, j) in val else ".", end="")
        print("")


coords_dict = {i: (x0, y0) for i, (x0, y0, _, _) in enumerate(lines)}

iter = 1
metrics = []
configs = {}
while True:
    counts = defaultdict(lambda: 0)
    for i, (_, _, dx, dy) in enumerate(lines):
        curr = coords_dict[i]
        x, y = curr
        x2, y2 = x + dx, y + dy
        if x2 < 0:
            x2 += max_x
        if x2 >= max_x:
            x2 -= max_x
        if y2 < 0:
            y2 += max_y
        if y2 >= max_y:
            y2 -= max_y
        coords_dict[i] = x2, y2
        counts[(x2, y2)] += 1
    metric = calc_metric(counts)
    metrics.append((metric, iter))
    configs[iter] = coords_dict.copy()

    iter += 1
    if iter > 10000:
        break

for _, i in sorted(metrics, key=lambda x: x[0])[:10][::-1]:
    print(f"iter: {i}")
    pp_grid(configs[i])
