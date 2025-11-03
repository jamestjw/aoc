import re
import sys
import z3

instructions = [x.split() for x in open(sys.argv[1]).read().splitlines()]

opt = z3.Optimize()
ints = []
for i in range(14):
    int_var = z3.Int(f"int_{i}")
    ints.append(int_var)

next_int_index = 0
state = {c: 0 for c in "wxyz"}
for instr in instructions:
    print(instr)
    match instr:
        case ["inp", var]:
            state[var] = ints[next_int_index]
            next_int_index += 1
        case ["add", x, y]:
            y_var = int(y) if y.lstrip("-").isdigit() else state[y]
            state[x] = state[x] + y_var
        case ["mul", x, y]:
            y_var = int(y) if y.lstrip("-").isdigit() else state[y]
            state[x] = state[x] * y_var
        case ["div", x, y]:
            y_var = int(y) if y.lstrip("-").isdigit() else state[y]
            state[x] = state[x] / y_var
        case ["mod", x, y]:
            y_var = int(y) if y.lstrip("-").isdigit() else state[y]
            state[x] = state[x] % y_var
        case ["eql", x, y]:
            y_var = int(y) if y.lstrip("-").isdigit() else state[y]
            state[x] = z3.If(state[x] == y_var, 1, 0)

total = 0
for i1, i2 in zip(range(14), ints[::-1]):
    total += int("1" + ("0" * i1)) * i2
opt.maximize(total)

for i in ints:
    opt.add(i > 0)
    opt.add(i <= 9)

opt.add(state["z"] == 0)

# opt.add(t_max <= t_area)
# opt.add(x_start <= calculate_x(0, vx, t_area))
# opt.add(calculate_x(0, vx, t_area) <= x_end)
# opt.add(y_start <= calculate_y(0, vy, t_area))
# opt.add(calculate_y(0, vy, t_area) <= y_end)
# opt.maximize(calculate_y(0, vy, t_max))

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
