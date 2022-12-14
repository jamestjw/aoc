"""
This file contains a code attempt for advent of code day 14
"""


import os
from collections import defaultdict
import numpy as np


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
            while True:
                cave[curr] = "#"
                if end == curr:
                    break
                curr += offset

    max_height = max(int(coord.imag) for coord in cave.keys())
    source = 500
    sand_directions = [1j, -1 + 1j, 1 + 1j]
    num_sand = 0

    overflow = False
    while not overflow:
        curr_sand = source
        while True:
            moved = False
            for offset in sand_directions:
                if not cave[curr_sand + offset]:
                    curr_sand += offset
                    moved = True
                    if curr_sand.imag > max_height:
                        overflow = True
                    break
            if overflow:
                break
            if not moved:
                cave[curr_sand] = "."
                num_sand += 1
                break

    print(num_sand)
