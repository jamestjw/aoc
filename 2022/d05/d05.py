"""
This file contains a code attempt for advent of code day 5
"""


import os
import copy


def move(cfg, num, source, dest):
    for _ in range(num):
        cfg[dest].append(cfg[source].pop())


def move2(cfg, num, source, dest):
    popped = [cfg[source].pop() for _ in range(num)][::-1]
    for e in popped:
        cfg[dest].append(e)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    my_tests = open("input.txt", "r", encoding="utf-8").read()

    layout_raw, movements = (
        open("input.txt", "r", encoding="utf-8").read().split("\n\n")
    )

    # take every 4th elem (starting from index 1)
    layout = [list(l[1::4]) for l in layout_raw.split("\n")]
    transposed = [list(filter(lambda x: x != " ", list(x)))[::-1] for x in zip(*layout)]

    p1_config = copy.deepcopy(transposed)
    p2_config = copy.deepcopy(transposed)

    # move 3 from 4 to 3
    # i.e. get index 1, 3 & 5
    # numcrate, source, dest
    movements = [
        map(int, (s[1], s[3], s[5]))
        for x in movements.split("\n")
        if (s := x.split(" "))
    ]

    for num, source, dest in movements:
        move(p1_config, num, source - 1, dest - 1)
        move2(p2_config, num, source - 1, dest - 1)

    p1 = "".join([x.pop() for x in p1_config])
    p2 = "".join([x.pop() for x in p2_config])

    print(f"Answer part1 : {p1}")
    print(f"Answer part2 : {p2}")
