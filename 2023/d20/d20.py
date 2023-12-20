from math import prod, lcm
import collections
import sys
import re

file = open(sys.argv[1]).read().strip().split("\n")

modules = {}

for row in file:
    m = re.search(r"(%|&)?(\w+) -> (.*)", row)
    if not m:
        raise Exception
    ty, name, targets = m.groups()
    modules[name] = (ty, targets.split(", "))

rx_inp = [name for name, (_, targs) in modules.items() if "rx" in targs]
rx_inp_sources = [
    name for name, (_, targs) in modules.items() if any(e in targs for e in rx_inp)
]


def go(num_iters):
    rx_dict = dict()
    # Keeps track of whether they are on or off
    # True = on
    flipflops = collections.defaultdict(lambda: False)

    conjunctions = dict()  # Last received signal from inputs
    for name, (ty, _) in modules.items():
        if ty == "&":
            conjunctions[name] = dict()
            for name2, (_, targs) in modules.items():
                if name in targs:
                    conjunctions[name][name2] = False

    num_lows = 0
    num_highs = 0

    for i in range(num_iters):
        # source, dest, low|high
        todolist = collections.deque([])
        todolist.append(("button", "broadcaster", False))

        while todolist:
            src, dest, is_high = todolist.popleft()

            if src in rx_inp_sources and dest in rx_inp and is_high:
                if src not in rx_dict:
                    rx_dict[src] = i + 1
                if len(rx_dict) == len(rx_inp_sources):
                    print(lcm(*rx_dict.values()))
                    return

            num_highs += int(is_high)
            num_lows += int(not is_high)

            if dest not in modules:
                continue  # Ignore dummies

            dest_type, dest_targets = modules[dest]

            match dest_type:
                case None:  # broadcaster
                    for targ in dest_targets:
                        todolist.append((dest, targ, is_high))
                case "%":  # flipflop
                    if is_high:
                        continue
                    else:
                        flipflops[dest] ^= True
                        for targ in dest_targets:
                            todolist.append((dest, targ, flipflops[dest]))
                case "&":  # conjunction
                    conjunctions[dest][src] = is_high
                    to_send = not all(conjunctions[dest].values())

                    for targ in dest_targets:
                        todolist.append((dest, targ, to_send))

                case _:
                    raise Exception

    print(num_lows * num_highs)


go(1000)
go(sys.maxsize)
