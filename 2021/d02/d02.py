inp = [x.split() for x in open(0).read().splitlines()]

start = (0, 0)

for d, c in inp:
    if d == "forward":
        m = (1, 0)
    elif d == "down":
        m = (0, 1)
    elif d == "up":
        m = (0, -1)
    elif d == "right":
        m = (-1, 0)
    i, j = m
    c = int(c)
    start = (start[0] + i * c, start[1] + j * c)

print(start)
