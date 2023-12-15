import sys
import re
from collections import defaultdict

file = open(sys.argv[1]).read()
instrs = file.split(",")


def hash(s: str) -> int:
    score = 0
    for c in s:
        score += ord(c)
        score *= 17
        score %= 256
    return score


print(sum(list(map(hash, instrs))))

boxes = defaultdict(lambda: list())

for instr in instrs:
    box, op, focal = re.match("(.*)(-|=)(.*)?", instr).groups()

    box_index = hash(box)
    slots = boxes[box_index]

    indices = [i for i, (name, _) in enumerate(slots) if name == box]
    match (op, focal):
        case ("-", ""):
            if len(indices) == 1:
                slots.pop(indices[0])

        case ("=", focal) if focal.isnumeric():
            focalVal = int(focal)
            if len(indices) == 1:
                slots[indices[0]] = (box, focalVal)
            else:
                slots.append((box, focalVal))

        case _:
            raise Exception


print(
    sum(
        (bn + 1) * (i + 1) * f
        for bn, slots in boxes.items()
        for i, (_, f) in enumerate(slots)
    )
)
