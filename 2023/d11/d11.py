import numpy as np
import sys

from itertools import combinations

file = open(sys.argv[1]).read()
inp_lines = file.splitlines()
grid = np.array(list(map(list, inp_lines)))

empty_rows = [i for i, line in enumerate(inp_lines) if not any(e == "#" for e in line)]
empty_cols = [
    i for i, line in enumerate(np.transpose(grid)) if not any(e == "#" for e in line)
]

galaxies = [(i, j) for i, j in zip(*np.where(grid == "#"))]


def do1(expansion_size):
    distances = []
    for (i1, j1), (i2, j2) in combinations(galaxies, 2):
        distance = abs(i1 - i2) + abs(j1 - j2)
        min_i = min(i1, i2)
        min_j = min(j1, j2)
        max_i = max(i1, i2)
        max_j = max(j1, j2)

        for row in empty_rows:
            if min_i < row < max_i:
                distance += expansion_size - 1
        for col in empty_cols:
            if min_j < col < max_j:
                distance += expansion_size - 1
        distances.append(distance)
    return distances


print(sum(do1(2)))
print(sum(do1(1000000)))
