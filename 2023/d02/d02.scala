import scala.io.Source

@main def main() = {
    val constraints = Map("red" -> 12, "green" -> 13, "blue" -> 14)
    val empty = Map("red" -> 0, "green" -> 0, "blue" -> 0)

    val inp: Array[String] = Source.fromFile("input.txt").mkString.split("\n")

    val indices = inp.map(_.split(": ")(0).split(" ")(1).toInt)
    val games = inp.map(_.split(": ")(1))
                   .map(_.split("; ")
                   .map(_.replace(",","").split(" ")))
    val valid = games
                  .map(_.map(_.grouped(2)).flatten)
                  .map(_.foldLeft(true)
                                 ((a, l) => a &&
                                            l(0).toInt <= constraints(l(1))))

    println(indices.zip(valid).filter(_(1)).map(_.head).sum)

    println(games.map(_.foldLeft(empty)((a, g) =>
                        g.grouped(2)
                         .foldLeft(a)
                                  ((m, d) =>
                                     m + (d(1) -> m(d(1)).max(d(0).toInt)))))
                 .map(_.values.product)
                 .sum)
}

