import sys

file = open(sys.argv[1]).read().split("\n")
rows = [d.split() for d in file]


def triangle(l):
    return int(
        abs(sum((x1 * y2) - (y1 * x2) for (x1, y1), (x2, y2) in zip(l, l[1:] + [l[0]])))
        / 2
    )


def do_area(directions, counts):
    def get_dir(d: str):
        return [1j, -1j, 1, -1]["RLDU".index(d)]

    curr = 0
    corners = []
    last_direction = get_dir(directions[-1])

    for direction, count in zip(directions, counts):
        offset = get_dir(direction)
        corners.append(curr + (last_direction + offset) * 0.5j)
        last_direction = offset
        curr = curr + offset * int(count)

    return triangle([(c.real, c.imag) for c in corners])


eq_dict = {"0": "R", "1": "D", "2": "L", "3": "U"}
print(do_area(*zip(*[(d, int(c)) for d, c, _ in rows])))
print(do_area(*zip(*[(eq_dict[d[-2]], int(d[2:-2], 16)) for _, _, d in rows])))
