import scala.io.Source
import scala.math._

def findMinMax(time: Long, distance: Long) =
  val tmp = sqrt(pow(time.toDouble, 2)/4 - distance)
  val minTime = (0.5 * time - tmp).ceil.toLong
  val maxTime = (0.5 * time + tmp).floor.toLong
  (minTime, maxTime)
    
@main def main() = {
    val inp: Array[String] = Source.fromFile("input.txt").mkString.split("\n")
    val digits = inp.map(raw"\d+".r.findAllIn(_).toList)
    val timeStrs = digits(0)
    val distanceStrs = digits(1)
    val times = timeStrs.map(_.toInt)
    val distances = distanceStrs.map(_.toInt)
    val combinedTime = timeStrs.mkString.toLong
    val combinedDistance = distanceStrs.mkString.toLong
    val combinedMinMax = findMinMax(combinedTime, combinedDistance)

    println(times.zip(distances)
                 .map((time, distance) =>
                        val minMax = findMinMax(time, distance)
                        minMax(1) - minMax(0) + 1)
                 .product)

    println(combinedMinMax(1) - combinedMinMax(0) + 1)
}

