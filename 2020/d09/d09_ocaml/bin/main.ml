open Core
module IntMap = Map.Make (Int)

let mk_counts l =
  let rec aux l acc =
    match l with
    | [] -> acc
    | x :: xs ->
        aux xs
        @@ Map.add_exn ~key:x
             ~data:(1 + (Map.find acc x |> Option.value ~default:0))
             acc
  in
  aux l IntMap.empty

let part1 preamble nums =
  let two_sum counts target =
    List.fold_until (Map.keys counts) ~init:false
      ~f:(fun acc key ->
        let other = target - key in
        match Map.find counts other with
        | Some 1 when other = key -> Continue acc
        | Some _ -> Stop true
        | None -> Continue acc)
      ~finish:(fun x -> x)
  in

  let rec aux nums preamble =
    match nums with
    | [] -> failwith "whoops"
    | num :: nums ->
        if two_sum (mk_counts preamble) num then
          aux nums (List.tl_exn preamble @ [ num ])
        else num
  in

  aux nums preamble

let part2 nums target =
  let rec trim l =
    if List.fold ~f:( + ) ~init:0 l > target then trim @@ List.tl_exn l else l
  in
  List.fold_until nums ~init:[]
    ~f:(fun acc num ->
      let new_acc = acc @ [ num ] in
      let sum = List.fold ~f:( + ) ~init:0 new_acc in
      if sum = target then
        if List.length new_acc >= 2 then Stop new_acc else Continue new_acc
      else if sum > target then
        let new_acc = trim new_acc in
        if List.fold ~f:( + ) ~init:0 new_acc = target then Stop new_acc
        else Continue new_acc
      else Continue new_acc)
    ~finish:(fun x -> x)

let () =
  let input_nums =
    In_channel.create @@ Array.get (Sys.get_argv ()) 1
    |> In_channel.input_all |> String.split_lines |> List.map ~f:Int.of_string
  in
  let n = Array.get (Sys.get_argv ()) 2 |> Int.of_string in
  let preamble, nums = List.split_n input_nums @@ (n + 1) in
  let invalid_number = part1 preamble nums in
  let contiguous_set = part2 input_nums invalid_number in

  Fmt.pr "Invalid number %d@." invalid_number;
  Fmt.pr "Answer: %d@."
    (List.fold ~f:Int.min ~init:Int.max_value contiguous_set
    + List.fold ~f:Int.max ~init:Int.min_value contiguous_set)
