import scala.io.Source

@main def main() = {
    val inp: Array[String] = Source.fromFile("input.txt").mkString.split("\n")

    val digits = Array("1", "2", "3", "4", "5", "6", "7", "8", "9")
    val words = Array("one", "two", "three", "four", "five", "six", 
                      "seven", "eight", "nine")
    val digitsAndWords = digits ++ words

    println(inp.map(l => digits.map(d => List((d, l.indexOf(d)),
                                              (d, l.lastIndexOf(d)))))
               .map(_.toList.flatten)
               .map(_.filter(_(1) >= 0)) // remove not founds
               .map(l => (l.minBy(_(1)), l.maxBy(_(1))))
               .map((p1, p2) => (p1(0) + p2(0)).toInt)
               .sum)

    println(inp.map(l => digitsAndWords.map(d => List((d, l.indexOf(d)),
                                                      (d, l.lastIndexOf(d)))))
               .map(_.toList.flatten)
               // words -> digits
               .map(_.map((d, i) => ((if d.length > 1 then
                                      digits(words.indexOf(d)) else d), i)))
               .map(_.filter(_(1) >= 0))
               .map(l => (l.minBy(_(1)), l.maxBy(_(1))))
               .map((p1, p2) => (p1(0) + p2(0)).toInt)
               .sum)
}

