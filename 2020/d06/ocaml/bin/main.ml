open Core
module CharSet = Stdlib.Set.Make (Char)

let () =
  let file_contents =
    In_channel.input_all (In_channel.create @@ (Sys.get_argv ()).(1))
  in
  let groups = Str.split (Str.regexp "\n\n") file_contents in

  let part1 () =
    let groups =
      List.map groups ~f:(fun g ->
          String.to_list g |> List.filter ~f:(fun c -> Char.is_alpha c))
    in

    let votes = List.map ~f:CharSet.of_list groups in

    Fmt.pr "Sum %d@." @@ List.fold ~init:0 ~f:( + )
    @@ List.map ~f:CharSet.cardinal votes
  in

  let part2 () =
    let votes =
      List.map groups ~f:(Str.split (Str.regexp "\n"))
      |> List.map ~f:(fun group ->
             match group with
             | [] -> 0
             | x :: xs ->
                 List.fold
                   ~init:(CharSet.of_list @@ String.to_list x)
                   ~f:(fun acc s ->
                     CharSet.inter acc @@ CharSet.of_list @@ String.to_list s)
                   xs
                 |> CharSet.cardinal)
    in

    Fmt.pr "Sum %d@." @@ List.fold ~init:0 ~f:( + ) votes
  in

  part1 ();
  part2 ()
