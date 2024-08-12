open Core

let do_binary (left, right) left_ch right_ch ch =
  if Char.equal left_ch ch then (left, (left + right) / 2)
  else if Char.equal right_ch ch then (1 + ((left + right) / 2), right)
  else assert false

let () =
  let inp = In_channel.read_lines (Sys.get_argv ()).(1) in
  let seat_ids =
    List.map
      ~f:(fun line ->
        let row_str = String.slice line 0 7 in
        let col_str = String.slice line 7 10 in
        let row_left, row_right =
          List.fold ~init:(0, 127)
            ~f:(fun range ch -> do_binary range 'F' 'B' ch)
            (String.to_list row_str)
        in
        assert (row_left = row_right);

        let col_left, col_right =
          List.fold ~init:(0, 7)
            ~f:(fun range ch -> do_binary range 'L' 'R' ch)
            (String.to_list col_str)
        in
        assert (col_left = col_right);
        let seat_id = (row_left * 8) + col_left in
        seat_id)
      inp
  in
  let max_seat_id = List.fold ~init:0 ~f:Int.max seat_ids in
  Fmt.pr "Max seat ID is %d@." max_seat_id;

  let sorted_ids = List.sort ~compare seat_ids in
  List.zip_exn (List.drop_last_exn sorted_ids) (List.tl_exn sorted_ids)
  |> List.iter ~f:(fun (i1, i2) ->
         if i2 - i1 <> 1 then Fmt.pr "(%d,%d)@." i1 i2)
