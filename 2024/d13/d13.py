import sys
import re
from z3 import *

file = open(sys.argv[1]).read()


file = [list(map(int, re.findall(r"\d+", e))) for e in file.strip().split("\n\n")]
offset = 10000000000000
# offset = 0

total = 0
for ax, ay, bx, by, target_x, target_y in file:
    s = Optimize()
    a = Int("a")
    b = Int("b")
    s.add(a * ax + b * bx == target_x + offset)
    s.add(a * ay + b * by == target_y + offset)
    s.minimize(3 * a + b)
    if s.check() == sat:
        model = s.model()
        total += model[a].as_long() * 3 + model[b].as_long()
print(total)
