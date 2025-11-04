{-# LANGUAGE OverloadedStrings #-}

import Data.Map.Strict qualified as M
import Data.Text qualified as T

grow :: M.Map Int Int -> M.Map Int Int
grow = M.foldlWithKey f M.empty
  where
    f m lifespan cnt = case lifespan of
      0 -> M.insert 6 cnt $ M.insert 8 cnt m
      _ -> M.insertWith (+) (lifespan - 1) cnt m

simulate time inp = M.foldl (+) 0 $ iterate grow m !! time
  where
    m = foldl (\m v -> M.insertWith (+) v 1 m) M.empty inp

main :: IO ()
main = do
  inp <- readFile "input.txt"
  let start :: [Int] = read . T.unpack <$> T.splitOn "," (T.pack inp)
  print $ simulate 80 start
  print $ simulate 256 start
