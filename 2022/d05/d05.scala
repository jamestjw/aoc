import scala.io.Source

@main def main() = {
    val inp: Array[String] = Source.fromFile("input.txt").mkString.split("\n\n")
    val layout = inp(0).split("\n").reverse.tail.map(x => x.tail.grouped(4).map(_.head).toList).toList
    val stacks_p1 = (for (i <- 0 until layout(0).length) yield layout.map(_(i)).filter(_ != ' ')).toArray
    val stacks_p2 = Array(stacks_p1: _*)
    
    val movements = inp(1).split("\n").toList

    for (movement <- movements) {
        val s = movement.split(" ")
        val counts = s(1).toInt
        val src = s(3).toInt - 1
        val dest = s(5).toInt - 1

        stacks_p1(dest) = stacks_p1(dest) ++ stacks_p1(src).takeRight(counts).reverse
        stacks_p1(src) = stacks_p1(src).dropRight(counts)

        stacks_p2(dest) = stacks_p2(dest) ++ stacks_p2(src).takeRight(counts)
        stacks_p2(src) = stacks_p2(src).dropRight(counts)
    }

    println(stacks_p1.map(_.last).mkString)
    println(stacks_p2.map(_.last).mkString)
}