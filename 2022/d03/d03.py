"""
This file contains a code attempt for advent of code day 3
"""


import os


def letter_to_score(s) -> int:
    return 1 + ord(s) - ord("a") if ord(s) >= 97 else 27 + (ord(s) - ord("A"))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    my_tests = []
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]
    with open(f"{day}_tests_input.txt", "r", encoding="utf-8") as file:
        content = file.readlines()
        for line in content:
            my_tests.append(line.rstrip("\n"))

    my_input = []
    day = __file__.split("\\", maxsplit=-1)[-1][:-3]
    with open(f"{day}.txt", "r", encoding="utf-8") as file:
        content = file.readlines()
        for line in content:
            my_input.append(line.rstrip("\n"))

    my_tests_2 = [
        (s[slice(0, len(s) // 2)], s[slice(len(s) // 2, len(s))]) for s in my_tests
    ]
    scores = [letter_to_score( (set(s1) & set(s2)).pop()) for s1, s2 in my_tests_2]
    p1 = sum(scores)

    list_of_groups = list(zip(*(iter(my_tests),) * 3))
    common_letter = [set(s1) & set(s2) & set(s3) for s1, s2, s3 in list_of_groups]
    p2 = sum([letter_to_score(s.pop()) for s in common_letter])

    print(f"Answer part1 : {p1}")
    print(f"Answer part2 : {p2}")
