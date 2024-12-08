"""
This file contains a code attempt for advent of code day 19
"""


import os
import z3

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    day = __file__.split("\\", maxsplit=-1)[-1][:-3]
    my_tests = open(f"{day}_tests_input.txt", "r", encoding="utf-8").read().splitlines()

    s = z3.Optimize()
    x, y = z3.Int("x"), z3.Int("y")

    ore_robot_ore_cost = 4
    clay_robot_ore_cost = 2
    obsidian_robot_ore_cost = 3
    obsidian_robot_clay_cost = 14
    geode_robot_ore_cost = 2
    geode_robot_obsidian_cost = 7

    ore_robot_count = 1
    clay_robot_count = 0
    obsidian_robot_count = 0
    geode_robot_count = 0

    ores = 0
    clays = 0
    obsidians = 0
    geodes = z3.Int("geodes")

    for i in range(24):
        number_ore_robot_purchased = z3.Int(f"ore_robot_purchase_{i}")
        number_clay_robot_purchased = z3.Int(f"clay_robot_purchase_{i}")
        number_obsidian_robot_purchased = z3.Int(f"obsidian_robot_purchase_{i}")
        number_geode_robot_purchased = z3.Int(f"geode_robot_purchase_{i}")
        s.add(number_ore_robot_purchased >= 0)
        s.add(number_clay_robot_purchased >= 0)
        s.add(number_obsidian_robot_purchased >= 0)
        s.add(number_geode_robot_purchased >= 0)

        ore_production = ore_robot_count
        clays_production = clay_robot_count
        obsidians_production = obsidian_robot_count
        geodes_production = geode_robot_count

        ore_robot_count += number_ore_robot_purchased
        clay_robot_count += number_clay_robot_purchased
        obsidian_robot_count += number_obsidian_robot_purchased
        geode_robot_count += number_geode_robot_purchased

        s.add(
            ores
            - (number_ore_robot_purchased * ore_robot_ore_cost)
            - (number_clay_robot_purchased * clay_robot_ore_cost)
            - number_obsidian_robot_purchased * obsidian_robot_ore_cost
            - number_geode_robot_purchased * geode_robot_ore_cost
            >= 0
        )
        s.add(clays - (number_obsidian_robot_purchased * obsidian_robot_clay_cost) >= 0)
        s.add(
            obsidians - (number_obsidian_robot_purchased * geode_robot_obsidian_cost)
            >= 0
        )

        ores += ore_production
        clays += clays_production
        obsidians += obsidians_production
        geodes = geodes + geodes_production

    s.add(geodes > 0)
    s.maximize(geodes)
    assert s.check() == z3.sat
    model = s.model()

    part1 = model[geodes].as_long()
    part2 = 0

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
