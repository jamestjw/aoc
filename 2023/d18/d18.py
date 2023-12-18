import sys

file = open(sys.argv[1]).read().split("\n")
rows = [d.split() for d in file]


def triangle(l):
    return (
        abs(sum((x1 * y2) - (y1 * x2) for (x1, y1), (x2, y2) in zip(l, l[1:] + [l[0]])))
        // 2
    )


def turn_left(coords):
    match coords:
        case (1, 0):
            return (0, 1)
        case (-1, 0):
            return (0, -1)
        case (0, 1):
            return (-1, 0)
        case (0, -1):
            return (1, 0)
        case _:
            raise Exception


def turn_right(coords):
    match coords:
        case (1, 0):
            return (0, -1)
        case (-1, 0):
            return (0, 1)
        case (0, 1):
            return (1, 0)
        case (0, -1):
            return (-1, 0)
        case _:
            raise Exception


def half(offset):
    return offset[0] / 2, offset[1] / 2


def reverse(offset):
    return -offset[0], -offset[1]


def move(here, offset):
    return here[0] + offset[0], here[1] + offset[1]


def do_area(directions, counts):
    def get_dir(d: str):
        return [(0, 1), (0, -1), (1, 0), (-1, 0)]["RLDU".index(d)]

    curr = (0, 0)
    corners = []
    last_direction = get_dir(directions[-1])

    for direction, count in zip(directions, counts):
        offset = get_dir(direction)
        end = curr[0] + int(count) * offset[0], curr[1] + int(count) * offset[1]

        if turn_right(last_direction) == offset:
            left_offset = half(reverse(offset))
            up_offset = half(last_direction)

            corner = move(move(curr, left_offset), up_offset)
            corners.append(corner)

        elif turn_left(last_direction) == offset:
            left_offset = half(offset)
            down_offset = half(reverse(last_direction))

            corner = move(move(curr, left_offset), down_offset)
            corners.append(corner)

        last_direction = offset
        curr = end

    return triangle(corners)


print(do_area([d for d, _, _ in rows], [c for _, c, _ in rows]))

alt_dirs = []
alt_counts = []

for _, _, code in rows:
    alt_dirs.append("RDLU"[["0", "1", "2", "3"].index(code[-2])])
    alt_counts.append(int(code[2:-2], 16))

print(do_area(alt_dirs, alt_counts))
