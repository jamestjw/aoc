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
                cave[curr_sand] = "."
                num_sand += 1
                if curr_sand == source:
                    done = True
                break

    print(num_sand)
