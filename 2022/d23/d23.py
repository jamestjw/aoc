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
    # my_tests = open("medium.txt", "r", encoding="utf-8").read().splitlines()
    my_tests = open("input.txt", "r", encoding="utf-8").read().splitlines()
    input = np.array(list(map(list, my_tests)))
    elves = list(map(tuple, np.argwhere(input.T == "#").tolist()))
    pos = defaultdict(lambda: False, {elf: True for elf in elves})

    for _ in range(10):
        proposals = {}
        for elf in elves:
            if alone(elf, pos):
                continue
            for offset, obstacles in dirs:
                if not any(pos[(elf[0] + x, elf[1] + y)] for (x, y) in obstacles):
                    proposals[elf] = (elf[0] + offset[0], elf[1] + offset[1])
                    break
        if not len(proposals) > 0:
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

    max_x = max(coord[0] for coord in elves)
    max_y = max(coord[1] for coord in elves)
    min_x = min(coord[0] for coord in elves)
    min_y = min(coord[1] for coord in elves)

    part1 = (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)
    part2 = 0

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
