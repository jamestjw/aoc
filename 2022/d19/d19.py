"""
This file contains a code attempt for advent of code day 19
"""


import os
from functools import lru_cache


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    day = __file__.split("\\", maxsplit=-1)[-1][:-3]
    my_tests = open(f"{day}_tests_input.txt", "r", encoding="utf-8").read().splitlines()

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
    geodes = 0

    @lru_cache(maxsize=1000000000)
    def traverse(
        i,
        ores,
        clays,
        obsidians,
        geodes,
        ore_robots,
        clay_robots,
        obsidian_robots,
        geode_robots,
    ):
        print(
            ores,
            clays,
            obsidians,
            geodes,
            ore_robots,
            clay_robots,
            obsidian_robots,
            geode_robots,
        )
        if i == 0:
            return geodes
        options = [geodes]
        for num_ore_purchased in range(ores // ore_robot_ore_cost + 1):
            remaining_ores = ores - num_ore_purchased * ore_robot_ore_cost
            for num_clay_purchased in range(remaining_ores // clay_robot_ore_cost + 1):
                remaining_ores2 = (
                    remaining_ores - num_clay_purchased * clay_robot_ore_cost
                )
                for num_obsidian_purchased in range(
                    min(
                        remaining_ores2 // obsidian_robot_ore_cost,
                        clays // obsidian_robot_clay_cost,
                    )
                    + 1
                ):
                    remaining_ores3 = (
                        remaining_ores2
                        - num_obsidian_purchased * obsidian_robot_ore_cost
                    )
                    remaining_clay = (
                        clays - num_obsidian_purchased * obsidian_robot_clay_cost
                    )
                    for num_geode_purchased in range(
                        min(
                            remaining_ores3 // geode_robot_ore_cost,
                            obsidians // geode_robot_obsidian_cost,
                        )
                        + 1
                    ):
                        remaining_ores4 = (
                            remaining_ores3 - num_geode_purchased * geode_robot_count
                        )
                        remaining_obsidians = (
                            obsidians - num_geode_purchased * geode_robot_obsidian_cost
                        )
                        options.append(
                            traverse(
                                i - 1,
                                remaining_ores4 + ore_robots,
                                remaining_clay + clay_robots,
                                remaining_obsidians + obsidian_robots,
                                geodes + geode_robots,
                                ore_robots + num_ore_purchased,
                                clay_robots + num_clay_purchased,
                                obsidian_robots + num_obsidian_purchased,
                                geode_robots + num_geode_purchased,
                            )
                        )

        return max(options)

    part1 = traverse(24, 0, 0, 0, 0, 1, 0, 0, 0)
    part2 = 0

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
