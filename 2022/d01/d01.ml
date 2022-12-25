let main =
  let read_file filename =
    let input_channel = open_in filename in
    let length = in_channel_length input_channel in
    let contents = really_input_string input_channel length in
    close_in input_channel;
    contents
  in
  let max_from_list l = List.fold_left max 0 l in
  let sum_list l = List.fold_left ( + ) 0 l in
  let take3 l =
    match l with a :: b :: c :: _ -> [ a; b; c ] | _ -> failwith "whoops!"
  in
  let f = read_file "input.txt" in
  let elves = Str.split (Str.regexp "\n\n") f in
  let calories =
    List.map
      (fun x -> List.map int_of_string (Str.split (Str.regexp "\n") x))
      elves
  in
  let sum_calories = List.map sum_list calories in
  let top3 = take3 (List.sort (fun x y -> y - x) sum_calories) in
  Printf.printf "%d\n" (max_from_list sum_calories);
  Printf.printf "%d\n" (sum_list top3)
