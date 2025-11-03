import re
import sys
import z3

x_start, x_end, y_start, y_end = tuple(
    map(int, re.findall(r"-?\d+", open(sys.argv[1]).read()))
)


def arith_sum(a, d, n):
    return n / 2 * (2 * a + (n - 1) * d)


def z3_abs(x):
    return z3.If(x >= 0, x, -x)

def z3_min(x, y):
    return z3.If(x < y, x, y)

def calculate_x(initial, velocity, time):
    d = z3.If(velocity > 0, -1, 1)
    abs_velo = z3_abs(velocity)
    
    return initial + arith_sum(velocity, d, z3_min(abs_velo, time))
    # return z3.If(
    #     time > abs_velo,
    #     initial + arith_sum(velocity, d, abs_velo),
    #     initial + arith_sum(velocity, d, time),
    # )

def calculate_y(initial, velocity, time):
    return initial + arith_sum(velocity, -1, time)

opt = z3.Optimize()

vx = z3.Int("vx")
vy = z3.Int("vy")
t_area = z3.Int("t_area")
t_max = z3.Int("t_max")

opt.add(t_max <= t_area)
opt.add(x_start <= calculate_x(0, vx, t_area))
opt.add(calculate_x(0, vx, t_area) <= x_end)
opt.add(y_start <= calculate_y(0, vy, t_area))
opt.add(calculate_y(0, vy, t_area) <= y_end)
opt.maximize(calculate_y(0, vy, t_max))

print(opt.check())
# print(opt.upper(h))
print(opt.model())

# # There are a number of very clever insights on Reddit regarding Part 2. I
# # particularily enjoyed u/bluepichu's. I, however, propose a much more brute
# # solution.
# s = z3.Solver()
# x, y = z3.Int("x"), z3.Int("y")

# s.add(0 <= x); s.add(x <= 4000000)
# s.add(0 <= y); s.add(y <= 4000000)

# def z3_abs(x):
#     return z3.If(x >= 0, x, -x)

# for sx, sy, bx, by in observations:
#     m = abs(sx - bx) + abs(sy - by)
#     s.add(z3_abs(sx - x) + z3_abs(sy - y) > m)

# assert s.check() == z3.sat
# model = s.model()
# print("Part 2:", model[x].as_long() * 4000000 + model[y].as_long())
