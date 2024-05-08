import sys
from collections import defaultdict

lines = open(sys.argv[1]).read().splitlines()
edges = defaultdict(lambda: list())

for line in lines:
    src, dest = line.split("-")
    edges[src].append(dest)
    edges[dest].append(src)


def part1():
    paths = []

    Q = [("start", {"start"})]

    while len(Q) != 0:
        curr, visited = Q.pop(0)

        for dest in edges[curr]:
            if dest == "end":
                paths.append(visited | {dest})
            elif dest[0].isupper() or dest not in visited:
                Q.append((dest, visited | {dest}))

    print(len(paths))


def part2():
    paths = []

    # We keep track of whether or not we have visited a small cave twice
    # curr_node, visited, small_twice
    Q: list[tuple[str, set[str], bool]] = [("start", {"start"}, False)]

    while len(Q) != 0:
        curr, visited, small_twice = Q.pop(0)

        for dest in edges[curr]:
            if dest == "end":
                paths.append(visited | {dest})
            elif dest[0].isupper() or dest not in visited:
                # 'start' is already in visited for sure
                Q.append((dest, visited | {dest}, small_twice))
            elif dest in visited and dest != "start" and not small_twice:
                Q.append((dest, visited | {dest}, True))

    print(len(paths))


part1()
part2()
