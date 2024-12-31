#> (or-basic-truth-table
#>   (out "!*!!")
#>   (mem X X X 0...)
#> )

VAR("X, Y, Z")
PROG(
  SET(X, 1), SET(Y, 0),
  SET(Z, OR(X, Y)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(X, 0), SET(Y, 0),
  SET(Z, OR(X, Y)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(X, 0), SET(Y, 1),
  SET(Z, OR(X, Y)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(X, 1), SET(Y, 1),
  SET(Z, OR(X, Y)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  )
