import scala.io.Source

@main def main() = {
    val constraints = Map("red" -> 12, "green" -> 13, "blue" -> 14)

    val inp: Array[String] = Source.fromFile("input.txt").mkString.split("\n")
    val colorCountRegex = raw"(\d+)\s+(\w+)".r
    val colorCounts =
      inp.map(colorCountRegex.findAllMatchIn(_)
                             .collect(m => (m.group(1).toInt, m.group(2)))
                             .toList)
    
    val pt1 = colorCounts.map(_.foldLeft(true)
                                        ((a, p) => a &&
                                                   p(0) <= constraints(p(1))))
                         .zipWithIndex.filter(_(0)).map(_(1) + 1).sum

    val pt2 = colorCounts.map(_.groupMapReduce(_(1))(_(0))(_.max(_)))
                         .map(_.values.product).sum

    println((pt1, pt2))
}

