import itertools


coords = [tuple(map(int, l.split(","))) for l in open(0).read().splitlines()]

min_x  = min(x for x,y in coords)
max_x  = max(x for x,y in coords)
min_y  = min(y for x,y in coords)
max_y  = max(y for x,y in coords)

pairs = list(itertools.combinations(coords, 2))
sizes = [(abs(x1 - x2) + 1) * (1 + abs(y1 - y2)) for (x1, y1), (x2, y2) in pairs]
print(max(sizes))

walls = []

for (x1, y1), (x2, y2) in zip(coords, coords[1:] + [coords[0]]):
    if x1 == x2:
        y1, y2 = sorted([y1, y2])
        for y in range(y1, y2 + 1):
            walls.append((x1, y))
    elif y1 == y2:
        x1, x2 = sorted([x1, x2])
        for x in range(x1, x2 + 1):
            walls.append((x, y1))
    else:
        raise Exception

walls = set(walls)
filled = walls.copy()

x1, y1 = coords[0]
x2, y2 = coords[1]

if x1 == x2:
    start_y = min(y1, y2) + 1
elif y1 == y2:
    start_x = min(x1, x2) + 1
else:
    raise Exception

x2, y2 = coords[-1]

if x1 == x2:
    start_y = max(y1, y2) - 1
elif y1 == y2:
    start_x = max(x1, x2) - 1
else:
    raise Exception

q = [(start_x, start_y)]
print( q)

while q:
    x1, y1 = q.pop()
    # print(len(filled))
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        x2, y2 = x1 + dx, y1 + dy
        if (x2, y2) in filled:
            continue
        assert min_x <= x2 <= max_x
        assert min_y <= y2 <= max_y
        q.append((x2, y2))
        # print((x2, y2))
        filled.add((x2, y2))
        # import time
        #
        # time.sleep(0.1)

valid_pairs = []
for (x1, y1), (x2, y2) in pairs:
    y1, y2 = sorted([y1, y2])
    x1, x2 = sorted([x1, x2])
    ok = True

    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            if (x,y) not in filled:
                ok = False
                break
        if not ok: break

    if ok:
        valid_pairs.append(((x1, y1), (x2,y2)))

print(max((abs(x1 - x2) + 1) * (1 + abs(y1 - y2)) for (x1, y1), (x2, y2) in valid_pairs))
