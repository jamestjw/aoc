{-# OPTIONS_GHC -Wno-incomplete-uni-patterns #-}

module Main where

import Data.List (find, partition, transpose)
import Data.List.Split (splitOn)

type Bingo = [[(Int, Bool)]]

hasWon :: Bingo -> Bool
hasWon bingo = hasWinningRow bingo || hasWinningRow (transpose bingo)
  where
    hasWinningRow = any (all snd)

mark :: Int -> Bingo -> Bingo
mark v bingo = [[(if v == c then (c, True) else (c, marked)) | (c, marked) <- row] | row <- bingo]

score :: Bingo -> Int -> Int
score bingo final = total * final
  where
    total = sum $ concat [[y | (y, marked) <- row, not marked] | row <- bingo]

pt1 :: [Bingo] -> [Int] -> Int
pt1 bingos draws =
  let d : ds = draws
      newBingos = map (mark d) bingos
   in ( case find hasWon newBingos of
          Just bingo -> score bingo d
          _ -> pt1 newBingos ds
      )

pt2 :: [Bingo] -> [Int] -> Int
pt2 bingos draws =
  let d : ds = draws
      newBingos = map (mark d) bingos
      (won, haventWon) = partition hasWon newBingos
   in ( case (won, haventWon) of
          ([bingo], []) -> score bingo d
          _ -> pt2 haventWon ds
      )

main :: IO ()
main = do
  inp <- readFile "./input.txt"
  let drawStrs : bingoStrs = splitOn "\n\n" inp
      draws :: [Int]
      draws = read <$> splitOn "," drawStrs
      bingoStrings = map words <$> map lines bingoStrs
      bingos :: [[[(Int, Bool)]]]
      bingos = (map . map . map) (\x -> (read x, False)) bingoStrings
  print $ pt1 bingos draws
  print $ pt2 bingos draws
