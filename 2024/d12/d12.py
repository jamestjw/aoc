import sys
from collections import defaultdict

file = open(sys.argv[1]).read()


grid = [list(e) for e in file.strip().splitlines()]
num_rows, num_cols = len(grid), len(grid[0])
grid = {complex(i, j): v for i, row in enumerate(grid) for j, v in enumerate(row)}


def in_grid(coords):
    return 0 <= coords.real < num_rows and 0 <= coords.imag < num_cols


groups = []
to_visit = set(grid.keys())

while to_visit:
    curr = to_visit.pop()
    group = []
    queue = {curr}

    while len(queue):
        curr = queue.pop()
        group.append(curr)
        to_visit -= {curr}
        for delta in (1, -1, 1j, -1j):
            coords2 = curr + delta
            if (
                in_grid(coords2)
                and coords2 not in group
                and grid[coords2] == grid[curr]
            ):
                queue.add(coords2)

    groups.append(group)

part1 = 0
part2 = 0

for group in groups:
    area = len(group)
    side_pieces = defaultdict(lambda: set())
    for curr in group:
        for delta in (1, -1, 1j, -1j):
            coords2 = curr + delta
            if grid.get(coords2) != grid[curr]:
                side_pieces[delta].add(curr + delta)

    perimeter = sum(len(val) for val in side_pieces.values())

    sides = 0
    for side, dirs in [(1, [1j, -1j]), (-1, [1j, -1j]), (1j, [1, -1]), (-1j, [1, -1])]:
        pieces = set(side_pieces[side])
        while pieces:
            sides += 1
            piece = pieces.pop()

            for d in dirs:
                curr = piece
                while (curr + d) in pieces:
                    pieces.remove(curr + d)
                    curr += d

    part1 += area * perimeter
    part2 += area * sides

print(part1, part2)
