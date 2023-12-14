import sys
import numpy as np

file = open(sys.argv[1]).read()
rows = file.split("\n")
grid = np.array(list(map(list, rows)))


def do1(grid):
    new_grid = np.copy(grid)
    new_grid[new_grid == "O"] = "."

    stone_indices = list(zip(*np.where(grid == "O")))
    for i, j in sorted(stone_indices, key=lambda x: (x[1], x[0])):
        obstacle_candidates = [
            index
            for index, e in enumerate(new_grid[:, j])
            if index < i and e in ("#", "O")
        ]
        obstacle_index = obstacle_candidates[-1] if len(obstacle_candidates) > 0 else -1
        new_grid[obstacle_index + 1, j] = "O"

    return new_grid


def do_cycle(grid):
    # north
    grid = do1(grid)
    # clockwise
    # west
    grid = do1(np.rot90(grid, axes=(1, 0)))
    # south
    grid = do1(np.rot90(grid, axes=(1, 0)))
    # east
    grid = do1(np.rot90(grid, axes=(1, 0)))
    return np.rot90(grid, axes=(1, 0))


def find_load(grid):
    max_rows, _ = grid.shape

    return sum([max_rows - i for i, _ in zip(*np.where(grid == "O"))])


print(find_load(do1(grid)))


curr_grid = np.copy(grid)
loads = []
for i in range(250):  # run the simulation for some number of cycles
    curr_grid = do_cycle(curr_grid)
    loads.append(find_load(curr_grid))

candidates = []

for i in range(len(loads)):
    max_seq_len = (len(loads) - i) // 2
    for seq_len in range(2, max_seq_len):
        left = loads[i : i + seq_len]
        right = loads[i + seq_len : i + seq_len * 2]
        assert len(left) == len(right)
        if left == right:
            candidates.append((seq_len, i))

seq_len, seq_start = min(candidates)

print(loads[((1000000000 - seq_start) % seq_len) + seq_start - 1])
