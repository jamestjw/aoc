import sys
from functools import reduce
import math

grid = [[int(e) for e in line] for line in open(sys.argv[1]).read().splitlines()]
num_rows = len(grid)
num_cols = len(grid[0])

lows = []
for i in range(num_rows):
    for j in range(num_cols):
        neighbours = []
        here = grid[i][j]
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            i2, j2 = i + di, j + dj
            if 0 <= i2 < num_rows and 0 <= j2 < num_cols:
                neighbours.append(grid[i2][j2])

        if all(here < n for n in neighbours):
            lows.append((i, j))

print(sum(grid[i][j] + 1 for i, j in lows))


basin_sizes = []

for i, j in lows:
    basin = set()
    worklist = [(i, j)]

    while len(worklist) != 0:
        i, j = coord = worklist.pop()

        if coord not in basin:
            basin |= {coord}

        here = grid[i][j]

        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            i2, j2 = i + di, j + dj
            if 0 <= i2 < num_rows and 0 <= j2 < num_cols:
                neighbour = grid[i2][j2]
                if neighbour > here and neighbour != 9:
                    worklist.append((i2, j2))

    basin_sizes.append(len(basin))


print(math.prod(sorted(basin_sizes)[::-1][:3]))
