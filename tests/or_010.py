#> (not-or-and-representation-works
#>   (out "!***")
#>   (mem X X X 0...)
#> )

VAR("X, Y, Z")
PROG(
  SET(X, 1), SET(Y, 1),
  SET(Z, NOT(OR(NOT(OR(X, X)), NOT(OR(Y, Y))))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(X, 1), SET(Y, 0),
  SET(Z, NOT(OR(NOT(OR(X, X)), NOT(OR(Y, Y))))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(X, 0), SET(Y, 1),
  SET(Z, NOT(OR(NOT(OR(X, X)), NOT(OR(Y, Y))))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(X, 0), SET(Y, 0),
  SET(Z, NOT(OR(NOT(OR(X, X)), NOT(OR(Y, Y))))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  )
