"""
This file contains a code attempt for advent of code day 2
"""


import os

from enum import Enum


class RPS(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

wins_against = {
    RPS.ROCK: RPS.SCISSORS,
    RPS.PAPER: RPS.ROCK,
    RPS.SCISSORS: RPS.PAPER
}

loses_against = {v: k for k,v in wins_against.items()}

LOST_SCORE = 0
DRAW_SCORE = 3
WIN_SCORE = 6

def convert_p1(input: str) -> RPS:
    if input == "A":
        return RPS.ROCK
    elif input == "B":
        return RPS.PAPER
    elif input == "C":
        return RPS.SCISSORS
    else:
        raise Exception

def convert_p2(input: str) -> RPS:
    if input == "X":
        return RPS.ROCK
    elif input == "Y":
        return RPS.PAPER
    elif input == "Z":
        return RPS.SCISSORS
    else:
        raise Exception


def score_from_outcome(outcome: int):
    if outcome == 0:
        return DRAW_SCORE
    elif outcome > 0:
        return WIN_SCORE
    else:
        return LOST_SCORE


def outcome(p1: RPS, p2: RPS) -> int:
    if p1 == p2:
        return 0
    if p2 == wins_against[p1]: return 1
    else: return -1

def p2_from_outcome(p1: RPS, outcome: int) -> RPS:
    if outcome == 0:
        return p1
    elif outcome == 1:
        return loses_against[p1]
    else:
        return wins_against[p1]

def str_to_outcome(input: str) -> int:
    if input == "X":
        return -1
    elif input == "Y":
        return 0
    elif input == "Z":
        return 1
    else:
        raise Exception


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

    my_tests = [t.split(" ") for t in my_tests]

    hands = [(convert_p1(p1), convert_p2(p2)) for p1, p2 in my_tests]

    scores = [p2.value + score_from_outcome(outcome(p2, p1)) for p1, p2 in hands]

    p1 = sum(scores)

    p2 = sum([
        p2_from_outcome(convert_p1(p1), str_to_outcome(o)).value
        + score_from_outcome(str_to_outcome(o))
        for p1, o in my_tests
    ])

    print(f"Answer part1 : {p1}")
    print(f"Answer part2 : {p2}")
