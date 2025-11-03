import re
import math
import sys

# x_start, x_end, y_start, y_end = tuple(
#     map(int, re.findall(r"-?\d+", open(sys.argv[1]).read()))
# )

lines = [re.findall(r"on|off|-?\d+", e) for e in open(sys.argv[1]).read().splitlines()]


def intervals_intersect(x, y):
    x_start, x_end = x
    y_start, y_end = y
    # return min(x_end, y_end) - max(x_start, y_start) >= 0
    return not (x_end < y_start or y_end < x_start)


def intersect_range(x, y):
    x_start, x_end = x
    y_start, y_end = y
    return max(x_start, y_start), min(x_end, y_end)


def cube_size(cube):
    (x1, x2), (y1, y2), (z1, z2) = cube
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1) * (abs(z2 - z1) + 1)
    # return (x2 - x1) * (y2 - y1 ) * (z2 - z1 )


pos = []

neg = []

for line in lines:
    mode = line[0]
    x1, x2, y1, y2, z1, z2 = list(map(int, line[1:]))

    if mode == "on":
        for (a1, a2), (b1, b2), (c1, c2) in pos:
            if (
                intervals_intersect((a1, a2), (x1, x2))
                and intervals_intersect((b1, b2), (y1, y2))
                and intervals_intersect((c1, c2), (z1, z2))
            ):
                res = (
                    intersect_range((a1, a2), (x1, x2)),
                    intersect_range((b1, b2), (y1, y2)),
                    intersect_range((c1, c2), (z1, z2)),
                )
                neg.append(res)
        pos.append(((x1, x2), (y1, y2), (z1, z2)))
    else:
        add_to_pos = []
        add_to_neg = []
        for (a1, a2), (b1, b2), (c1, c2) in pos:
            if (
                intervals_intersect((a1, a2), (x1, x2))
                and intervals_intersect((b1, b2), (y1, y2))
                and intervals_intersect((c1, c2), (z1, z2))
            ):
                res = (
                    intersect_range((a1, a2), (x1, x2)),
                    intersect_range((b1, b2), (y1, y2)),
                    intersect_range((c1, c2), (z1, z2)),
                )
                add_to_neg.append(res)

            # for (x1, x2), (y1, y2), (z1, z2) in add_to_neg:
        for (a1, a2), (b1, b2), (c1, c2) in neg:
            if (
                intervals_intersect((a1, a2), (x1, x2))
                and intervals_intersect((b1, b2), (y1, y2))
                and intervals_intersect((c1, c2), (z1, z2))
            ):
                res = (
                    intersect_range((a1, a2), (x1, x2)),
                    intersect_range((b1, b2), (y1, y2)),
                    intersect_range((c1, c2), (z1, z2)),
                )
                add_to_pos.append(res)
        pos.extend(add_to_pos)
        neg.extend(add_to_neg)
    # if mode == "on":
    #     add_to = pos
    #     remove_from = neg
    # else:
    #     add_to = neg
    #     remove_from = pos

    # for (a1, a2), (b1, b2), (c1, c2) in add_to:
    #     if (
    #         intervals_intersect((a1, a2), (x1, x2))
    #         and intervals_intersect((b1, b2), (y1, y2))
    #         and intervals_intersect((c1, c2), (z1, z2))
    #     ):
    #         res = (
    #             intersect_range((a1, a2), (x1, x2)),
    #             intersect_range((b1, b2), (y1, y2)),
    #             intersect_range((c1, c2), (z1, z2)),
    #         )
    #         remove_from.append(res)
    # add_to.append(((x1, x2), (y1, y2), (z1, z2)))

count = 0
for cube in pos:
    count += cube_size(cube)
for cube in neg:
    count -= cube_size(cube)

print(count)
