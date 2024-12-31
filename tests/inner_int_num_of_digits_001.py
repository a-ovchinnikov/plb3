#> (**inner-int-num-of-digits-works
#>   (mem 0 0 0   X 0  X 0  X 0  X 0  X 0   X 0  X 0  X 0  X 0  X 0
#>        X 0...
#>   )
#> (out "!!!!!!"
#> ))


VAR("X", INT)
VAR("W")

PROG(
    INTSET(X, 1), SET(W, EQ(_int_num_of_digits(X), 1)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 10), SET(W, EQ(_int_num_of_digits(X), 2)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 101), SET(W, EQ(_int_num_of_digits(X), 3)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 100), SET(W, EQ(_int_num_of_digits(X), 3)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, -100), SET(W, EQ(_int_num_of_digits(X), 3)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 999909999), SET(W, EQ(_int_num_of_digits(X), 9)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
)
