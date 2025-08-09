import sys
import math
import re
from operator import add

file = open(sys.argv[1]).read().strip()
numbers = re.findall(r"\d+", file)
# Always skip the first number and take the subsequent 6
blueprints = [tuple(map(int, numbers[i : i + 6])) for i in range(1, len(numbers), 7)]


def run(
    cache: dict,
    inventory: tuple[int, int, int, int, int, int, int, int],
    iters,
    blueprint,
):
    ore, clay, obsidian, geode, ore_bot, clay_bot, obsidian_bot, geode_bot = inventory
    (
        ore_ore_cost,
        clay_ore_cost,
        obsi_ore_cost,
        obsi_clay_cost,
        geode_ore_cost,
        geode_obsi_cost,
    ) = blueprint

    if iters == 0:
        return cache, geode

    if (score := cache.get((iters, inventory))) is not None:
        return cache, score

    null = inventory
    buy_ore = (
        ore - ore_ore_cost,
        clay,
        obsidian,
        geode,
        ore_bot + 1,
        clay_bot,
        obsidian_bot,
        geode_bot,
    )
    buy_clay = (
        ore - clay_ore_cost,
        clay,
        obsidian,
        geode,
        ore_bot,
        clay_bot + 1,
        obsidian_bot,
        geode_bot,
    )
    buy_obs = (
        ore - obsi_ore_cost,
        clay - obsi_clay_cost,
        obsidian,
        geode,
        ore_bot,
        clay_bot,
        obsidian_bot + 1,
        geode_bot,
    )
    buy_geod = (
        ore - geode_ore_cost,
        clay,
        obsidian - geode_obsi_cost,
        geode,
        ore_bot,
        clay_bot,
        obsidian_bot,
        geode_bot + 1,
    )

    if ore >= geode_ore_cost and obsidian >= geode_obsi_cost:
        next_inventories = [buy_geod]
    elif ore >= obsi_ore_cost and clay >= obsi_clay_cost:
        next_inventories = [buy_obs]
    else:
        next_inventories = [
            i for i in [null, buy_clay, buy_ore] if all(e >= 0 for e in i)
        ]

    next_inventories = [
        tuple(map(add, i, (ore_bot, clay_bot, obsidian_bot, geode_bot, 0, 0, 0, 0)))
        for i in next_inventories
    ]

    cache2 = cache
    scores = []
    for inv in next_inventories:
        cache2, score = run(cache2, inv, iters - 1, blueprint)
        scores.append(score)
    best_score = max(scores)
    cache2[(iters, inventory)] = best_score

    return cache2, best_score


print(
    sum(
        [
            i * score
            for i, (_, score) in enumerate(
                [run(dict(), (0, 0, 0, 0, 1, 0, 0, 0), 24, bp) for bp in blueprints], 1
            )
        ]
    )
)

print(
    math.prod(
        [
            score
            for (_, score) in [
                run(dict(), (0, 0, 0, 0, 1, 0, 0, 0), 32, bp) for bp in blueprints[:3]
            ]
        ]
    )
)
