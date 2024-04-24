from collections import defaultdict
import sys
import re


## We want the lower end (wrt. to z-axis) to be on the left
def rearrange(brick):
    x1, y1, z1, x2, y2, z2 = brick
    if z1 <= z2:
        return brick
    else:
        return x2, y2, z2, x1, y1, z1


def overlap(start1, end1, start2, end2) -> bool:
    if start1 <= start2:
        return start2 <= end1
    else:
        return start1 <= end2


# Check for x-y intersection
def bricks_intersect(brick1, brick2) -> bool:
    x11, y11, _, x12, y12, _ = brick1
    x21, y21, _, x22, y22, _ = brick2
    return overlap(x11, x12, x21, x22) and overlap(y11, y12, y21, y22)


file = open(sys.argv[1]).read().strip().split("\n")
bricks = [rearrange(tuple(list(map(int, re.findall(r"\d+", line))))) for line in file]
bricks.sort(key=lambda x: x[2])

# Just check that the lower end is on the left
assert all(z1 <= z2 for _, _, z1, _, _, z2 in bricks)

# bricks sorted by z
positions = []

for brick in bricks:
    x1, y1, z1, x2, y2, z2 = brick
    blockers = [o for o in positions[::-1] if bricks_intersect(brick, o)]
    blockers.sort(key=lambda x: x[5])  # Get highest blocker
    if len(blockers) == 0:
        brick_z = 1
    else:
        brick_z = blockers[-1][5] + 1
    positions.append((x1, y1, brick_z, x2, y2, z2 - (z1 - brick_z)))

## Find supports
supports = defaultdict(lambda: set())
supported_by = defaultdict(lambda: set())

for i, brick1 in enumerate(positions):
    for brick2 in positions[i + 1 :]:
        if brick2[2] - brick1[5] == 1 and bricks_intersect(brick1, brick2):
            supports[brick1] |= {brick2}
            supported_by[brick2] |= {brick1}

safe_to_disintegrate = 0

for brick in positions:
    if all(len(supported_by[brick2]) > 1 for brick2 in supports[brick]):
        safe_to_disintegrate += 1

print(safe_to_disintegrate)

total = 0
for brick in positions:
    gone = {brick}
    candidates = list(supports[brick])
    while candidates:
        brick = candidates.pop()
        if len(supported_by[brick] - gone) == 0:
            total += 1
            gone |= {brick}
            candidates.extend(list(supports[brick]))

print(total)
