import sys
from itertools import product
from typing import Tuple

DIRECTIONS: list[Tuple[int, int]] = [
    tuple(d) for d in product([1, 0, -1], repeat=2) if d != (0, 0)
] # type: ignore

file = open(sys.argv[1]).read()

grid = [[c for c in line] for line in file.splitlines()]

num_rows, num_cols = len(grid), len(grid[0])


def get_from_offset(coords, direction):
    i, j = coords
    di, dj = direction
    new_i, new_j = i + di, j + dj
    return (
        grid[new_i][new_j] if 0 <= new_i < num_rows and 0 <= new_j < num_cols else None
    )


def find_seq(coords: Tuple[int, int], direction: Tuple[int, int], chars: list[str]):
    match chars:
        case []:
            return True
        case [targ, *rest] if targ == get_from_offset(coords, direction):
            return find_seq(
                (coords[0] + direction[0], coords[1] + direction[1]), direction, rest
            )
        case _:
            return False


def part1():
    total = 0
    for i in range(num_rows):
        for j in range(num_cols):
            curr = grid[i][j]
            if curr == "X":
                for d in DIRECTIONS:
                    total += int(find_seq((i, j), d, ["M", "A", "S"]))
    return total


def cyclic(elems):
    for i in range(len(elems)):
        yield elems[i:] + elems[:i]


cycle_directions = [(1, -1), (1, 1), (-1, 1), (-1, -1)]


def part2():
    total = 0
    for i in range(num_rows):
        for j in range(num_cols):
            curr = grid[i][j]
            if curr == "A":
                if any(
                    all(
                        get_from_offset((i, j), d) == targ
                        for d, targ in zip(cycle_directions, targs)
                    )
                    for targs in cyclic("MMSS")
                ):
                    total += 1
    return total


print(part1())
print(part2())
