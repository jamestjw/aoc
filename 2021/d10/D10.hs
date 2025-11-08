import Data.List (sort)
import Data.Maybe (isNothing)

findCorrupted :: String -> Maybe Char
findCorrupted = inner []
  where
    inner stack ps = case (stack, ps) of
      (_, []) -> Nothing
      (_, paren : parens) | paren `elem` ['{', '(', '<', '['] -> inner (paren : stack) parens
      ('{' : stack, '}' : ps) -> inner stack ps
      ('<' : stack, '>' : ps) -> inner stack ps
      ('[' : stack, ']' : ps) -> inner stack ps
      ('(' : stack, ')' : ps) -> inner stack ps
      (_, illegal : _) -> Just illegal

findMissing :: String -> [Char]
findMissing = inner []
  where
    inner stack ps = case (stack, ps) of
      (_, []) -> stack
      (_, paren : parens) | paren `elem` ['{', '(', '<', '['] -> inner (paren : stack) parens
      ('{' : stack, '}' : ps) -> inner stack ps
      ('<' : stack, '>' : ps) -> inner stack ps
      ('[' : stack, ']' : ps) -> inner stack ps
      ('(' : stack, ')' : ps) -> inner stack ps

scoreCorrupted :: Maybe Char -> Int
scoreCorrupted (Just ')') = 3
scoreCorrupted (Just ']') = 57
scoreCorrupted (Just '}') = 1197
scoreCorrupted (Just '>') = 25137
scoreCorrupted _ = 0

scoreMissing :: [Char] -> Int
scoreMissing = foldl (\acc c -> acc * 5 + charScore c) 0
  where
    charScore '(' = 1
    charScore '[' = 2
    charScore '{' = 3
    charScore '<' = 4

main :: IO ()
main = do
  inps <- lines <$> readFile "input.txt"
  let pt1 = sum $ map (scoreCorrupted . findCorrupted) inps
  let pt2Scores = scoreMissing . findMissing <$> filter (isNothing . findCorrupted) inps
  let pt2 = sort pt2Scores !! (length pt2Scores `div` 2)
  print (pt1, pt2)
