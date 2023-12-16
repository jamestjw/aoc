import sys

file = open(sys.argv[1]).read().split("\n")
grid = [list(row) for row in file]
max_i, max_j = len(grid), len(grid[0])


def valid_coords(coords):
    i, j = coords
    return 0 <= i < max_i and 0 <= j < max_j


def move(coord, offset):
    return coord[0] + offset[0], coord[1] + offset[1]


def do_beam(
    curr_pos: tuple[int, int],
    direction: tuple[int, int],
):
    to_visit = [(curr_pos, direction)]
    visited = set()

    while to_visit:
        curr_pos, direction = to_visit.pop()
        i, j = next_coords = move(curr_pos, direction)

        if not valid_coords(next_coords):
            continue

        if (next_coords, direction) in visited:
            continue
        else:
            visited |= {(next_coords, direction)}

        match grid[i][j]:
            case ".":
                to_visit.append((next_coords, direction))
            case "/":
                to_visit.append((next_coords, (-direction[1], -direction[0])))

            case "\\":
                to_visit.append((next_coords, (direction[1], direction[0])))

            case "|":
                if direction in ((1, 0), (-1, 0)):
                    to_visit.append((next_coords, direction))

                else:
                    to_visit.append((next_coords, (1, 0)))
                    to_visit.append((next_coords, (-1, 0)))

            case "-":
                if direction in ((0, 1), (0, -1)):
                    to_visit.append((next_coords, direction))

                else:
                    to_visit.append((next_coords, (0, 1)))
                    to_visit.append((next_coords, (0, -1)))

            case _:
                raise Exception
    return [e for e, _ in visited]


def print_grid(grid, coords):
    for i in range(max_i):
        for j in range(max_j):
            print("#" if (i, j) in coords else ".", end="")
        print("")


def get_len(start, direction):
    return len(set(do_beam(start, direction)))

print(get_len((0, -1), (0, 1)))

inputs = []

for i in range(max_i):
    inputs.append(((i, -1), (0, 1)))
    inputs.append(((i, max_j), (0, -1)))


for j in range(max_j):
    inputs.append(((-1, j), (1, 0)))
    inputs.append(((max_i, j), (-1, 0)))


print(max(get_len(c, d) for c, d in inputs))
