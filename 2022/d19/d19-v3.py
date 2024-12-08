import sys
from collections import defaultdict
from functools import lru_cache, reduce

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


def tuple_max(t1, t2):
    return tuple(max(i, j) for i, j in zip(t1, t2))


def add(t1, t2):
    return tuple(i + j for i, j in zip(t1, t2))


def sub(t1, t2):
    return tuple(i - j for i, j in zip(t1, t2))


def gte(t1, t2):
    return tuple(i >= j for i, j in zip(t1, t2))


def lt(t1, t2):
    return tuple(i < j for i, j in zip(t1, t2))


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


def bfs(blueprint, max_iter):
    Q = [(0, empty, (1, 0, 0, 0), empty, (False,) * 4)]
    seen = set()

    while len(Q) != 0:
        (
            curr_iter,
            inventory,
            robots,
            pending_robots,
            declined_purchases,
        ) = Q.pop(0)

        print(curr_iter)

        if all(declined_purchases):
            new_inventory = add(inventory, robots)
            new_robots = add(robots, pending_robots)

            if curr_iter + 1 == max_iter:
                print("RES:", blueprint, new_inventory)
            else:
                new_key = (
                    curr_iter + 1,
                    new_inventory,
                    new_robots,
                    empty,
                    (False,) * 4,
                )
                if new_key not in seen:
                    seen |= {new_key}
                    Q.append(new_key)
        else:
            next_type = next(
                i for i, declined in enumerate(declined_purchases) if not declined
            )
            cost = blueprint[next_type]
            new_keys = []
            # Can afford to buy
            if all(gte(inventory, cost)):
                # Add key for purchase
                new_keys.append(
                    (
                        curr_iter,
                        sub(inventory, cost),
                        robots,
                        add(pending_robots, one_at(next_type)),
                        declined_purchases,  # don't decline since might want to purchase again
                    )
                )

                # Decline the purchase
                new_keys.append(
                    (
                        curr_iter,
                        inventory,
                        robots,
                        pending_robots,
                        declined_purchases[:next_type]
                        + (True,)
                        + declined_purchases[
                            next_type + 1 :
                        ],  # don't decline since might want to purchase again
                    )
                )
            else:
                # Can't afford to buy, so mark as declined
                new_keys.append(
                    (
                        curr_iter,
                        inventory,
                        robots,
                        pending_robots,
                        declined_purchases[:next_type]
                        + (True,)
                        + declined_purchases[next_type + 1 :],
                    )
                )
            for new_key in new_keys:
                if new_key not in seen:
                    seen |= {new_key}
                    Q.append(new_key)


@lru_cache(maxsize=None)
def possible_purchases(blueprint, inventory):
    def helper(declined_purchases, inventory, bought):
        if all(declined_purchases):
            return {(inventory, bought)}
        else:
            next_type = next(
                i for i, declined in enumerate(declined_purchases) if not declined
            )
            cost = blueprint[next_type]
            # Can afford to buy
            if all(gte(inventory, cost)):
                # Add key for purchase
                option1 = helper(
                    declined_purchases,  # don't decline since might want to purchase again
                    sub(inventory, cost),
                    add(bought, one_at(next_type)),
                )

                # Decline the purchase
                option2 = helper(
                    declined_purchases[:next_type]
                    + (True,)
                    + declined_purchases[
                        next_type + 1 :
                    ],  # don't decline since might want to purchase again
                    inventory,
                    bought,
                )
                return option1 | option2

            else:
                # Can't afford to buy, so mark as declined
                return helper(
                    declined_purchases[:next_type]
                    + (True,)
                    + declined_purchases[next_type + 1 :],
                    inventory,
                    bought,
                )

    return list(helper((False,) * 4, inventory, empty))


# @lru_cache(maxsize=1024)
@lru_cache(maxsize=None)
def helper(blueprint, declined_purchases, inventory, bought):
    if all(declined_purchases):
        return {(inventory, bought)}
    else:
        next_type = next(
            i for i, declined in enumerate(declined_purchases) if not declined
        )
        cost = blueprint[next_type]
        # Can afford to buy
        if all(gte(inventory, cost)):
            # Add key for purchase
            option1 = helper(
                blueprint,
                declined_purchases,  # don't decline since might want to purchase again
                sub(inventory, cost),
                add(bought, one_at(next_type)),
            )

            # Decline the purchase
            option2 = helper(
                blueprint,
                declined_purchases[:next_type]
                + (True,)
                + declined_purchases[
                    next_type + 1 :
                ],  # don't decline since might want to purchase again
                inventory,
                bought,
            )
            return option1 | option2

        else:
            # Can't afford to buy, so mark as declined
            return helper(
                blueprint,
                declined_purchases[:next_type]
                + (True,)
                + declined_purchases[next_type + 1 :],
                inventory,
                bought,
            )


@lru_cache(maxsize=None)
def possible_purchases2(blueprint, inventory):
    res = [(inventory, empty)]
    for i, cost in enumerate(blueprint):
        if all_gte(inventory, cost):
            res.append((sub(inventory, cost), one_at(i)))
    return res


def should_prune(blueprint, robots):
    max_cost = reduce(tuple_max, blueprint)
    if any(lt(max_cost[:3], robots[:3])):
        return True
    return False


def bfs2(blueprint, max_iter):
    Q = [(0, empty, (1, 0, 0, 0))]
    seen = set()
    iter_best = defaultdict(lambda: empty + empty)

    while len(Q) != 0:
        (
            curr_iter,
            inventory,
            robots,
        ) = Q.pop(0)

        print(curr_iter)

        for new_inventory, purchase in possible_purchases2(blueprint, inventory):
            new_inventory2 = add(new_inventory, robots)
            new_robots = add(robots, purchase)
            new_key = (curr_iter + 1, new_inventory2, new_robots)

            if curr_iter + 1 == max_iter:
                print(new_key)
            else:
                if new_key not in seen:
                    seen |= {new_key}
                    remaining_iter = max_iter - curr_iter
                    if should_prune(blueprint, robots):
                        continue
                    if all_lt(new_inventory2 + new_robots, iter_best[remaining_iter]):
                        continue

                    if all_gte(new_inventory2 + new_robots, iter_best[remaining_iter]):
                        iter_best[remaining_iter] = new_inventory2 + new_robots
                    Q.append(new_key)


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


# res = run_iter(15)

# bfs(blueprint,15)
# bfs2(blueprint, 24)
