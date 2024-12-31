#> (**ints-can-be-divided-by-ten
#> ;                               1  1 1   1 1  1 1  1 1  1 2  2 2
#> ;      0 1 2   3 4  5 6  7 8  9 0  1 2   3 4  5 6  7 8  9 0  1 2
#> ;      ---------------------------------------------------------
#>  (mem  0 0 0   X 0  0 0  0 0  0 0  0 0   0 0  0 0  0 0  X 0  X 0
#>        0 0 0   X 0  0 0  0 0  0 0  0 0   0 0  X 0  X 0  X 0  X 0 X 0...)
# >  (out "!!!!!"
#>  (out "!!!!!"
#> ))


VAR("X, EXPECTED", INT)
VAR("W")
PROG(
    INTSET(X, 10), INTSET(EXPECTED, 1),
    _int_shift_right_in_place(X),
    SET(W, INTEQ(X, EXPECTED)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 100), INTSET(EXPECTED, 10),
    _int_shift_right_in_place(X),
    SET(W, INTEQ(X, EXPECTED)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, -100), INTSET(EXPECTED, -10),
    _int_shift_right_in_place(X),
    SET(W, INTEQ(X, EXPECTED)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    # TODO: > (add-expected (out "!"))
    INTSET(X, -101), INTSET(EXPECTED, -10),
    _int_shift_right_in_place(X),
    SET(W, INTEQ(X, EXPECTED)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 1), INTSET(EXPECTED, 0),
    _int_shift_right_in_place(X),
    SET(W, INTEQ(X, EXPECTED)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
)
