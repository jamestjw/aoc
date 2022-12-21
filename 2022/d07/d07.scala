import scala.io.Source
import scala.collection.mutable.HashMap

@main def main() = {
    val inp: Array[String] = Source.fromInputStream(System.in).mkString.split('\n')
    var cwd: List[String] = List[String]()
    val dirSizes: HashMap[List[String], Int] = new HashMap[List[String], Int]()

    for (line <- inp) {
        line.split(" ").toList match
            case "$" :: "cd" :: ".." :: Nil =>
                cwd = cwd.dropRight(1)
            case "$" :: "cd" :: dest :: Nil =>
                cwd = cwd :+ dest
            case "$" :: "ls" :: Nil => ()
            case "dir" :: dirname :: Nil => ()
            case size :: filename :: Nil =>
                for (i <- 0 until cwd.length) {
                  val d = cwd.dropRight(i)
                  dirSizes(d) = dirSizes.getOrElse(d, 0) + size.toInt
                }
            case e =>
                throw new Exception("Unexpected input");
    }

    val p1 = dirSizes.values.filter { x => x <= 100000 }.sum
    val rootSize = dirSizes.values.max
    val toDelete = rootSize - (70000000 - 30000000)
    val p2 = dirSizes.values.filter { x => x >= toDelete }.min

    println(p1)
    println(p2)
}
