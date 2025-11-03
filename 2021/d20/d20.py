import sys
import math
import copy
from functools import reduce
from itertools import permutations

algo, grid_text = open(sys.argv[1]).read().split("\n\n")
grid = list(map(list, grid_text.splitlines()))


def print_grid_coords(grid_coords):
    min_x = min(x for x, y in grid_coords) - 1
    max_x = max(x for x, y in grid_coords) + 2
    min_y = min(y for x, y in grid_coords) - 1
    max_y = max(y for x, y in grid_coords) + 2

    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            if (x, y) in grid_coords:
                to_print = "#"
            else:
                to_print = "."
            print(to_print, end="")
        print("")


def enhance(grid_coords):

    min_x = min(x for x, y in grid_coords)
    max_x = max(x for x, y in grid_coords)
    min_y = min(y for x, y in grid_coords)
    max_y = max(y for x, y in grid_coords)

    # Create new picture

    start_x = min_x - 3
    start_y = min_y - 3
    end_x = max_x + 3
    end_y = max_y + 3

    new_grid_coords = set()

    # needs to be inclusive, so  + 1
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            bits = ""
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (x + dx, y + dy) in grid_coords:
                        bits += "1"
                    else:
                        bits += "0"
            if algo[int(bits, 2)] == "#":
                new_grid_coords |= {(x, y)}

    return new_grid_coords

grid_coords = set()

for i, row in enumerate(grid):
    for j, e in enumerate(row):
        if e == "#":
            grid_coords |= {(i, j)}

# print_grid_coords(grid_coords)

curr_grid_coords = grid_coords.copy()

for _ in range(2):
    curr_grid_coords = enhance(curr_grid_coords)

    
    # print_grid_coords(curr_grid_coords)

    print(len(curr_grid_coords))

# 5255 too high
# print(len(curr_grid_coords))
