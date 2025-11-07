{-# LANGUAGE OverloadedStrings #-}

import Data.Text qualified as T

calculate :: [Int] -> (Int -> Int -> Int) -> Int
calculate xs distanceFn = minimum distances
  where
    candidates = [(minimum xs) .. (maximum xs)]
    distances = map (\c -> sum $ map (distanceFn c) xs) candidates

arithSum x y = diff * (diff + 1) `div` 2
  where
    diff = abs $ x - y

main :: IO ()
main = do
  xs :: [Int] <- map (read . T.unpack) . T.splitOn "," . T.pack <$> getLine
  print $ calculate xs (\x y -> abs $ x - y)
  print $ calculate xs arithSum
