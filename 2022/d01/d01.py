"""
This file contains a code attempt for advent of code day 1
"""


import os
from itertools import groupby

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    my_tests = []
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]
    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        content = file.readlines()
        for line in content:
            my_tests.append(line.rstrip("\n"))

    data = [list(group) for k, group in groupby(my_tests, lambda x: x == "") if not k]
    amounts = [sum(map(int, x_)) for x_ in data]
    part1 = max(amounts)
    part2 = sum(sorted(amounts, reverse=True)[:3])

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
