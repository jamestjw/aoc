import scala.io.Source

def findMarker(s: String, packetLen: Int, msgLen: Int) : Unit = {
    val packet = s.sliding(packetLen).indexWhere { elem => elem.distinct.length == packetLen } + packetLen
    val msg = s.substring(packet)
                .sliding(msgLen)
                .indexWhere { elem => elem.distinct.length == msgLen }
                + packet + msgLen
    
    println(s"$packet $msg")
}

@main def main() = {
    val inp: Array[String] = Source.fromFile("input.txt").mkString.split("\n")

    inp.foreach(findMarker(_, 4, 14))
}
