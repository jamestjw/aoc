import scala.io.Source

@main def main() = {
    val inp: List[Int] = Source.fromFile("input.txt")
                               .mkString.split(",").toList
                               .map(_.toInt)

    
    def grow(fishes: Map[Int, Long]) : Map[Int, Long] =
      fishes.foldLeft(Map[Int, Long]().withDefaultValue(0L))
                     ((m, kv) => if kv(0) == 0
                                 then m + (8 -> (m(8) + kv(1)))
                                        + (6 -> (m(6) + kv(1)))
                                 else m + ((kv(0) - 1) ->
                                            (m(kv(0) - 1) + kv(1))))

    def fishForLifespan(timespan: Int) =
      List.range(0, timespan)
          .foldLeft(inp.foldLeft(Map[Int, Long]().withDefaultValue(0L))
                                ((m, v) => m + (v -> (m(v) + 1L))))
                   ((m, _) => grow(m))
 
    val eighty = fishForLifespan(80)
    val twofivesix = fishForLifespan(256)

    println(eighty.values.sum)
    println(twofivesix.values.sum)
}
