run :: [String] -> a -> (a -> String -> Int -> a) -> (a -> Int) -> Int
run strs init move final = final $ foldl step init strs
  where
    step state str = case words str of
      [cmd, d] -> move state cmd (read d)

pt1 :: [String] -> Int
pt1 strs = run strs (0, 0) move (uncurry (*))
  where
    move (h, v) cmd offset =
      case cmd of
        "forward" -> (h + offset, v)
        "up" -> (h, v - offset)
        "down" -> (h, v + offset)

pt2 :: [String] -> Int
pt2 strs = run strs (0, 0, 0) move (\(h, v, _) -> h * v)
  where
    move (h, v, aim) cmd offset =
      case cmd of
        "forward" -> (h + offset, v + aim * offset, aim)
        "up" -> (h, v, aim - offset)
        "down" -> (h, v, aim + offset)

main :: IO ()
main = do
  inp <- lines <$> readFile "./input.txt"
  print $ pt1 inp
  print $ pt2 inp
