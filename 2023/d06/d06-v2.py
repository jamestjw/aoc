import re
from functools import reduce
import math

inp_lines = open("input.txt", "r", encoding="utf-8").read().split("\n")
# inp_lines = open("smol.txt", "r", encoding="utf-8").read().split("\n")

times = list(map(int, re.findall(r"\d+", inp_lines[0])))
distances = list(map(int, re.findall(r"\d+", inp_lines[1])))


## Solve charge + run = time
## and charge * run > distance
## We just need to find the zeroes of (let x = charge):
## -(x - time/2)**2 - distance + time**2/4 = 0
def do1(time, distance):
    min_time = math.ceil(0.5 * time - math.sqrt(-distance + (time**2) / 4))
    max_time = int(0.5 * time + math.sqrt(-distance + (time**2) / 4))
    return min_time, max_time


print(
    reduce(
        lambda x, y: x * y,
        [
            e[1] - e[0] + 1
            for time, distance in zip(times, distances)
            if (e := do1(time, distance))
        ],
        1,
    )
)
time = int("".join(re.findall(r"\d+", inp_lines[0])))
distance = int("".join(re.findall(r"\d+", inp_lines[1])))
min_time, max_time = do1(time, distance)
print(max_time - min_time + 1)
