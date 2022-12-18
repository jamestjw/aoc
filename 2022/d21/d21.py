"""
This file contains a code attempt for advent of code day 21
"""

import z3

if __name__ == "__main__":
    my_tests = open(f"smol.txt", "r", encoding="utf-8").read().splitlines()
    my_tests = open("input.txt", "r", encoding="utf-8").read().splitlines()
    monkeys = {s[0]: s[1].strip().split() for row in my_tests if (s := row.split(":"))}

    def evaluate(n):
        match monkeys[n]:
            case [d]:
                return int(d)
            case [l, op, r]:
                f = eval(f"lambda x,y: x {op} y")
                return int(f(evaluate(l), evaluate(r)))

    part1 = evaluate("root")

    s = z3.Solver()
    humn = z3.Int("humn")

    def do(n):
        match monkeys[n]:
            case [d]:
                return int(d) if n != "humn" else humn
            case [l, op, r]:
                if n == "root":
                    op = "=="
                f = eval(f"lambda x,y: x {op} y")
                return f(do(l), do(r))

    s.add(do("root"))

    assert s.check() == z3.sat
    model = s.model()

    part2 = model[humn].as_long()

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
