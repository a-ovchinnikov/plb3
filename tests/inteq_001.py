#> (inteq-works
#>   (mem 0 0 0   0 0  0 0  0 0  0 0  0 0   9 0  9 0  0 0  0 0  9 0
#>        0 0 0   0 0  0 0  0 0  0 0  X 0   X 0  X 0  X 0  X 0  X 0 X 0...)
#>   (out "!*******!")
#> )

VAR("X, Y", INT)
VAR("W")
PROG(
     INTSET(X, 99009),
     INTSET(Y, 99009),
     SET(W, INTEQ(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

     INTSET(Y, 99008),
     SET(W, INTEQ(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

     INTSET(Y, 99019),
     SET(W, INTEQ(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

     INTSET(Y, 91009),
     SET(W, INTEQ(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

     INTSET(Y, 19009),
     SET(W, INTEQ(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

     INTSET(Y, 9909),
     SET(W, INTEQ(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

     INTSET(Y, 990009),
     SET(W, INTEQ(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

     INTSET(Y, -99009),
     SET(W, INTEQ(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

     INTSET(Y, X),
     SET(W, INTEQ(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
)
