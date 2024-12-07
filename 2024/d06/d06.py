import sys

file = open(sys.argv[1]).read()

grid = [list(line) for line in file.splitlines()]
num_rows, num_cols = len(grid), len(grid[0])
start = next(
    (i + j * (1j))
    for i in range(num_rows)
    for j in range(num_cols)
    if grid[i][j] == "^"
)
start_direction = -1 + 0j

directions = [(-1 + 0j), (0 + 1j), (1 + 0j), (0 - 1j)]


def get(coords):
    return grid[int(coords.real)][int(coords.imag)]


def assign(coords, v):
    grid[int(coords.real)][int(coords.imag)] = v


def rotate(offset):
    return directions[(directions.index(offset) + 1) % 4]


def patrol():
    visited = {start}
    entered_from = {(start - start_direction, start_direction)}
    curr = start
    direction = start_direction

    while True:
        next_coords = curr + direction
        if not (0 <= next_coords.real < num_rows and 0 <= next_coords.imag < num_cols):
            break
        if get(next_coords) == "#":
            direction = rotate(direction)
            continue
        visited.add(next_coords)
        entry_pair = curr, direction
        if entry_pair in entered_from:
            return visited, True

        entered_from.add(entry_pair)
        curr = next_coords
    return visited, False


visited, _ = patrol()
print(len(visited))

count = 0
blockades = set()
for blockade in visited:
    if blockade == start:
        continue
    assign(blockade, "#")
    _, looped = patrol()
    if looped:
        blockades.add(blockade)
    assign(blockade, ".")

print(len(blockades))
