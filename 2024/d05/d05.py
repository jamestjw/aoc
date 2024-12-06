import functools
import sys

file = open(sys.argv[1]).read()

order_str, pages_str = file.split("\n\n")
order = {pair for pair in order_str.split("\n")}
pages = [page.split(",") for page in pages_str.strip().split("\n")]


def mid(l):
    return l[len(l) // 2]


def compare(left, right):
    if left == right:
        return 0
    if f"{left}|{right}" in order:
        return -1
    if f"{right}|{left}" in order:
        return 1
    raise Exception("impossible, we expect a total order")


valid, invalid = 0, 0
for page in pages:
    sorted_page = sorted(page, key=functools.cmp_to_key(compare))
    if page == sorted_page:
        valid += int(mid(page))
    else:
        invalid += int(mid(sorted_page))

print(valid, invalid)
