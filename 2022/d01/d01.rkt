#lang racket

(define file-contents (port->string (open-input-file "input.txt") #:close? #t))

(define elf-strings (string-split file-contents "\n\n"))

(define elf-calories (map
                      (lambda (elf)
                        (apply + (map string->number (string-split elf))))
                      elf-strings))

(module* main #f
  (begin
    (display (apply max elf-calories))
    (newline)
    (display (apply + (take (sort elf-calories >) 3)))))