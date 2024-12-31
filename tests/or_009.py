#> (or-works-for-nested-expressions-with-depth-of-three-and-variables
#>   (out "!!**")
#>   (mem X X X 0...)
#> )

VAR("X, Y, Z")
PROG(
  SET(X, 1), SET(Y, 0),
  SET(Z, OR(OR(OR(0, Y), OR(0, X)), OR(OR(Y, 1), OR(0, 1)))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(OR(OR(0, Y), OR(0, X)), OR(OR(Y, X), OR(0, 1)))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(OR(OR(Y, 0), OR(0, Y)), OR(OR(0, Y), OR(Y, 0)))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(OR(OR(0, Y), OR(0, Y)), OR(NOT(OR(Y, X)), OR(Y, 0)))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  )
