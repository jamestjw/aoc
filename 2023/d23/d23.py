import sys
from queue import PriorityQueue
from collections import defaultdict


grid = open(sys.argv[1]).read().strip().split("\n")

num_rows = len(grid)
num_cols = len(grid[0])

start = [(0, i) for i, e in enumerate(grid[0]) if e == "."][0]
end = [(num_rows - 1, i) for i, e in enumerate(grid[-1]) if e == "."][0]


def get_adj(coords, restriction) -> list:
    i, j = coords
    res = []
    for i_offset, j_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        # Check if there is a restriction, in which case the direction
        # must match it

        if restriction is not None and (i_offset, j_offset) != restriction:
            continue
        new_i = i + i_offset
        new_j = j + j_offset
        if (
            0 <= new_i < num_rows
            and 0 <= new_j < num_cols
            and grid[new_i][new_j] != "#"
        ):
            res.append((i + i_offset, j + j_offset))
    return res


def get_next_dirs(coords, prev_dir, restriction) -> list:
    i, j = coords
    prev_dir_rev = (-prev_dir[0], -prev_dir[1])
    res = []
    for i_offset, j_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        # Check if there is a restriction, in which case the direction
        # must match it

        if (i_offset, j_offset) == prev_dir_rev:
            continue

        if restriction is not None and (i_offset, j_offset) != restriction:
            continue
        new_i = i + i_offset
        new_j = j + j_offset
        if (
            0 <= new_i < num_rows
            and 0 <= new_j < num_cols
            and grid[new_i][new_j] != "#"
        ):
            res.append((i_offset, j_offset))
    return res


## NOTE: Commented code works for part 1 but is ugly

# ## Max distance from the end
# dist = defaultdict(lambda: 0)

# Q = PriorityQueue()
# # Dist, Coords, Path
# Q.put((0, end, set()))

# while not Q.empty():
# dist_to_end, next_coords, path = Q.get_nowait()

# i, j = next_coords

# restriction = None

# match grid[i][j]:
# case "^":
# restriction = (1, 0)
# case "v":
# restriction = (-1, 0)
# case "<":
# restriction = (0, 1)
# case ">":
# restriction = (0, -1)

# adjacents = get_adj(next_coords, restriction)

# for c in adjacents:
# alt = dist_to_end - 1
# path_set = path | {next_coords}
# if c in path_set:
# continue

# dist_key = (c, tuple(path_set))
# if alt < dist[dist_key]:
# dist[dist_key] = alt
# Q.put_nowait((alt, c, path_set))

# res = []
# for (c, path), v in dist.items():
# if c == start:
# res.append((path, v))

# path, v = sorted(res, key=lambda x: x[1])[0]

# print("Path is ", path, "dist: ", v)
# for i in range(num_rows):
# for j in range(num_cols):
# if (i, j) in set(path):
# print("X", end="")
# else:
# print(grid[i][j], end="")
# print("")


def make_adjacency_from_paths(paths):
    adjacency = []

    for path in paths:
        start = path[0]
        dest = path[-1]
        adjacency.append((start, dest, len(path) - 1))

    return adjacency


# Adjacency (Src, Dest, Cost)
#   - Tuple[Tuple[int, int], Tuple[int, int], int]
def longest_path(adjacency, start, dest):
    # tuple of coords, direction, and repeat count
    adjacency_dict = defaultdict(lambda: dict())

    for s, d, cost in adjacency:
        # adjacency_dict[d][s] = cost
        adjacency_dict[s][d] = cost

    solutions = []
    Q = [([start], 0)]

    while len(Q) != 0:
        path, curr_cost = Q.pop()
        curr = path[-1]
        if curr == dest:
            solutions.append((path, curr_cost))
        else:
            for n, cost in adjacency_dict[curr].items():
                if n not in path:
                    Q.append((path + [n], curr_cost + cost))

    return solutions


def make_adjacency(grid, start, with_restriction=False):
    paths = []

    assert grid[start[0] + 1][start[1] + 0] != "#"
    worklist = [([start], (1, 0))]
    visited = []

    while worklist:
        path, direction = worklist.pop()
        curr = path[-1]

        while True:
            if curr in visited:
                if len(path) > 1:
                    ## Don't include already visited square
                    paths.append(path)
                break

            restriction = None
            if with_restriction:
                match grid[curr[0]][curr[1]]:
                    case "^":
                        restriction = (-1, 0)
                    case "v":
                        restriction = (1, 0)
                    case "<":
                        restriction = (0, -1)
                    case ">":
                        restriction = (0, 1)
                    case _:
                        restriction = None

            adjs = get_next_dirs(curr, direction, restriction)

            match adjs:
                case []:
                    paths.append(path)
                    visited.append(curr)
                    break
                case [next_dir]:
                    direction = next_dir
                    curr = (curr[0] + next_dir[0], curr[1] + next_dir[1])
                    path.append(curr)

                case l:
                    for di, dj in l:
                        next_coords = (curr[0] + di, curr[1] + dj)
                        worklist.append(([curr, next_coords], (di, dj)))
                    paths.append(path)
                    visited.append(path[-1])
                    break

    adjacency = []

    for path in paths:
        start = path[0]
        dest = path[-1]
        adjacency.append((start, dest, len(path) - 1))
        if not with_restriction:
            adjacency.append((dest, start, len(path) - 1))

    return adjacency

# Part 1

## TODO: A bit iffy, works for input but not for smol
adjacency = make_adjacency(grid, start, True)
solutions = longest_path(adjacency, start, end)

print(sorted(solutions, key=lambda x: x[1])[-1][1])

# Part 2
adjacency = make_adjacency(grid, start, False)
solutions = longest_path(adjacency, start, end)

print(sorted(solutions, key=lambda x: x[1])[-1][1])
