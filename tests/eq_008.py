#> (eq-operates-correctly-when-nested-two-levels-2
#>   (out "!*!")
#>   (mem X X X 0...)
#>)

VAR("X, Y, Z")
PROG(
  SET(X, 1), SET(Y, 0),

  SET(Z, EQ(EQ(X, 1), EQ(Y, Y))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(NOT(EQ(X, 1)), EQ(Y, Y))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(NOT(EQ(X, Y)), EQ(Y, Y))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
