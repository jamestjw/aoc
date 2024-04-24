import sys
import re
from itertools import combinations
from tqdm import tqdm

file = open(sys.argv[1]).read().strip().split("\n")

data = []

for row in file:
    data.append([int(e) for e in re.findall(r"-?\d+", row)])

success = 0
min_x = 200000000000000
max_x = 400000000000000

# min_x = 7
# max_x = 27

for (x1, y1, z1, dx1, dy1, dz1), (x2, y2, z2, dx2, dy2, dz2) in tqdm(
    combinations(data, 2)
):
    if (dx2 - (dx1 * dy2 / dy1)) == 0:
        continue

    t2 = ((dx1 * (y2 - y1) / dy1) + x1 - x2) / (dx2 - (dx1 * dy2 / dy1))
    t1 = (x2 + dx2 * t2 - x1) / dx1

    if not (0 <= t1 and 0 <= t2):
        continue

    if not min_x <= x1 + dx1 * t1 <= max_x:
        continue

    if not min_x <= y1 + dy1 * t1 <= max_x:
        continue
    success += 1

    # print((x1, y1, z1, dx1, dy1, dz1), (x2, y2, z2, dx2, dy2, dz2))
    # print(x1 + dx1 * t1, y1 + dy1 * t1)

print(success)
