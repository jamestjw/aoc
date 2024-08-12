open Angstrom
open Core

let whitespace = skip_while Char.is_whitespace
let words = take_while Char.is_alpha

let line_parse =
  let* op = words <* whitespace in
  let* sign = char '+' <|> char '-' in
  let* value = take_while Char.is_digit in
  return (op, int_of_string value * if Char.equal sign '-' then -1 else 1)

let parse_line line =
  match parse_string ~consume:Prefix line_parse line with
  | Ok res -> res
  | Error err -> Fmt.failwith "whoops: %s" err

let empty = Map.empty (module Int)

let () =
  let lines =
    In_channel.input_all @@ In_channel.create @@ Array.get (Sys.get_argv ()) 1
  in
  let ops =
    List.map ~f:parse_line (String.split_lines lines) |> Array.of_list
  in

  let pt1 () =
    let rec loop acc visited idx =
      match Map.find visited idx with
      | Some _ -> acc
      | None ->
          let op, value = Array.get ops idx in
          let new_acc, new_idx =
            match op with
            | "nop" -> (acc, idx + 1)
            | "jmp" -> (acc, idx + value)
            | "acc" -> (acc + value, idx + 1)
            | op -> Fmt.failwith "Invalid operator %s?" op
          in
          loop new_acc (Map.add_exn visited ~key:idx ~data:true) new_idx
    in
    loop 0 empty 0
  in

  let pt2 () =
    let rec loop ops acc visited idx =
      if idx = Array.length ops then Some acc
      else
        match Map.find visited idx with
        | Some _ -> None
        | None ->
            let op, value = Array.get ops idx in
            let new_acc, new_idx =
              match op with
              | "nop" -> (acc, idx + 1)
              | "jmp" -> (acc, idx + value)
              | "acc" -> (acc + value, idx + 1)
              | op -> Fmt.failwith "Invalid operator %s?" op
            in
            loop ops new_acc (Map.add_exn visited ~key:idx ~data:true) new_idx
    in
    let changeable =
      Array.filter_mapi ops ~f:(fun i (op, _) ->
          match op with "nop" | "jmp" -> Some i | _ -> None)
      |> List.of_array
    in
    let rec compute candidates =
      match candidates with
      | [] -> Fmt.failwith "Exhausted all options@."
      | idx :: rest -> (
          let ops = Array.copy ops in
          let op, value = Array.get ops idx in
          let new_op = if String.equal op "nop" then "jmp" else "nop" in
          Array.set ops idx (new_op, value);
          match loop ops 0 empty 0 with Some e -> e | None -> compute rest)
    in
    compute changeable
  in
  Fmt.pr "Pt1: %d@." @@ pt1 ();
  Fmt.pr "Pt2: %d@." @@ pt2 ();
  Fmt.pr "Done."
