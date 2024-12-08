import fractions
import sys
from collections import defaultdict
from itertools import combinations

file = open(sys.argv[1]).read()

grid = [list(line) for line in file.splitlines()]
num_rows, num_cols = len(grid), len(grid[0])

sats = defaultdict(lambda: [])

for i, row in enumerate(grid):
    for j, val in enumerate(row):
        if val != ".":
            sats[val].append((i, j))

res = set()
for sat, coords in sats.items():
    for (i1, j1), (i2, j2) in combinations(coords, 2):
        di, dj = i2 - i1, j2 - j1
        for i, j in [(i1 - di, j1 - dj), (i2 + di, j2 + dj)]:
            if 0 <= i < num_rows and 0 <= j < num_cols:
                res.add((i, j))

print(len(res))

res = set()
for sat, coords in sats.items():
    for (i1, j1), (i2, j2) in combinations(coords, 2):
        gradient = fractions.Fraction(i2 - i1, j2 - j1)
        y_intercept = i2 - gradient * j2
        for j in range(num_cols):
            i = gradient * j + y_intercept
            if i.is_integer() and 0 <= i < num_rows and 0 <= j < num_cols:
                res.add((i, j))

print(len(res))
