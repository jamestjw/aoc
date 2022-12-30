"""
This file contains a code attempt for advent of code day 23
"""


import numpy as np
from collections import defaultdict, Counter

dirs = [
    # north
    ((0, -1), [(0, -1), (1, -1), (-1, -1)]),
    # south
    ((0, 1), [(0, 1), (1, 1), (-1, 1)]),
    # west
    ((-1, 0), [(-1, 0), (-1, -1), (-1, 1)]),
    # east
    ((1, 0), [(1, 0), (1, -1), (1, 1)]),
]


def alone(coord, d):
    return not any(
        abs(x) + abs(y) > 0 and d[(coord[0] + x, coord[1] + y)]
        for x in [0, 1, -1]
        for y in [0, 1, -1]
    )


if __name__ == "__main__":
    # my_tests = open("smol.txt", "r", encoding="utf-8").read().splitlines()
    my_tests = open("medium.txt", "r", encoding="utf-8").read().splitlines()
    my_tests = open("input.txt", "r", encoding="utf-8").read().splitlines()
    input = np.array(list(map(list, my_tests)))
    elves = list(map(tuple, np.argwhere(input.T == "#").tolist()))
    pos = defaultdict(lambda: False, {elf: True for elf in elves})

    i = 0
    while True:
        i+=1
        proposals = {}
        for elf in elves:
            if alone(elf, pos):
                continue
            for offset, obstacles in dirs:
                if not any(pos[(elf[0] + x, elf[1] + y)] for (x, y) in obstacles):
                    proposals[elf] = (elf[0] + offset[0], elf[1] + offset[1])
                    break
        if not len(proposals) > 0:
            print(i)
            break
        counts = Counter(list(proposals.values()))
        new_pos = {}

        for elf in elves:
            if elf not in proposals or counts[proposals[elf]] > 1:
                new_pos[elf] = True
            else:
                new_pos[proposals[elf]] = True

        pos = defaultdict(lambda: False, new_pos)
        elves = list(pos.keys())

        dirs = dirs[1:] + dirs[:1]
