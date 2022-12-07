# part 1
python d07.py < d07_tests_input.txt | awk '{ if ($1 > max) { max = $1 }; if ($1 <= 100000) {s += $1} } END { printf "part1 %d\n part2: need to delete %d" , s , max - 40000000 }'

# part 2
python d07.py < d07_tests_input.txt | awk '$1 >= 7052440'
