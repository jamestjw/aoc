import sys
from collections import defaultdict
from functools import lru_cache, reduce

# file = open(sys.argv[1]).read().strip().split("\n")

# ore, clay, obsidian, geode
empty = (0, 0, 0, 0)
start_inventory = empty
start_robots = (0, 0, 0, 0)
blueprint = (
    (4, 0, 0, 0),
    (2, 0, 0, 0),
    (3, 14, 0, 0),
    (2, 0, 7, 0),
)

blueprint = (
    (2, 0, 0, 0),
    (3, 0, 0, 0),
    (3, 8, 0, 0),
    (3, 0, 12, 0),
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


def some_gt(t1, t2):
    return any(tuple(i > j for i, j in zip(t1, t2)))


def some_lt(t1, t2):
    return any(tuple(i < j for i, j in zip(t1, t2)))


def all_lte(t1, t2):
    return all(tuple(i <= j for i, j in zip(t1, t2)))


def one_at(i):
    return empty[:i] + (1,) + empty[i + 1 :]


def max_by_geode(t1, t2):
    if t1[3] > t2[3]:
        return t1
    else:
        return t2


iter_best = defaultdict(lambda: empty + empty)
iter_best_geode = defaultdict(lambda: 0)


def set_iter_best(curr, inventory, robots, pending_robots):
    val = inventory + (add(robots, pending_robots))
    if all_lte(val, iter_best[curr]):
        return False
    if some_gt(val, iter_best[curr]) and not some_lt(val, iter_best[curr]):
        print(f"new iter best: {curr} {val}")
        iter_best[curr] = val
    return True


def set_iter_best_geode(curr, robots, pending_robots):
    val = add(robots, pending_robots)[3]
    if val < iter_best_geode[curr]:
        return False
    iter_best_geode[curr] = max(iter_best_geode[curr], val)
    return True


@lru_cache
def go(
    curr_iter,
    max_iter,
    inventory,
    robots,
    pending_robots,
    blueprint,
):
    if curr_iter == max_iter:
        # print(inventory, robots)
        return inventory

    if not set_iter_best(curr_iter, inventory, robots, pending_robots):
        return inventory

    if not set_iter_best_geode(curr_iter, robots, pending_robots):
        return inventory

    new_inventory = add(inventory, robots)
    new_robots = add(robots, pending_robots)

    res = []
    for delta_inventory, cost in possible_purchases2(blueprint, new_inventory):
        res.append(
            go(
                curr_iter + 1,
                max_iter,
                sub(new_inventory, cost),
                new_robots,
                delta_inventory,  # reset pending robots
                blueprint,
            )
        )

    res.append(
        go(
            curr_iter + 1,
            max_iter,
            new_inventory,
            new_robots,
            empty,  # reset pending robots
            blueprint,
        )
    )
    return max(res, key=lambda x: x[3])


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
def possible_purchases2(blueprint, inventory):
    purchases = []
    for i, cost in enumerate(blueprint):
        # Can afford to buy
        if all(gte(inventory, cost)):
            purchases.append((one_at(i), cost))
    return purchases


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
                    if all_lte(new_inventory2 + new_robots, iter_best[remaining_iter]):
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
    )


print(run_iter(24))

# bfs(blueprint,15)
# bfs2(blueprint, 24)
