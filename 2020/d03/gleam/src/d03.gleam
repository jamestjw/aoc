import argv
import gleam/dict
import gleam/int
import gleam/io
import gleam/list
import gleam/result
import gleam/string
import simplifile.{read}

pub fn main() {
  let fname = case argv.load().arguments {
    [fname] -> fname
    _ -> panic
  }
  let assert Ok(contents) = read(from: fname)
  let lines = string.trim(contents) |> string.split("\n")
  let num_rows = list.length(lines)
  let num_cols = string.length(list.first(lines) |> result.unwrap(""))
  io.println("Num rows: " <> int.to_string(num_rows))
  io.println("Num cols: " <> int.to_string(num_cols))

  let data =
    list.index_fold(lines, dict.new(), fn(d, str, i) {
      string.to_graphemes(str)
      |> list.index_fold(d, fn(d, ch, j) {
        // io.println("Inserting to (" <> int.to_string(i) <> ", " <> int.to_string(j) <> ")")
        dict.insert(d, #(i, j), ch)
      })
    })
  part1(0, 0, 1, 3, 0, num_rows, num_cols, data)
  |> int.to_string()
  |> io.println()

  part2(num_rows, num_cols, data)
  |> int.to_string()
  |> io.println()
}

// i goes down
// j goes right
fn part1(i: Int, j: Int, di, dj, score: Int, num_rows: Int, num_cols: Int, data) {
  case i {
    // If we surpass the bottom row
    _ if i >= num_rows -> score
    _ -> {
      let j = j % num_cols
      let score = case dict.get(data, #(i, j)) {
        Ok(res) if res == "#" -> score + 1
        Ok(_) -> score
        Error(_) -> {
          io.println("i: " <> int.to_string(i) <> " j: " <> int.to_string(j))
          panic
        }
      }
      part1(i + di, j + dj, di, dj, score, num_rows, num_cols, data)
    }
  }
}

fn part2(num_rows, num_cols, data) {
  let offsets = [#(1, 1), #(1, 3), #(1, 5), #(1, 7), #(2, 1)]
  list.map(offsets, fn(pair) {
    let #(di, dj) = pair

    part1(0 + di, 0 + dj, di, dj, 0, num_rows, num_cols, data)
  })
  |> list.fold(1, fn(acc, i) { acc * i })
}
