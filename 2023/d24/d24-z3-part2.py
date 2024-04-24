import sys
import re
from z3 import *

file = open(sys.argv[1]).read().strip().split("\n")

data = []

for row in file:
    data.append([int(e) for e in re.findall(r"-?\d+", row)])

s = Solver()
x, y, z, dx, dy, dz = Ints("x y z dx dy dz")
for i, (x1, y1, z1, dx1, dy1, dz1) in enumerate(data):
    time = Int(f"t{i}")

    s.add(time >= 0)
    s.add(x + time * dx == x1 + time * dx1)
    s.add(y + time * dy == y1 + time * dy1)
    s.add(z + time * dz == z1 + time * dz1)

if s.check() == sat:
    model = s.model()
    print(model[x].as_long() + model[y].as_long() + model[z].as_long())
else:
    print("Failed")
