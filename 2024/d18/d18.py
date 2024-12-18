import math
import re
import sys

# To import lib
sys.path.insert(0, "../..")

from lib.search import *

file = open(sys.argv[1]).read()
blocks = [map(int, re.findall(r"\d+", line)) for line in file.strip().splitlines()]

num_rows, num_cols, num_fallen = 7, 7, 12
num_rows, num_cols, num_fallen = 71, 71, 1024

start, dest = (0, 0), (num_rows - 1, num_cols - 1)

grid = [[1.0] * num_cols for _ in range(num_rows)]

for x, y in blocks[:num_fallen]:
    grid[x][y] = math.inf


d = djikstra(BaseGrid(grid), dest)
print(d[(0, 0)] - 1)


for x, y in blocks[num_fallen:]:
    grid[x][y] = math.inf
    if start not in djikstra(BaseGrid(grid), dest):
        print(f"{x},{y}")
        break
