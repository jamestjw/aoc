"""
This file contains a code attempt for advent of code day 5
"""


import os
import copy


def move(cfg, num, source, dest):
    for i in range(num): cfg[dest].append(cfg[source].pop())

def move2(cfg, num, source, dest):
    popped = [cfg[source].pop() for _ in range(num)][::-1]
    for e in popped: cfg[dest].append(e)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    day = __file__.split("\\", maxsplit=-1)[-1][:-3]
    my_tests = open(f"{day}_tests_input.txt", "r", encoding="utf-8").read().splitlines()

    layout_raw = open("layout.txt").read().splitlines()
    # take every 4th elem (starting from index 1)
    layout = [list(l[1::4]) for l in layout_raw]
    transposed = [list(x) for x in zip(*layout)]
    # pop empty string and reverse
    transposed = [list(filter(lambda x: x != " ", x))[::-1] for x in transposed]

    p1_config = copy.deepcopy(transposed)
    p2_config = copy.deepcopy(transposed)

    # move 3 from 4 to 3
    # i.e. get index 1, 3 & 5
    # numcrate, source, dest
    movements = [list(map(x.split(" ").__getitem__, [1, 3, 5])) for x in my_tests]
    movements = [list(map(int, x)) for x in movements]

    for num, source, dest in movements:
        move(p1_config, num, source - 1, dest - 1)
        move2(p2_config, num, source - 1, dest - 1)

    p1 = "".join([x.pop() for x in p1_config])
    p2 = "".join([x.pop() for x in p2_config])

    print(f"Answer part1 : {p1}")
    print(f"Answer part2 : {p2}")
