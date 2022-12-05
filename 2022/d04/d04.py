"""
This file contains a code attempt for advent of code day 4
"""


import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    my_tests = []
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]
    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        content = file.readlines()
        for line in content:
            my_tests.append(line.rstrip("\n"))

    my_tests = [x.split(",") for x in my_tests]
    my_tests = [(x1.split("-"), x2.split("-")) for x1, x2 in my_tests]
    my_tests = [(list(map(int, x1)), list(map(int, x2))) for x1, x2 in my_tests]
    my_tests = [sorted(x, key=lambda x: (x[0], -1 * x[1])) for x in my_tests]
    p1 = sum([1 if x >= y else 0 for (_, x), (_, y) in my_tests])
    p2 = sum([1 if x >= y else 0 for (_, x), (y, _) in my_tests])

    print(f"Answer part1 : {p1}")
    print(f"Answer part2 : {p2}")
