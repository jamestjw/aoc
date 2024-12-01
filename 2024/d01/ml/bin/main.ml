open Core
module IntMap = Stdlib.Map.Make (Int)

let () =
  let input_nums =
    In_channel.create @@ Array.get (Sys.get_argv ()) 1
    |> In_channel.input_all |> String.split_lines
    |> List.map ~f:(Str.split (Str.regexp "[ ]+"))
    |> List.map ~f:(function
         | [ e1; e2 ] -> (int_of_string e1, int_of_string e2)
         | _ -> failwith "oops")
  in
  let left, right = List.unzip input_nums in
  let left = List.sort left ~compare:Int.compare in
  let right = List.sort right ~compare:Int.compare in
  let part1 =
    List.zip_exn left right
    |> List.map ~f:(fun (l, r) -> Int.abs (l - r))
    |> List.fold ~f:( + ) ~init:0
  in
  let counter =
    List.fold ~init:IntMap.empty
      ~f:(fun map i ->
        IntMap.add i
          (IntMap.find_opt i map |> Option.value ~default:0 |> Int.succ)
          map)
      right
  in
  let part2 =
    List.map
      ~f:(fun e -> e * (IntMap.find_opt e counter |> Option.value ~default:0))
      left
    |> List.fold ~f:( + ) ~init:0
  in
  Printf.printf "part1: %d\n" part1;
  Printf.printf "part2: %d\n" part2
