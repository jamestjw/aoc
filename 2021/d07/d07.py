import sys
import math

file = open(sys.argv[1]).read()
nums = sorted([int(e) for e in file.split(",")])

## https://stackoverflow.com/questions/23452479/minimise-the-sum-of-difference-between-each-element-of-an-array-and-an-integer-k
## Median minimises absolute deviation
if len(nums) % 2 == 0:
    median = nums[len(nums) // 2 - 1]
else:
    median  = nums[(len(nums) + 1) // 2 - 1]

print(f"Median is {median}")
print(f"Dist is {sum([abs(num - median) for num in nums])}")

## FIXME: Depending on the data, math.ceil may give a better score
avg = math.floor(sum(nums)/len(nums))
dist = 0.0

for num in nums:
    abs_diff = abs(num - avg)
    dist += abs_diff * (abs_diff + 1) / 2

print(f"Dist is {dist}")
