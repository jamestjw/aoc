import scala.io.Source

@main def main() = {
    val inp: Array[String] = Source.fromFile("d01_tests_input.txt").mkString.split("\n\n")
    val elfCalories = inp.map(_.split("\n").map(_.toInt).sum)

    println(elfCalories.max)
    println(elfCalories.sorted.reverse.take(3).sum)
}
