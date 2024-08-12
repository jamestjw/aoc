open Core
open Str

let () =
  let parse_dict txt =
    let kvs = Str.split (Str.regexp "[ |\n]") txt in
    List.fold
      ~init:(Hashtbl.create (module String))
      ~f:(fun ht kvs ->
        match String.split ~on:':' kvs with
        | [ key; value ] ->
            ignore @@ Hashtbl.add ht ~key ~data:value;
            ht
        | _ -> assert false)
      kvs
  in
  let is_passport_valid_pt1 passport =
    let required_fields =
      [
        "byr";
        "iyr";
        "eyr";
        "hgt";
        "hcl";
        "ecl";
        "pid";
        (* "cid"  *)
        (* its fine to not have cid:*)
      ]
    in
    List.fold ~init:true
      ~f:(fun acc field ->
        match Hashtbl.find passport field with Some _ -> acc | None -> false)
      required_fields;
  in

  let is_passport_valid_pt2 passport =
    let tests =
      [
        ( "byr",
          fun year ->
            let year = int_of_string year in
            year >= 1920 && year <= 2002 );
        ( "iyr",
          fun year ->
            let year = int_of_string year in
            year >= 2010 && year <= 2020 );
        ( "eyr",
          fun year ->
            let year = int_of_string year in
            year >= 2020 && year <= 2030 );
        ( "hgt",
          fun h ->
            if Str.string_match (Str.regexp {|\([0-9]+\)\([a-z]+\)|}) h 0 then
              let value = Str.matched_group 1 h |> int_of_string in
              let unit = Str.matched_group 2 h in

              match unit with
              | "cm" when value >= 150 && value <= 193 -> true
              | "in" when value >= 59 && value <= 76 -> true
              | _ -> false
            else false );
        ( "hcl",
          fun h ->
            Str.string_match (Str.regexp {|#\([0-9\|a-f]+\)|}) h 0
            && String.length (Str.matched_group 1 h) = 6 );
        ( "ecl",
          function
          | "amb" | "blu" | "brn" | "gry" | "grn" | "hzl" | "oth" -> true
          | _ -> false );
        ( "pid",
          fun h ->
            Str.string_match (Str.regexp {|\([0-9]+\)|}) h 0
            && String.length (Str.matched_group 1 h) = 9 );
      ]
    in
    List.fold ~init:true
      ~f:(fun acc (field, test) ->
        match Hashtbl.find passport field with
        | Some h -> acc && test h
        | None -> false)
      tests
  in
  let input_text =
    In_channel.input_all (In_channel.create @@ Array.get (Sys.get_argv ()) 1)
  in
  let docs = Str.split (Str.regexp "\n\n") input_text in
  let passports = List.map ~f:parse_dict docs in
  Printf.printf "Part1: %d\n"
    (List.filter passports ~f:is_passport_valid_pt1 |> List.length);

  Printf.printf "Part2: %d\n"
    (List.filter passports ~f:is_passport_valid_pt2 |> List.length)
