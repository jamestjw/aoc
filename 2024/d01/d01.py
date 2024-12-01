import sys
from collections import Counter

file = open(sys.argv[1]).read()

inp_lines = [tuple(map(int, l.split())) for l in file.splitlines()]
left, right = list(zip(*inp_lines))

print(sum(abs(l - r) for l, r in zip(sorted(left), sorted(right))))

counter = Counter(right)

print(sum([l * counter.get(l, 0) for l in left]))
