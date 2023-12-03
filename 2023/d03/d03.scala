import scala.io.Source

def collapseConsecutives(nums :Seq[Int]) =
  nums.foldRight((Int.MaxValue, List.empty[List[Int]])) {
    case (n, (prev, a::as)) if prev-n == 1 => (n, (n::a) :: as)
    case (n, ( _  , a))                => (n, List(n) :: a)
  }._2


@main def main() = {
    val inp: Array[String] = Source.fromFile("input.txt").mkString.split("\n")
    val num_rows = inp.length
    val num_cols = inp(0).length

    def getGearRange(coords: (Int, Int)) : List[(Int, Int)] =
      var offsets = List(-1, 0, 1)

      offsets.flatMap(i_offset => offsets.map(j_offset =>
                                (coords(0) + i_offset, coords(1) + j_offset)))
             .filter((i, j) => i >= 0 && i < num_rows &&
                               j >= 0 && i < num_cols && (i, j) != coords)
          

    val numbers = inp.map(_.zipWithIndex.filter(_(0).isDigit).map(_(1)))
                     .map(collapseConsecutives)

    
    val part1GearCoords: Array[(Int, Int)] =
      inp.map(_.zipWithIndex
               .filter((c, _) => !(c.isDigit || c == '.'))
               .map(_(1)))
         .zipWithIndex
         .flatMap((l, i) => l.map((i, _)))

    var part1 = part1GearCoords.map(getGearRange)
                               .flatMap(_.flatMap((i,j) =>
                                      numbers(i).filter(l => j >= l.head &&
                                                             j <= l.last)
                                                .map((i, _))))
                               .distinct
                               .map((row, indices) =>
                                      indices.map(inp(row)(_)).mkString.toInt)
                               .sum

    val part2GearCoords: Array[(Int, Int)] =
      inp.map(_.zipWithIndex
               .filter((c, _) => c == '*')
               .map(_(1)))
         .zipWithIndex
         .flatMap((l, i) => l.map((i, _)))
    
    val part2 = part2GearCoords.map(getGearRange)
                               .map(_.flatMap((i,j) =>
                                     numbers(i).filter(l => j >= l.head &&
                                                            j <= l.last)
                                               .map((i, _)))
                                    .distinct)
                              .filter(_.length == 2)
                              .map(_.map((row, indices) =>
                                             indices.map(i => inp(row)(i))
                                                    .mkString.toInt)
                                    .product)
                              .sum

    println((part1, part2))
}

