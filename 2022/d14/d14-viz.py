"""
This file contains a code attempt for advent of code day 14
"""

from collections import defaultdict


def string2coord(s):
    x, y = s.split(",")
    return int(x) + int(y) * 1j


if __name__ == "__main__":
    # lines = open(f"smol.txt", "r", encoding="utf-8").read().splitlines()
    lines = open(f"input.txt", "r", encoding="utf-8").read().splitlines()
    lines = [list(map(string2coord, x.split(" -> "))) for x in lines]

    cave = defaultdict(lambda: None)

    for line in lines:
        for start, end in zip(line[:-1], line[1:]):
            curr = start
            offset = (end - start) / abs(end - start)
            for _ in range(int(abs(end - start) + 1)):
                cave[curr] = "#"
                curr += offset

    max_height = max(int(coord.imag) for coord in cave.keys())
    ceiling = max_height + 2

    source = 500
    sand_directions = [1j, -1 + 1j, 1 + 1j]
    num_sand = 0

    done = False
    while not done:
        curr_sand = source
        while True:
            moved = False
            for offset in sand_directions:
                if (
                    not cave[curr_sand + offset]
                    and (curr_sand + offset).imag != ceiling
                ):
                    curr_sand += offset
                    moved = True
            if not moved:
                cave[curr_sand] = "o"
                num_sand += 1
                if curr_sand == source:
                    done = True
                break

    xs = [int(coord.real) for coord in cave.keys()]
    ys = [int(coord.imag) for coord in cave.keys()]
    max_x, max_y, min_x, min_y = max(xs), max(ys), min(xs), min(ys)
    grid = [["." for _ in range(1 + max_x - min_x)] for _ in range(1 + max_y - min_y)]
    for k, v in cave.items():
        if v: grid[int(k.imag-min_y)][int(k.real-min_x)] = v
    print('\n'.join([''.join(row) for row in grid]), file=open('viz.txt', 'w'))
