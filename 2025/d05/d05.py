ranges, inp = list(map(lambda x: x.splitlines(), open(0).read().split("\n\n")))
inp = [int(i) for i in inp]
ranges = [tuple(map(int, lohi)) for r in ranges if (lohi := r.split("-"))]
ranges.sort(key=lambda x: x[0])

print(len([1 for i in inp if any(lo <= i <= hi for lo, hi in ranges)]))

combined = [ranges[0]]

for current_lo, current_hi in ranges[1:]:
    last_lo, last_hi = combined[-1]

    if current_lo <= last_hi:
        combined[-1] = (last_lo, max(last_hi, current_hi))
    else:
        combined.append((current_lo, current_hi))

print(sum(1 + hi - lo for lo, hi in combined))
