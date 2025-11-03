import scala.io.Source

@main def main() = {
    def bin2int(s : String) = Integer.parseInt(s, 2)
    def mostCommon(l : List[Char]) =
      l.groupMapReduce(identity)(_ => 1)(_+_).maxBy(_(1))._1

    def mostCommonRiggedFor1(l : List[Char]) =
      l.groupMapReduce(identity)(_ => 1)(_+_).maxBy(_.swap)._1

    def leastCommonRiggedFor0(l : List[Char]) =
      l.groupMapReduce(identity)(_ => 1)(_+_).minBy(_.swap)._1

    val inp: List[List[Char]] = Source.fromFile("input.txt").mkString.split("\n")
                                      .toList.map(_.toList).transpose

    var bits = inp.map(mostCommon)
    
    var gamma = bin2int(bits.mkString)
    var eps = bin2int(bits.map(e => if e == '0' then '1' else '0').mkString)

    var o2bits = List.range(0, inp.length)
                     .foldLeft(inp.transpose)
                              ((l, i) =>
                                 if l.length <= 1 then l
                                 else l.filter(_(i) == mostCommonRiggedFor1(l.map(_(i)))))

    var co2bits = List.range(0, inp.length)
                      .foldLeft(inp.transpose)
                               ((l, i) =>
                                  if l.length <= 1 then l
                                  else l.filter(_(i) == leastCommonRiggedFor0(l.map(_(i)))))

    println(gamma * eps)

    println(bin2int(o2bits.head.mkString) * bin2int(co2bits.head.mkString))
}
