import re
import functools
import z3

lines = open(0).read().splitlines()
inp = [
    (
        re.findall(r"\[(.*)\]", line)[0],
        re.findall(r"\((.*?)\)", line),
        re.findall(r"\{(.*)\}", line)[0],
    )
    for line in lines
]


def parse_buttons(buttons, n):
    start = [False] * n

    for c in buttons.split(","):
        start[int(c)] = True

    return tuple(start)


def parse_buttons2(buttons, n):
    start = [False] * n

    for c in buttons.split(","):
        start[int(c)] = True

    return tuple(map(int, start))


def find_min_pt1(target, buttons):
    start = (False,) * len(target)
    target = tuple(c == "#" for c in target)
    buttons = [parse_buttons(b, len(target)) for b in buttons]

    def go(states, n):
        next_states = set()

        for state in states:
            for b in buttons:
                next_state = tuple(a ^ b for a, b in zip(state, b))
                if next_state == target:
                    return n + 1
                next_states.add(next_state)

        return go(next_states, n + 1)

    return go([start], 0)


def find_min_pt2(target, buttons):
    target = tuple(int(c) for c in target.split(","))
    buttons = [parse_buttons2(b, len(target)) for b in buttons]

    s = z3.Optimize()
    coefs = [z3.Int(f"x{i}") for i in range(len(buttons))]
    for c in coefs:
        s.add(c >= 0)

    transposed = list(zip(*buttons))

    for bs, t in zip(transposed, target):
        prods = [b * coef for b, coef in zip(bs, coefs)]
        s.add(functools.reduce(lambda x, y: x + y, prods) == t)

    s.minimize(z3.Sum(coefs))
    assert s.check()

    model = s.model()
    return sum(model.evaluate(c).as_long() for c in coefs)

print(sum(find_min_pt1(target, buttons) for target, buttons, _ in inp))
print(sum(find_min_pt2(target, buttons) for _, buttons, target in inp))
