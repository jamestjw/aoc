import sys

from functools import reduce
from itertools import cycle, permutations
import re

_, p1, _, p2 = re.findall(r"\d+", open(sys.argv[1]).read())

pool = cycle(range(1, 101))
rolled = 0
def det_dice():
    global rolled
    rolled += 1
    return next(pool)

p1_score, p2_score = 0 , 0
p1_pos, p2_pos = int(p1) - 1, int(p2) - 1

while True:
    p1_offset = det_dice() + det_dice() + det_dice()
    p1_pos = (p1_pos + p1_offset) % 10
    p1_score += p1_pos + 1

    if p1_score >= 1000: break

    p2_offset = det_dice() + det_dice() + det_dice()

    p2_pos = (p2_pos + p2_offset) % 10
    p2_score += p2_pos + 1
    
    

    if p2_score >= 1000: break

print(p1_score, p2_score, p1_pos, p2_pos, rolled)
print(min(p1_score, p2_score) * rolled)
