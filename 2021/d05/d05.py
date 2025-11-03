"""
This file contains a code attempt for advent of code day 6
"""


import os


def generate_line(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    m = int((y2 - y1) / (x2 - x1))

    def f(x):
        return m * (x - x1) + y1

    return f


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

    grid = [[0] * (max_y + 1) for _ in range(max_x + 1)]
    grid_diagonal = [[0] * (max_y + 1) for _ in range(max_x + 1)]

    for (x1, y1), (x2, y2) in input_coords:
        if abs(y2 - y1) == abs(x2 - x1):
            line = generate_line((x1, y1), (x2, y2))
            min_x, max_x = sorted([x1, x2])
            for x in range(min_x, max_x + 1):
                grid_diagonal[x][line(x)] += 1
        elif x1 == x2:
            y1, y2 = sorted([y1, y2])
            for y in range(y1, y2 + 1):
                grid[x1][y] += 1
        elif y1 == y2:
            x1, x2 = sorted([x1, x2])
            for x in range(x1, x2 + 1):
                grid[x][y1] += 1

    grid_straight_diagonal = [
        [i1 + j1 for i1, j1 in zip(i, j)] for i, j in zip(grid, grid_diagonal)
    ]

    part1 = sum(map(lambda x: sum(1 for x_ in x if x_ >= 2), grid))
    part2 = sum(map(lambda x: sum(1 for x_ in x if x_ >= 2), grid_straight_diagonal))

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
