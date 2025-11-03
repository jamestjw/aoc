{-# LANGUAGE OverloadedStrings #-}

import Data.Map.Strict qualified as M
import Data.Text qualified as T

parseRow :: String -> (Int, Int, Int, Int)
parseRow row =
  let [x1, y1, x2, y2] = map T.unpack $ T.splitOn "," $ T.replace " -> " "," (T.pack row)
   in (read x1, read y1, read x2, read y2)

run :: [(Int, Int, Int, Int)] -> ((Int, Int, Int, Int) -> Bool) -> Int
run coords coordsFilter = length $ filter (1 <) $ M.elems $ foldl doRow M.empty coords
  where
    mkGenerator i1 i2 =
      if i1 == i2
        then repeat i1
        else [i1, i1 + step .. i2]
      where
        step = if i2 > i1 then 1 else -1
    doRow grid (x1, y1, x2, y2) =
      if coordsFilter (x1, y1, x2, y2)
        then
          foldl (\grid (x, y) -> M.insertWith (+) (x, y) 1 grid) grid $ zip (mkGenerator x1 x2) (mkGenerator y1 y2)
        else grid

pt1 coords = run coords (\(x1, y1, x2, y2) -> (x1 == x2) || (y1 == y2))

pt2 coords = run coords (const True)

main :: IO ()
main = do
  rows <- map parseRow . lines <$> readFile "./input.txt"
  print $ pt1 rows
  print $ pt2 rows
