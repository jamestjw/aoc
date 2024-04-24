import sys
import re
from z3 import *
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
    s = Solver()
    t1 = Real("t1")
    t2 = Real("t2")

    dest_x1 = x1 + t1 * dx1
    dest_y1 = y1 + t1 * dy1
    dest_x2 = x2 + t2 * dx2
    dest_y2 = y2 + t2 * dy2

    s.add(t1 >= 0)
    s.add(t2 >= 0)
    s.add(dest_x1 == dest_x2)
    s.add(dest_y1 == dest_y2)
    s.add(dest_x1 >= min_x)
    s.add(dest_y1 >= min_x)
    s.add(dest_x1 <= max_x)
    s.add(dest_y1 <= max_x)

    if s.check() == sat:
        success += 1
        # model = s.model()
        # print(model)
        # print((x1,y1,z1,dx1,dy1,dz1),(x2,y2,z2,dx2,dy2,dz2))

print(success)
