import sys
from collections import defaultdict
from functools import lru_cache

# file = open(sys.argv[1]).read().strip().split("\n")

# ore, clay, obsidian, geode
empty = (0, 0, 0, 0)
start_inventory = (0, 0, 0, 0)
start_robots = (0, 0, 0, 0)
blueprint = (
    (4, 0, 0, 0),
    (2, 0, 0, 0),
    (3, 14, 0, 0),
    (2, 0, 7, 0),
)

TYPES = ["ore", "clay", "obsidian", "geode"]


def add(t1, t2):
    return tuple(i + j for i, j in zip(t1, t2))


def sub(t1, t2):
    return tuple(i - j for i, j in zip(t1, t2))


def gte(t1, t2):
    return tuple(i >= j for i, j in zip(t1, t2))


def all_gte(t1, t2):
    return all(gte(t1, t2))


def all_lt(t1, t2):
    return all(tuple(i <= j for i, j in zip(t1, t2)))


def one_at(i):
    return empty[:i] + (1,) + empty[i + 1 :]


def max_by_geode(t1, t2):
    if t1[3] > t2[3]:
        return t1
    else:
        return t2


iter_best = defaultdict(lambda: empty + empty)


@lru_cache
def go(
    curr_iter,
    max_iter,
    inventory,
    robots,
    pending_robots,
    blueprint,
    declined_purchases,
):
    if curr_iter == max_iter:
        # print(inventory, robots)
        return inventory

    # ore, clay, obsidian, geode = inventory
    # oreR, clayR, obsidianR, geodeR = robots
    # oreCost, clayCost, obsidianCost, geodeCost = blueprint
    # oreDeclined, clayDeclined, obsidianDeclined, geodeDeclined = declined_purchases

    if all(declined_purchases):
        new_inventory = add(inventory, robots)
        new_robots = add(robots, pending_robots)

        remaining_iter = max_iter - curr_iter
        if all_lt(new_inventory + new_robots, iter_best[remaining_iter]):
            # import pdb; pdb.set_trace()
            return iter_best[curr_iter][:4]  # short circuit

        if all_gte(new_inventory + new_robots, iter_best[remaining_iter]):
            iter_best[remaining_iter] = new_inventory + new_robots
        return go(
            curr_iter + 1,
            max_iter,
            new_inventory,
            new_robots,
            empty,  # reset pending robots
            blueprint,
            (False,) * 4,  # reset declined purchases
        )
    else:
        next_type = next(
            i for i, declined in enumerate(declined_purchases) if not declined
        )
        cost = blueprint[next_type]
        if all(gte(inventory, cost)):
            buy = go(
                curr_iter,
                max_iter,
                sub(inventory, cost),
                robots,
                add(pending_robots, one_at(next_type)),
                blueprint,
                declined_purchases,  # don't decline since might want to purchase again
            )
            no_buy = go(
                curr_iter,
                max_iter,
                inventory,
                robots,
                pending_robots,
                blueprint,
                declined_purchases[:next_type]
                + (True,)
                + declined_purchases[next_type + 1 :],
            )
            return max_by_geode(buy, no_buy)
        else:
            # Can't afford to build
            return go(
                curr_iter,
                max_iter,
                inventory,
                robots,
                pending_robots,
                blueprint,
                declined_purchases[:next_type]
                + (True,)
                + declined_purchases[next_type + 1 :],
            )


def run_iter(i):
    return go(
        0,
        i,
        empty,
        (1, 0, 0, 0),
        empty,
        blueprint,
        (False,) * 4,
    )


res = run_iter(15)
