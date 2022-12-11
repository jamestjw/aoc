"""
This file contains a code attempt for advent of code day 11
"""
import re
from functools import reduce
from copy import deepcopy

monkeys = open(0).read().split("\n\n")

monkey_dict = dict()

for monkey in monkeys:
    res = re.search(
        "Monkey (\d):\n  Starting items: (.*)\n  Operation: new = (.*)\n  Test: divisible by (\d+)\n    If true: throw to monkey (\d)\n    If false: throw to monkey (\d)",
        monkey,
    ).groups()
    monkey_dict[res[0]] = {
        "items": list(map(int, res[1].split(","))),
        "new": res[2],
        "div": int(res[3]),
        "true": res[4],
        "false": res[5],
        "examined": 0,
    }

def run(monkey_dict, iterations, stress_reducer):
    for _ in range(iterations):
        for monkey in monkey_dict.values():
            for old in monkey["items"]:
                monkey["examined"] += 1
                item = stress_reducer(eval(monkey["new"]))
                targ = "true" if item % monkey["div"] == 0 else "false"
                monkey_dict[monkey[targ]]["items"].append(item)
            monkey["items"] = []
    top2 = sorted([monkey["examined"] for monkey in monkey_dict.values()], reverse=True)[:2]

    print(f"Answer : {top2[0] * top2[1]}")

common_multiple = reduce(lambda x, y: x * y, [monkey["div"] for monkey in monkey_dict.values()])

run(deepcopy(monkey_dict), 20, lambda x: x // 3)
run(deepcopy(monkey_dict), 10000, lambda x: x % common_multiple)
