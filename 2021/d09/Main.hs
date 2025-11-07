import Data.Char (digitToInt)
import Data.List (sort)
import Data.Set qualified as Set

type Grid = [[Int]]

type Coords = (Int, Int)

type Queue = [Coords]

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

foldQueue :: ((Queue, a) -> Coords -> (Queue, a)) -> a -> Queue -> a
foldQueue fn acc queue =
  case queue of
    [] -> acc
    c : cs ->
      let (newQueue, newAcc) = fn (cs, acc) c
       in foldQueue fn newAcc newQueue

neighborsOf :: Grid -> (Int, Int) -> [((Int, Int), Int)]
neighborsOf grid (i, j) =
  [ ((i2, j2), grid !! i2 !! j2)
    | (di, dj) <- directions,
      let i2 = i + di,
      let j2 = j + dj,
      0 <= i2,
      i2 < numRows,
      0 <= j2,
      j2 < numCols
  ]
  where
    numRows = length grid
    numCols = length $ head grid

findLows grid =
  [ ((i, j), here)
    | i <- [0 .. (numRows - 1)],
      j <- [0 .. (numCols - 1)],
      let neighbors = neighborsOf grid (i, j),
      let here = grid !! i !! j,
      all ((here <) . snd) neighbors
  ]
  where
    numRows = length grid
    numCols = length $ head grid

findBasinSize :: Grid -> Coords -> Int
findBasinSize grid low = length $ Set.fromList $ foldQueue doCoords [] [low]
  where
    doCoords (q, basin) (i, j) =
      let neighbors =
            [ neighbor
              | (neighbor, v) <- neighborsOf grid (i, j),
                v > grid !! i !! j,
                v /= 9
            ]
       in (neighbors ++ q, (i, j) : basin)

main :: IO ()
main = do
  grid <- map (map digitToInt) . lines <$> readFile "input.txt"
  let lows = findLows grid
  print . sum . map ((+ 1) . snd) $ lows
  print . product . take 3 . reverse . sort . map (findBasinSize grid . fst) $ lows
