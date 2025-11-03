import scala.io.Source

@main def main() = {
    val inp: List[String] = Source.fromFile("input.txt").mkString.split("\n\n").toList
    //val inp: List[String] = Source.fromFile("smol.txt").mkString.split("\n\n").toList

    val draws: List[Int] = inp(0).split(',').toList.map(_.toInt)
    // Represent board as List[List[(String, Bool)]]
    type Board = List[List[(Int, Boolean)]]

    val boards: List[Board] =
      inp.tail.map(_.split("\n").toList.map(_.trim.split(raw"\s+").toList.map(_.toInt)))
              .map(_.map(_.map((_, false))))

    def hasWin(board: Board) =
      def isRowComplete(r: List[(Int, Boolean)]) : Boolean = {
        r.foldLeft(true)(_ && _(1))
      }

      List(board, board.transpose)
        .exists(_.foldLeft(false)((b, l) => b || isRowComplete(l)))

    
    def updateBoard(board: Board, draw: Int) : Board =
      board.map(_.map(e => if e(0) == draw then (draw, true) else e))

    
    var firstWinnerScore =
      draws.foldLeft((None : Option[(Int, Board)], boards))
                    ((a, draw) => a match {
                      case (Some(_), _) => a  
                      case (None, boards) =>
                        var newBoards = boards.map(updateBoard(_, draw))
                        var res = newBoards
                                    .foldLeft(None : Option[(Int, Board)])
                                             ((a, b) => if a.isDefined then
                                                         a 
                                                        else if hasWin(b) then
                                                         Some((draw, b))
                                                        else None) 
                        (res, newBoards)
                    })._1
           .map(sb => sb(0) * sb(1).map(_.filter(!_(1)).map(_(0)).sum).sum)

    var lastWinnerScore =
      draws.foldLeft((None : Option[(Int, Board)], boards))
                    ((a, draw) => a match {
                      case (Some(_), _) => a  
                      case (None, boards) =>
                        var newBoards = boards.map(updateBoard(_, draw))
                        var winBoards = newBoards.filter(hasWin)
                        var rest = newBoards.filterNot(hasWin)
                        var res = if rest.length == 0
                                  then Some((draw, winBoards.head))
                                  else None

                        (res, rest)
                    })._1
           .map(sb => sb(0) * sb(1).map(_.filter(!_(1)).map(_(0)).sum).sum)

    println((firstWinnerScore, lastWinnerScore))
}
