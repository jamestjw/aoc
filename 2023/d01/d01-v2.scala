import scala.io.Source

@main def main() = {
    val inp: Array[String] = Source.fromFile("input.txt").mkString.split("\n")

    def helper(l : List[Char]) : List[Char] = {
        l match {
            case 'o' :: 'n' :: 'e' :: _ => '1' :: helper(l.tail)
            case 't' :: 'w' :: 'o' :: _ => '2' :: helper(l.tail)
            case 't' :: 'h' :: 'r' :: 'e' :: 'e' :: _ => '3' :: helper(l.tail)
            case 'f' :: 'o' :: 'u' :: 'r' :: _ => '4' :: helper(l.tail)
            case 'f' :: 'i' :: 'v' :: 'e' :: _ => '5' :: helper(l.tail)
            case 's' :: 'i' :: 'x' :: _ => '6' :: helper(l.tail)
            case 's' :: 'e' :: 'v' :: 'e' :: 'n' :: _ => '7' :: helper(l.tail)
            case 'e' :: 'i' :: 'g' :: 'h' :: 't' :: _ => '8' :: helper(l.tail)
            case 'n' :: 'i' :: 'n' :: 'e' :: _ => '9' :: helper(l.tail)
            case  c :: _ => if c.isDigit then c :: helper(l.tail) else helper(l.tail)
            case Nil => List[Char]()
        }
    }

    println(inp.map(_.foldRight(List[Char]())
                               ((c,a) => if c.isDigit then c :: a else a))
               .map(l => List(l.head , l.last).mkString.toInt).sum)


    println(inp.map(_.toList).map(helper)
               .map(l => List(l.head , l.last).mkString.toInt).sum)
}

