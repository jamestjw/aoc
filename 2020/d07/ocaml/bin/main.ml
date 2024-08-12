open Angstrom
open Core

let whitespace = skip_while Char.is_whitespace

let words =
  take_while (function 'a' .. 'z' -> true | ' ' -> true | _ -> false)

(* Helper function to parse a specific word *)
let word w = string w *> skip_many (char ' ')

(* Parser for a single bag description *)
let bag_color =
  many1 (satisfy (function 'a' .. 'z' | ' ' -> true | _ -> false))
  >>| String.of_char_list

let line_parse =
  (* let* bag_name = words *> string "bags" in *)
  let* bag_name = bag_color in
  (* let* _ = whitespace *> string "bags" in *)
  return bag_name

let parse_line line =
  match parse_string ~consume:Prefix line_parse line with
  | Ok res -> res
  | Error err -> Fmt.failwith "whoops: %s" err

let () =
  let lines =
    In_channel.input_all @@ In_channel.create @@ Array.get (Sys.get_argv ()) 1
  in
  List.iter ~f:(fun line ->
    Fmt.pr "Doing line: %s@." line; print_endline @@ parse_line line)
  @@ String.split_lines lines
