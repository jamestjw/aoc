import re
from functools import reduce
from z3 import *

inp_lines = open("input.txt", "r", encoding="utf-8").read().split("\n")
# inp_lines = open("smol.txt", "r", encoding="utf-8").read().split("\n")

times = list(map(int, re.findall(r"\d+", inp_lines[0])))
distances = list(map(int, re.findall(r"\d+", inp_lines[1])))


def do1(time, distance, is_max=True):
    o = Optimize()
    charge, run = z3.Int("x"), z3.Int("y")

    o.add(charge + run == time)
    o.add(Product(run, charge) > distance)
    if is_max:
        o.maximize(charge)
    else:
        o.minimize(charge)

    if o.check() == sat:
        return o.model()[charge].as_long()
    else:
        raise Exception


print(
    reduce(
        lambda x, y: x * y,
        [
            do1(time, distance, True) - do1(time, distance, False) + 1
            for time, distance in zip(times, distances)
        ],
        1,
    )
)

time = int("".join(re.findall(r"\d+", inp_lines[0])))
distance = int("".join(re.findall(r"\d+", inp_lines[1])))

max_time = do1(time, distance, True)
min_time = do1(time, distance, False)
print(max_time - min_time + 1)
