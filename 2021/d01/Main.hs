main :: IO ()
main = do
  digits :: [Int] <- map read . lines <$> readFile "./input.txt"
  let triples = map (\(x, y, z) -> x + y + z) $ zip3 digits (tail digits) (tail $ tail digits)
  isIncreasing digits (tail digits)
  isIncreasing triples (tail triples)
  where
    isIncreasing l1 l2 = print $ length $ filter (uncurry (<)) $ zip l1 l2
