"""
This file contains a code attempt for advent of code day 22
"""


import re
import itertools
import numpy as np

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
score = [0, 1, 2, 3]


def turn(o, dir):
    offset = 1 if dir == "R" else -1
    return directions[(directions.index(o) + offset) % 4]


if __name__ == "__main__":
    grid, commands = open("smol.txt", "r", encoding="utf-8").read().split("\n\n")
    grid, commands = open("input.txt", "r", encoding="utf-8").read().split("\n\n")
    commands = [
        x
        for x in itertools.chain(
            *itertools.zip_longest(
                list(map(int, re.findall("\d+", commands))),
                re.findall("[LR]", commands),
            )
        )
        if x is not None
    ]
    max_len = max(len(x) for x in grid.split("\n"))
    grid = np.array([list(row.ljust(max_len, " ")) for row in grid.split("\n")])

    x_len, y_len = len(grid[0]), len(grid)

    curr_offset = (1, 0)
    coords = tuple(np.argwhere(grid == ".")[0][::-1])

    def valid(x, y):
        return 0 <= x < x_len and 0 <= y < y_len

    for command in commands:
        print(command)
        match command:
            case int(x):
                for _ in range(x):
                    new_coords = (
                        coords[0] + curr_offset[0],
                        coords[1] + curr_offset[1],
                    )
                    if (
                        not valid(*new_coords)
                        or grid[new_coords[1], new_coords[0]] == " "
                    ):
                        # wrap around
                        match curr_offset:
                            case (1, 0):
                                y = coords[1]
                                new_coords = (np.argwhere(grid[y] != " ")[0][0], y)
                            case (0, 1):
                                x = coords[0]
                                new_coords = (x, np.argwhere(grid[:, x] != " ")[0][0])
                            case (-1, 0):
                                y = coords[1]
                                new_coords = (np.argwhere(grid[y] != " ")[-1][0], y)
                            case (0, -1):
                                x = coords[0]
                                new_coords = (x, np.argwhere(grid[:, x] != " ")[-1][0])

                    if grid[new_coords[1], new_coords[0]] == "#":
                        break  # stop moving
                    coords = new_coords
                    print(coords)
            case str(dir):
                curr_offset = turn(curr_offset, dir)
            case _:
                raise Exception

    final_row, final_column = coords[1] + 1, coords[0] + 1

    part1 = 1000 * final_row + 4 * final_column + score[directions.index(curr_offset)]
    part2 = 0

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
