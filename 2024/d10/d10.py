import sys
from collections import defaultdict

file = open(sys.argv[1]).read()


grid = [list(map(int, line)) for line in file.strip().splitlines()]


num_to_coords = defaultdict(lambda: [])
for i, row in enumerate(grid):
    for j, val in enumerate(row):
        num_to_coords[val].append(complex(i, j))


pt1_dict, pt2_dict = defaultdict(lambda: set()), defaultdict(lambda: 0)

for height in range(9, -1, -1):
    for c in num_to_coords[height]:
        if height == 9:
            pt1_dict[c] = {c}
            pt2_dict[c] = 1
        else:
            for delta in [1, 1j, -1, -1j]:
                if c + delta in num_to_coords[height + 1]:
                    pt1_dict[c] |= pt1_dict[c + delta]
                    pt2_dict[c] += pt2_dict[c + delta]

print(sum(len(pt1_dict[s]) for s in num_to_coords[0]))
print(sum(pt2_dict[s] for s in num_to_coords[0]))
