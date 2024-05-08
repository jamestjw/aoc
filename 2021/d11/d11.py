import sys
import copy

lines = open(sys.argv[1]).read().splitlines()
grid = [list(map(int, line)) for line in lines]


def add1(grid):
    return [[e + 1 for e in row] for row in grid]


# Do one timestep
def simulate(grid):
    grid = copy.deepcopy(grid)
    flashed = set()
    num_rows = len(grid)
    num_cols = len(grid[0])

    grid = add1(grid)
    Q = []

    for i, row in enumerate(grid):
        for j, e in enumerate(row):
            if e > 9:
                Q.append((i, j))

    while len(Q) != 0:
        i, j = coords = Q.pop(0)
        flashed.add(coords)

        for di, dj in [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]:
            i2, j2 = i + di, j + dj
            if 0 <= i2 < num_rows and 0 <= j2 < num_cols:
                grid[i2][j2] += 1
                if grid[i2][j2] == 10:
                    Q.append((i2, j2))  # First time flashing

    for i, j in flashed:
        grid[i][j] = 0 # used up energy

    return grid, len(flashed)


flashes = 0
curr = grid
for i in range(100):
    curr, count = simulate(curr)
    flashes += count

print(flashes)

curr = grid
objective = len(grid) * len(grid[0])
iter = 1
while True:
    curr, count = simulate(curr)
    if count == objective:
        print(iter)
        break
    iter += 1
