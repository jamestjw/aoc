(* Function to find the three-sum *)
let three_sum nums target =
  let sorted_nums = List.sort compare nums in
  let rec find_triplets acc list =
    match list with
    | [] | [ _ ] | [ _; _ ] -> acc
    | x :: xs ->
        let rec find_pairs left right =
          if left >= right then acc
          else
            let sum = x + List.nth xs left + List.nth xs right in
            if sum = target then
              let triplet = (x, List.nth xs left, List.nth xs right) in
              find_pairs (left + 1) (right - 1) @ (triplet :: acc)
            else if sum < target then find_pairs (left + 1) right
            else find_pairs left (right - 1)
        in
        find_triplets (find_pairs 0 (List.length xs - 1)) xs
  in
  find_triplets [] sorted_nums

let _ =
  let lines = In_channel.input_lines (open_in Sys.argv.(1)) in
  let numbers = List.map int_of_string lines in
  let target = 2020 in
  let tbl = Hashtbl.create 0 in

  (* Part 1 *)
  List.iter
    (fun num ->
      let required = target - num in
      match Hashtbl.find_opt tbl required with
      | Some _ -> Fmt.pr "Part 1: %d@." @@ (required * num)
      | None -> Hashtbl.add tbl num true)
    numbers;
  (* Part 2
     Sort the integers and run three-sum *)
  let x, y, z = List.hd @@ three_sum numbers target in
  Fmt.pr "Part 2: %d@." (x * y * z)
