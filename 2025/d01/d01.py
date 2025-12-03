inp = open(0).read().strip().splitlines()
inp = [(l[0], int(l[1:])) for l in inp]
curr = 50
pt1_count = pt2_count = 0
for dir, n in inp:
    match dir:
        case "L":
            op = lambda x, y: x - y
        case "R":
            op = lambda x, y: x + y
        case _:
            raise Exception

    for _ in range(n):
        curr = op(curr, 1)

        if curr < 0:
            curr = 99
        elif curr > 99:
            curr = 0

        if curr == 0:
            pt2_count += 1

    if curr == 0:
        pt1_count += 1


print(pt1_count, pt2_count)
