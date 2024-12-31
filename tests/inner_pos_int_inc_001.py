#> (**positive-integer-could-be-incremented-in-place
#>   (mem 0 0 0   X 0  X 0  X 0  X 0  X 0   X 0  X 0  X 0  X 0  X 0
#>        0 0 0   X 0  X 0  X 0  X 0  X 0   X 0  X 0  X 0  X 0  X 0
#>        X 0...
#>   )
#>  (out "!"
#>  )
#> )

VAR("X, EXPECTED", INT)
VAR("W")
PROG(
#    INTSET(X, 1), INTSET(EXPECTED, 2),
#    INTSET(X, 8), INTSET(EXPECTED, 9),
#    INTSET(X, 9), INTSET(EXPECTED, 10),
#    INTSET(X, 10), INTSET(EXPECTED, 11),
#    INTSET(X, 199), INTSET(EXPECTED, 200),
    INTSET(X, 9999), INTSET(EXPECTED, 10000),
    _pos_int_inc(X),
    SET(W, INTEQ(X, EXPECTED)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
)
