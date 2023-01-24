NB. _2 indicates that cut should split on the last
NB. char (newline) and not include it in the result
data =: (< ;. _2 @: fread) 'input.txt'
NB. Add blank space at the end so we can cut on it
NB. Then convert to integers
NB. Then sum across 1st dimension
elves =: (+/"1) 0". > ;. _2 (data , <'')
NB. Reduce by taking max
max =: >./ elves
NB. Sort, take first three, then sum
sumtop3 =: +/ 0 1 2  { \:~ elves
echo max, sumtop3
