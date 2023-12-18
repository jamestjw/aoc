import sys

file = open(sys.argv[1]).read().split("\n")
rows = [d.split() for d in file]


def triangle(l):
    return (
        abs(sum((x1 * y2) - (y1 * x2) for (x1, y1), (x2, y2) in zip(l, l[1:] + [l[0]])))
        / 2
    )


def do_area(directions, counts):
    def get_dir(d: str):
        return [(0, 1), (0, -1), (1, 0), (-1, 0)]["RLDU".index(d)]

    curr = (0, 0)
    verts = []
    corners = []
    last_direction = get_dir(directions[-1])

    for direction, count in zip(directions, counts):
        offset = get_dir(direction)
        end = curr[0] + count * offset[0], curr[1] + count * offset[1]

        verts.append(curr)
        curr = end

    # Points on the boundary (perimeter)
    boundary_count = sum(counts)

    # Area within polygon
    area = triangle(verts)
    # Points within polygon using Pick's theorem
    interior_count = area - (boundary_count // 2) + 1

    return int(interior_count + boundary_count)


print(do_area([d for d, _, _ in rows], [int(c) for _, c, _ in rows]))
print(
    do_area(
        ["RDLU"[["0", "1", "2", "3"].index(d[-2])] for _, _, d in rows],
        [int(d[2:-2], 16) for _, _, d in rows],
    )
)
