"""
This file contains a code attempt for advent of code day 16
"""

import re


def floyd(G):
    nV = len(G)
    dist = list(map(lambda p: list(map(lambda q: q, p)), G))
    for r in range(nV):
        for p in range(nV):
            for q in range(nV):
                dist[p][q] = min(dist[p][q], dist[p][r] + dist[r][q])
    return dist


if __name__ == "__main__":
    lines = open("input.txt", "r", encoding="utf-8").read().splitlines()
    # lines = open("smol.txt", "r", encoding="utf-8").read().splitlines()
    lines = [
        (int(re.search("(\d+)", x).groups()[0]), re.findall("[A-Z]{2}", x))
        for x in lines
    ]
    valves = {valves[0]: (rate, valves[1:]) for rate, valves in lines}
    name2id = {name: i for i, name in enumerate(valves.keys())}

    useful_valves = [name for name, (rate, _) in valves.items() if rate > 0]

    adjacency = [[99999999 for _ in range(len(valves))] for _ in range(len(valves))]

    for name, (_, adjs) in valves.items():
        for adj in adjs:
            adjacency[name2id[name]][name2id[adj]] = 1

    shortestPath = floyd(adjacency)

    def get_distance(src, dest):
        return shortestPath[name2id[src]][name2id[dest]]

    useful_valve_neighbors = {
        name: {
            neighbor: get_distance(neighbor, name)
            for neighbor in useful_valves
            if neighbor != name
        }
        for name in valves
    }

    FULL_TIME = 30
    REDUCED_TIME = 26
    start = 'AA'

    def traverse(opened, time, score, remaining, cheat=True):
        incr = []
        curr_neighbors = useful_valve_neighbors[opened[-1]]

        for neighbor in remaining:
            distance = curr_neighbors[neighbor]
            required_time = distance + 1
            if required_time < time:
                rate, _ = valves[neighbor]
                incr += [
                    traverse(
                        opened + [neighbor],
                        time - required_time,
                        score + (time - required_time) * rate,
                        remaining - {neighbor},
                        cheat
                    )
                ]

        if cheat:
            incr += [traverse(opened + [start], REDUCED_TIME, score, remaining, False)]

        return max(incr, default=[opened, score], key=lambda x: x[1])

    print(traverse([start], FULL_TIME, 0, set(useful_valves), cheat=False))
    print(traverse([start], REDUCED_TIME, 0, set(useful_valves), cheat=True))