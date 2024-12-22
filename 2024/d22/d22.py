import sys
from functools import reduce

file = open(sys.argv[1]).read()
initial_numbers = [int(e) for e in file.splitlines()]


def mix(secret, other):
    return secret ^ other


def prune(secret):
    return secret % 16777216


def next_secret(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, int(secret / 32)))
    secret = prune(mix(secret, secret * 2048))

    return secret


def generate_list(secret, n):
    res = [secret]
    for _ in range(n):
        res.append(next_secret(res[-1]))
    return res


secrets = [generate_list(i, 2000) for i in initial_numbers]
print(sum([s[-1] for s in secrets]))


def build_changes_dict(secrets):
    secrets = [s % 10 for s in secrets]  # only want last digit
    prev = secrets[0]
    d = dict()
    changes = []
    for secret in secrets[1:]:
        changes.append(secret - prev)
        if len(changes) == 4:
            k = tuple(changes)
            d.setdefault(k, secret)
            changes.pop(0)
        prev = secret
    return d


def sum_from_dict(k, dicts):
    return sum(d.get(k, 0) for d in dicts)


dicts = [build_changes_dict(s) for s in secrets]
keys = reduce(lambda s, d: s | set(d.keys()), dicts, set())


print(max([sum_from_dict(k, dicts) for k in keys]))
