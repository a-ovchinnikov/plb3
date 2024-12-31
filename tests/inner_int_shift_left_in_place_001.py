#> (**ints-can-be-multiplied-by-ten
#> ;                               1  1 1   1 1  1 1  1 1  1 2  2 2
#> ;      0 1 2   3 4  5 6  7 8  9 0  1 2   3 4  5 6  7 8  9 0  1 2
#> ;      ---------------------------------------------------------
#>  (mem  0 0 0   0 0  0 0  0 0  0 0  0 0   0 0  X 0  X 0  X 0  X 0
#>        0 0 0   0 0  0 0  0 0  0 0  0 0   0 0  X 0  X 0  X 0  X 0 X 0...)
#>  (out "!!!!!"
#> ))


VAR("X, EXPECTED", INT)
VAR("W")
PROG(
    INTSET(X, 10), INTSET(EXPECTED, 100),
    _int_shift_left_in_place(X),
    SET(W, INTEQ(X, EXPECTED)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 1), INTSET(EXPECTED, 10), SET(W, 0),
    _int_shift_left_in_place(X),
    SET(W, INTEQ(X, EXPECTED)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 11), INTSET(EXPECTED, 110), SET(W, 0),
    _int_shift_left_in_place(X),
    SET(W, INTEQ(X, EXPECTED)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 101), INTSET(EXPECTED, 1010), SET(W, 0),
    _int_shift_left_in_place(X),
    SET(W, INTEQ(X, EXPECTED)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 1), INTSET(EXPECTED, 100), SET(W, 0),
    _int_shift_left_in_place(X),
    _int_shift_left_in_place(X),
    SET(W, INTEQ(X, EXPECTED)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
)
