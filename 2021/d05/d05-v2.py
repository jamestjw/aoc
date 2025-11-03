"""
This file contains a code attempt for advent of code day 6
"""


import os
import itertools


def generate_iterator(x1, x2):
    if x1 == x2:
        return itertools.cycle([x1])
    step = 1 if x2 > x1 else -1
    return range(x1, x2 + step, step)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    my_tests = open(0).read().splitlines()
    input_coords_flat = [
        list(map(int, pair))
        for x in my_tests
        if (pair := x.replace("->", ",").split(","))
    ]
    max_x = max([num for sl in input_coords_flat for num in sl][0::2])
    max_y = max([num for sl in input_coords_flat for num in sl][1::2])
    input_coords = [((x1, y1), (x2, y2)) for x1, y1, x2, y2 in input_coords_flat]

    grid_diagonal = [[0] * (max_y + 1) for _ in range(max_x + 1)]

    for (x1, y1), (x2, y2) in input_coords:
        if abs(y2 - y1) == abs(x2 - x1) or x1 == x2 or y1 == y2:
            for x, y in zip(generate_iterator(x1, x2), generate_iterator(y1, y2)):
                grid_diagonal[x][y] += 1

    part2 = sum(map(lambda x: sum(1 for x_ in x if x_ >= 2), grid_diagonal))

    print(f"Answer part2 : {part2}")
