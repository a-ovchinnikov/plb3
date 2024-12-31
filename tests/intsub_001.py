# Компиляция: ~1.635с, исполнение: ~2.057с
# Без необходимости не включать!
#> (intsub-works-when-signs-of-minuend-and-subtrachend-differ
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
#>        0 0 0   X 0  0 0  0 0  0 0  0 0   0 0  X 0  X 0  X 0  X 0   ; R
#> ;
#>        0 0 0   X 0  0 0  0 0  0 0  0 0   X 0  X 0  X 0  X 0  X 0 X 0...)
#> ;
#> (out "!!" "!!" "!!"  ; Section 1.
#>      "!!!!"          ; Section 2.
# > (out "!")  ; Section 1.
#> )

VAR("X, Y, R, EXPECTED", INT)
VAR("W")
PROG(
    # 1.
    # WORKS:
    INTSET(X, -1), INTSET(Y, 2), INTSET(EXPECTED, 3), SET(W, 0),
    INTSUB(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
    SET(W, NOT(INTPOSITIVE(X))), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 2), INTSET(Y, -1), INTSET(EXPECTED, -3), SET(W, 0),
    INTSUB(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
    SET(W, NOT(INTPOSITIVE(Y))), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 2), INTSET(Y, 5), INTSET(EXPECTED, 3), SET(W, 0),
    INTSUB(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 2), INTSET(Y, 2), INTSET(EXPECTED, 0), SET(W, 0),
    INTSUB(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    # 2.
    INTSET(X, 5), INTSET(Y, 12), INTSET(EXPECTED, 7), SET(W, 0),
    INTSUB(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 55), INTSET(Y, 122), INTSET(EXPECTED, 67), SET(W, 0),
    INTSUB(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 1), INTSET(Y, 100), INTSET(EXPECTED, 99), SET(W, 0),
    INTSUB(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 1), INTSET(Y, 10000), INTSET(EXPECTED, 9999), SET(W, 0),
    INTSUB(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
)
