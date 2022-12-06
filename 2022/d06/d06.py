"""
This file contains a code attempt for advent of code day 6
"""


import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    my_tests = open(f"d06_tests_input.txt", "r", encoding="utf-8").read().strip()

    P1_LEN = 4
    P2_LEN = 14

    part1 = next(i+P1_LEN for i in range(len(my_tests)) if len(set(my_tests[i:i+P1_LEN])) == P1_LEN)
    part2 = next(i+P2_LEN for i in range(part1, len(my_tests)) if len(set(my_tests[i:i+P2_LEN])) == P2_LEN)

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
