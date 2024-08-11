let () =
  let lines = In_channel.input_lines (open_in Sys.argv.(1)) in
  let numbers = List.map int_of_string lines in
  let tbl = Hashtbl.create 0 in

  (* Part 1 *)
  List.iter
    (fun num ->
      let required = 2020 - num in
      match Hashtbl.find_opt tbl required with
      | Some _ ->
          print_int @@ (required * num);
          exit 0
      | None -> Hashtbl.add tbl num true)
    numbers
