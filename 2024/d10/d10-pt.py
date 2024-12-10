import sys

from collections import defaultdict

file = open(sys.argv[1]).read()


def maybe_int(x):
    try: return int(x)
    except: return None
grid = [list(map(maybe_int, line)) for line in file.strip().splitlines()]
num_rows, num_cols = len(grid), len(grid[0])


num_to_coords = defaultdict(lambda: [])
for i, row in enumerate(grid):
    for j, val in enumerate(row):
        num_to_coords[val].append((i, j))


summits = defaultdict(lambda: set())

for i in range(9, -1, -1):
    print(i)
    coords = num_to_coords[i]
    if i == 9:
        for c in coords:
            summits[c] |= {c}
    else:
        prev = set(num_to_coords[i + 1])
        for i, j in coords:
            for di, dj in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                i2, j2 = i + di, j + dj
                if (i2,j2) in prev :
                    summits[(i, j)] |= summits[(i2, j2)]
        # (for c in prev)

total = 0

for zero in num_to_coords[0]:
    print(summits[zero])
    total += len(summits[zero])
print(total)
