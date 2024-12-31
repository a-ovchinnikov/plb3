#> (add-complex-expressions-work
#>   (out "!!!")
#>   (mem 1 2 X 0...)  ; (mem X X X 0...) is probably better.
#> )

VAR("X, Y, Z")  # X and Y are effectively constants here.
PROG(
  SET(Z, EQ(8, ADD(ADD(ADD(1, 1), ADD(1, 1)),
                   ADD(ADD(1, 1), ADD(1, 1))))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(X, 1),
  SET(Z, EQ(8, ADD(ADD(ADD(X, X), ADD(X, X)),
                   ADD(ADD(X, X), ADD(X, X))))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Y, 2),
  SET(Z, EQ(12, ADD(ADD(ADD(Y, X), ADD(X, Y)),
                    ADD(ADD(X, Y), ADD(Y, X))))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
