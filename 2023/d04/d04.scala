import scala.io.Source
import scala.math.pow

@main def main() = {
    val inp: Array[String] = Source.fromFile("input.txt").mkString.split("\n")

    val winnerHands = inp.map(_.split(':')(1)
                               .split(" \\| ")
                               .map(_.split("\\s")
                                     .filter(_.nonEmpty).toSet))

    println(winnerHands.map(e => (e(0) & e(1)).toList.length)
                       .map(e => pow(2, e - 1).intValue)
                       .sum)
    
    val startingHand = List.range(0, inp.length)
                           .foldLeft(Map[Int, Int]())
                                    ((m, i) => m + (i -> 1))

    println(winnerHands
               .zipWithIndex
               .foldLeft(startingHand)
                        ((h, whi) =>
                            val winCount = (whi(0)(0) & whi(0)(1)).toList.length
                            List.range(whi(1) + 1, whi(1) + winCount + 1)
                                .foldLeft(h)((h, i) => h + (i -> (h(i) + h(whi(1))))))
               .values.sum)
}

