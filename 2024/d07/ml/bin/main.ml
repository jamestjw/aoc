open Core

let is_ok targ operands fns =
  let rec is_ok' operands acc =
    match operands with
    | [] -> acc = targ
    | o :: os -> List.exists ~f:(fun fn -> is_ok' os (fn acc o)) fns
  in
  is_ok' (List.tl_exn operands) (List.hd_exn operands)

let concat x y = int_of_string (Printf.sprintf "%d%d" x y)

let solve inp fns =
  List.filter ~f:(fun (targ, args) -> is_ok targ args fns) inp
  |> List.fold ~f:(fun acc (targ, _) -> acc + targ) ~init:0

let () =
  let input_rows =
    In_channel.create @@ Array.get (Sys.get_argv ()) 1
    |> In_channel.input_all |> String.split_lines
    |> List.map ~f:(Str.split (Str.regexp {|: \| |}))
    |> List.map ~f:(function
         | fst :: rest -> (int_of_string fst, List.map ~f:int_of_string rest)
         | _ -> failwith "")
  in

  Printf.printf "%d %d"
    (solve input_rows [ ( + ); ( * ) ])
    (solve input_rows [ ( + ); ( * ); concat ])
