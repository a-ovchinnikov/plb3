# Компиляция: ~1.635с, исполнение: ~2.057с
# Без необходимости не включать!
#> (intsub-works-when-signs-of-minuend-and-subtrachend-match
#> ;                               1  1 1   1 1  1 1  1 1  1 2  2 2
#> ;      0 1 2   3 4  5 6  7 8  9 0  1 2   3 4  5 6  7 8  9 0  1 2
#> ;      ---------------------------------------------------------
#>   (mem 0 0 0   X 0  0 0  0 0  0 0  0 0   X 0  0 0  X 0  X 0  X 0   ; X
#> ;
#> ;      2 2 2   2 2  2 2  3 3  3 3  3 3   3 3  3 3  4 4  4 4  4 4
#> ;      3 4 5   6 7  8 9  0 1  2 3  4 5   6 7  8 9  0 1  2 3  4 5
#> ;      ---------------------------------------------------------
#>        0 0 0   X 0  0 0  0 0  0 0  0 0   X 0  0 0  X 0  X 0  X 0   ; Y
#> ;
#> ;      4 4 4   4 5  5 5  5 5  5 5  5 5   5 6  6 6  6 6  6 6  6 6
#> ;      6 7 8   9 0  1 2  3 4  5 6  7 8   9 0  1 2  3 4  5 6  7 8
#> ;      ---------------------------------------------------------
#>        0 0 0   1 0  0 0  0 0  0 0  0 0   0 0  0 0  0 0  0 0  1 0   ; R
# >        0 0 0   1 0  0 0  0 0  0 0  0 0   X 0  X 0  X 0  X 0  X 0   ; R
#> ;
#>        0 0 0   X 0  0 0  0 0  0 0  0 0   X 0  X 0  X 0  X 0  X 0 X 0...)
#> ;
#> (out "!!"  ; Section 1.
#>      "!!"  ; Section 2.
#> )
#> )

VAR("X, Y, R, EXPECTED", INT)
VAR("W")
PROG(
    # 1.
    INTSET(X, 3), INTSET(Y, 2), INTSET(EXPECTED, -1), SET(W, 0),
    INTSUB(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 14), INTSET(Y, 2), INTSET(EXPECTED, -12), SET(W, 0),
    INTSUB(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    # 2.
    INTSET(X, -3), INTSET(Y, -2), INTSET(EXPECTED, 1), SET(W, 0),
    INTSUB(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, -2), INTSET(Y, -3), INTSET(EXPECTED, -1), SET(W, 0),
    INTSUB(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
)
