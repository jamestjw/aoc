import sys
from functools import lru_cache

file = open(sys.argv[1]).read()


grid = [list(e) for e in file.strip().splitlines()]
num_rows = len(grid)
num_cols = len(grid[0])
grid = {complex(i, j): v for i, row in enumerate(grid) for j, v in enumerate(row)}

groups = []

to_visit = set(grid.keys())


def in_grid(coords):
    return 0 <= coords.real < num_rows and 0 <= coords.imag < num_cols


while to_visit:
    print("new group")
    curr = to_visit.pop()
    group = {curr}
    queue = {curr}

    while len(queue):
        curr = queue.pop()
        print(curr, grid[curr])
        group.add(curr)
        to_visit -= {curr}
        for delta in (1, -1, 1j, -1j):
            coords2 = curr + delta
            if not in_grid(coords2):
                continue
            if (
                coords2 in to_visit
                and coords2 not in group
                and grid[coords2] == grid[curr]
            ):
                queue.add(coords2)

    groups.append(group)

print(groups)

total = 0
for group in groups:
    area =len(group)
    perimeter = 0
    for curr in group:
        for delta in (1, -1, 1j, -1j):
            coords2 = curr + delta
            if grid.get(coords2) != grid[curr]:
                perimeter += 1
    print(grid[curr]) # type: ignore
    print("area: ", len(group))
    print("perimeter: ", perimeter)
    total += area * perimeter
print(total)
