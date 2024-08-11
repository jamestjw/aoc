let print_list l = print_endline (String.concat ", " l)

let () =
  let parse_line line =
    match String.split_on_char ' ' line with
    | [ range; letter; data ] ->
        let range =
          match String.split_on_char '-' range with
          | [ left; right ] -> (int_of_string left, int_of_string right)
          | _ -> assert false
        in
        let letter =
          String.sub letter 0 1 |> String.to_seq |> List.of_seq |> List.hd
        in

        (range, letter, data)
    | _ -> assert false
  in
  let is_valid_pt1 ((left, right), letter, data) =
    let counts = Hashtbl.create 26 in
    List.iter
      (fun c ->
        match Hashtbl.find_opt counts c with
        | Some v -> Hashtbl.add counts c (v + 1)
        | None -> Hashtbl.add counts c 1)
      (String.to_seq data |> List.of_seq);
    let count = Hashtbl.find_opt counts letter |> Option.value ~default:0 in
    if count >= left && count <= right then 1 else 0
  in
  let is_valid_pt2 ((left, right), letter, data) =
    let xor a b = (a || b) && not (a && b) in
    let chars = String.to_seq data |> List.of_seq in
    if
      xor
        (List.nth chars (left - 1) == letter)
        (List.nth chars (right - 1) == letter)
    then 1
    else 0
  in
  let lines =
    In_channel.input_lines (open_in Sys.argv.(1)) |> List.map parse_line
  in
  print_int @@ List.fold_left (fun acc line -> acc + is_valid_pt1 line) 0 lines;
  print_newline ();
  print_int @@ List.fold_left (fun acc line -> acc + is_valid_pt2 line) 0 lines
