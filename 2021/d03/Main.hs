solvePt1 :: [String] -> Int
solvePt1 lines = bitsToInt majority * bitsToInt minority
  where
    numBits = length $ head lines
    f :: [Int] -> String -> [Int]
    f acc line = do
      (i, bit) <- zip acc line
      return $ case bit of
        '1' -> i + 1
        _ -> i - 1
    collect :: [String] -> [Int]
    collect = foldl f (replicate numBits 0)
    bitsToInt :: [Bool] -> Int
    bitsToInt = foldl (\acc x -> acc * 2 + fromEnum x) 0
    majority = map (0 <) $ collect lines
    minority = map not majority

solvePt2 :: [String] -> Int
solvePt2 lines = o2 * co2
  where
    char2Int '1' = 1
    char2Int '0' = 0
    bitsToInt :: String -> Int
    bitsToInt = foldl (\acc x -> acc * 2 + char2Int x) 0
    chooseC02 (zeroes, ones) = if length zeroes <= length ones then zeroes else ones
    chooseO2 (zeroes, ones) = if length ones >= length zeroes then ones else zeroes
    segregate (zeroes, ones) ('1' : xs, l) = (zeroes, (xs, l) : ones)
    segregate (zeroes, ones) ('0' : xs, l) = ((xs, l) : zeroes, ones)
    magicFilter _ [(bits, l)] = bitsToInt l
    magicFilter choose lines =
      magicFilter choose $ choose $ foldl segregate ([], []) lines
    o2 = magicFilter chooseO2 (map (\x -> (x, x)) lines)
    co2 = magicFilter chooseC02 (map (\x -> (x, x)) lines)

main :: IO ()
main = do
  digits <- lines <$> readFile "./input.txt"
  _ <- print $ solvePt1 digits
  print $ solvePt2 digits
