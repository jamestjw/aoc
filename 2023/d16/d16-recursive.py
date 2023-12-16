import sys
from functools import cache

sys.setrecursionlimit(5000)

file = open(sys.argv[1]).read().split("\n")
grid = [list(row) for row in file]
max_i, max_j = len(grid), len(grid[0])


def valid_coords(coords):
    i, j = coords
    return 0 <= i < max_i and 0 <= j < max_j


def move(coord, offset):
    return coord[0] + offset[0], coord[1] + offset[1]


@cache
def do_beam(curr_pos: tuple[int, int], direction: tuple[int, int]):
    global visited

    delta_i, delta_j = next_coords = move(curr_pos, direction)

    if not valid_coords(next_coords) or (curr_pos, direction) in visited:
        visited |= {(curr_pos, direction)}
        return
    else:
        visited |= {(curr_pos, direction)}

    match grid[delta_i][delta_j]:
        case ".":
            do_beam(next_coords, direction)
        case "/":
            # flip and negate
            do_beam(next_coords, (-direction[1], -direction[0]))
        case "\\":
            # flip
            do_beam(next_coords, (direction[1], direction[0]))
        case "|":
            if direction in ((1, 0), (-1, 0)):
                do_beam(next_coords, direction)
            else:
                do_beam(next_coords, (1, 0))
                do_beam(next_coords, (-1, 0))
        case "-":
            if direction in ((0, 1), (0, -1)):
                do_beam(next_coords, direction)
            else:
                do_beam(next_coords, (0, 1))
                do_beam(next_coords, (0, -1))
        case _:
            raise Exception


def print_grid(grid, coords):
    for i in range(max_i):
        for j in range(max_j):
            print("#" if (i, j) in coords else ".", end="")
        print("")


def get_max(start, direction):
    global visited
    visited = set()

    do_beam.cache_clear()
    do_beam(start, direction)

    visited_coords = set(e for e, _ in visited if valid_coords(e))

    return len(visited_coords)


print(get_max((0, -1), (0, 1)))


inputs = []

for i in range(max_i):
    inputs.append(((i, -1), (0, 1)))
    inputs.append(((i, max_j), (0, -1)))


for j in range(max_j):
    inputs.append(((-1, j), (1, 0)))
    inputs.append(((max_i, j), (-1, 0)))


print(max(get_max(c, d) for c, d in inputs))
