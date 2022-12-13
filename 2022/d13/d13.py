"""
This file contains a code attempt for advent of code day 13
"""


import itertools
import numpy as np
from functools import cmp_to_key

def L(x):
    return x if type(x) is list else [x]

def compare(l1, l2):
    for e1, e2 in zip(l1, l2):
        if e1 != e2:
            if type(e1) is list or type(e2) is list:
                res = compare(L(e1), L(e2))
                if res != 0:
                    return res
            else:
                return np.sign(e2 - e1)
    return np.sign(len(l2) - len(l1))

if __name__ == "__main__":
    my_tests = open(f"input.txt", "r", encoding="utf-8").read().split("\n\n")
    # my_tests = open(f"smol.txt", "r", encoding="utf-8").read().split("\n\n")
    my_tests = list(map(lambda x: x.split(), my_tests))
    pairs = list(map(lambda x: [eval(x_) for x_ in x], my_tests))

    res1 = map(lambda x: compare(*x), pairs)
    part1 = sum([i + 1 for i, v in enumerate(res1) if v == 1])

    flattened = list(itertools.chain(*pairs)) + [[[2]], [[6]]]
    flattened.sort(key=cmp_to_key(compare), reverse=True)
    part2 = (flattened.index([[2]]) + 1) * (flattened.index([[6]]) + 1)

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
