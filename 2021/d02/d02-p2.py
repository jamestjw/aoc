inp = [x.split() for x in open(0).read().splitlines()]

start = (0, 0)
aim = 0

for d, c in inp:
    c = int(c)
    aim_offset = 0
    m = (0, 0)
    if d == "forward":
        m = (c, aim * c)
    elif d == "down":
        aim_offset = c
    elif d == "up":
        aim_offset = -1 * c
    i, j = m
    aim += aim_offset
    start = (start[0] + i, start[1] + j)

print(start[0] * start[1])
