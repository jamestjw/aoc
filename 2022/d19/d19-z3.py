"""
This file contains a code attempt for advent of code day 19
"""


import os
import z3

if __name__ == "__main__":
    s = z3.Optimize()
    x, y = z3.Int("x"), z3.Int("y")

    ore_robot_ore_cost = 4
    clay_robot_ore_cost = 2
    obsidian_robot_ore_cost = 3
    obsidian_robot_clay_cost = 14
    geode_robot_ore_cost = 2
    geode_robot_obsidian_cost = 7

    iterations = 24
    ore_purchases = [z3.Int(f"ore_robot_purchase_{i}") for i in range(iterations)]
    clay_purchases = [z3.Int(f"clay_robot_purchase_{i}") for i in range(iterations)]
    obsidian_purchases = [
        z3.Int(f"obsidian_robot_purchase_{i}") for i in range(iterations)
    ]
    geode_purchases = [z3.Int(f"geode_robot_purchase_{i}") for i in range(iterations)]

    # ores = [0] + [z3.Int(f'ores_{i+1}') for i in range(iterations)]
    # clays = [0] + [z3.Int(f'clays{i+1}') for i in range(iterations)]
    # obsidians = [0] + [z3.Int(f'obsidians{i+1}') for i in range(iterations)]
    # geodes = [0] + [z3.Int(f'geodes{i+1}') for i in range(iterations)]

    for c in ore_purchases + clay_purchases + obsidian_purchases + geode_purchases:
        s.add(c >= 0)

    ores = 0
    obsidians = clays = 0

    for i in range(iterations):
        remaining_ores = (
            ores
            - (ore_purchases[i] * ore_robot_ore_cost)
            - (clay_purchases[i] * clay_robot_ore_cost)
            - (obsidian_purchases[i] * obsidian_robot_ore_cost)
            - (geode_purchases[i] * geode_robot_ore_cost)
        )
        remaining_clays = clays - (obsidian_purchases[i] * obsidian_robot_clay_cost)
        remaining_obsidians = obsidians - (
            geode_purchases[i] * geode_robot_obsidian_cost
        )
        s.add(remaining_ores >= 0)
        s.add(remaining_clays >= 0)
        s.add(remaining_obsidians >= 0)
        # ore_robots = 1 + sum(ore_purchases[:i])
        # clay_robots = sum(clay_purchases[:i])
        # obsidian_robots = sum(obsidian_purchases[:i])
        # geode_robots = sum(geode_purchases[:i])
        # Purchases before this iteration
        ores = 1 + sum(ore_purchases[:i]) + remaining_ores
        clays = sum(clay_purchases[:i]) + remaining_clays
        obsidians = sum(obsidian_purchases[:i]) + remaining_obsidians

    geodes = 0
    for i, g in enumerate(geode_purchases):
        geodes += g * (iterations - i - 1)

    print("maximising...")
    s.maximize(geodes)
    assert s.check() == z3.sat
    model = s.model()
    print(model)
    part1 = 0
    part2 = 0

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
