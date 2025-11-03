import re
import math
import sys

x_start, x_end, y_start, y_end = tuple(
    map(int, re.findall(r"-?\d+", open(sys.argv[1]).read()))
)


def arith_sum(a, d, n):
    return int(n / 2 * (2 * a + (n - 1) * d))


def calculate_x(initial, velocity, time):
    d = -1 if velocity > 0 else 1
    abs_velo = abs(velocity)

    return initial + arith_sum(velocity, d, min(abs_velo, time))


def calculate_y(initial, velocity, time):
    return initial + arith_sum(velocity, -1, time)


def get_candidate_x(start, end):
    candidates = []
    next_candidate = 0
    while True:
        t = 0
        ok = False
        max_disp = -1
        while True:
            disp = arith_sum(next_candidate, -1, min(next_candidate, t))
            if disp == max_disp:
                break
            elif disp < start:
                max_disp = disp
                t += 1
                continue
            elif start <= disp <= end:
                candidates.append((next_candidate, t))
                ok = True
                break
            else:
                break
        if not ok and len(candidates) != 0:
            break
        next_candidate += 1
    return candidates


def get_x_end_time(velocity, start, end, start_time):
    end_time = start_time + 1
    disp = arith_sum(velocity, -1, start_time)
    while True:
        new_disp = calculate_x(0, velocity, end_time)
        if new_disp != disp:
            if new_disp <= end:
                disp = new_disp
                end_time += 1
            else:
                break
        else:
            end_time = math.inf
            break

    return end_time - 1


def get_y_end_time(velocity, start, end, start_time):
    end_time = start_time + 1
    disp = calculate_y(0, velocity, start_time)
    while True:
        new_disp = calculate_y(0, velocity, end_time)

        if start <= new_disp <= end:
            disp = new_disp
            end_time += 1
        else:
            break

    return end_time - 1


def get_candidate_y(start, end):
    candidates = []

    next_candidate = 0
    while True:
        t = 0
        ok = False

        while True:
            disp = arith_sum(next_candidate, -1, t)

            if disp < start:
                break
            elif start <= disp <= end:
                candidates.append((next_candidate, t))
                ok = True
                break
            else:
                t += 1
                continue
        if not ok and len(candidates) != 0:
            break
        next_candidate += 1

    next_candidate = -1
    while True:
        t = 0
        ok = False

        while True:
            disp = arith_sum(next_candidate, -1, t)

            if disp < start:
                break
            elif start <= disp <= end:
                candidates.append((next_candidate, t))
                ok = True
                break
            else:
                t += 1
                continue
        if not ok and len(candidates) != 0:
            break
        next_candidate -= 1

    return candidates


candidate_xs = [
    (x, t, get_x_end_time(x, x_start, x_end, t))
    for x, t in get_candidate_x(x_start, x_end)
]


candidate_ys = [
    (y, t, get_y_end_time(y, y_start, y_end, t))
    for y, t in get_candidate_y(y_start, y_end)
]

candidate_ys.sort(key=lambda x: -x[0])


def intervals_intersect(x, y):
    x_start, x_end = x
    y_start, y_end = y
    # return min(x_end, y_end) - max(x_start, y_start) >= 0
    return not (x_end < y_start or y_end < x_start)


good_ys = [
    (vy, t1, t2)
    for (vy, t1, t2) in candidate_ys
    if any(intervals_intersect((t1, t2), (tx1, tx2)) for _, tx1, tx2 in candidate_xs)
]

max_ys = [arith_sum(v, -1, max(v, 0)) for v, _, _ in good_ys]
# 1081 too low
max_y = max(arith_sum(v, -1, max(v, 0)) for v, _, _ in good_ys)
