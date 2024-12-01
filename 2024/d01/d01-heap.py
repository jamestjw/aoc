import sys
import heapq

file = open(sys.argv[1]).read()

inp_lines = [list(map(int, l.split())) for l in file.splitlines()]
left, right = [list(l) for l in list(zip(*inp_lines))]

# O(n)
heapq.heapify(left)
heapq.heapify(right)

total = 0
while left and right:
    # Popping is O(log n)
    x, y = heapq.heappop(left), heapq.heappop(right)
    total += abs(x - y)

print(total)
