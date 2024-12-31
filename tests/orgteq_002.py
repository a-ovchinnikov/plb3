#> (or-gt-eq-work-together
#>   (out "!!" "!!" "!!" "!!!")
#>   (mem X X X X 0...)
#> )

VAR("X, Y, W, Z")
PROG(
  SET(X, 1), SET(Y, 2), SET(W, 2),

  SET(Z, OR(EQ(X, Y), GT(Y, X))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  SET(Z, OR(GT(Y, X), EQ(X, Y))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(EQ(Y, X), EQ(Y, W))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  SET(Z, OR(EQ(Y, W), EQ(Y, X))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(GT(X, Y), GT(Y, X))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  SET(Z, OR(GT(Y, X), GT(X, Y))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(0, GT(Y, X))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  SET(Z, OR(EQ(Y, X), GT(Y, X))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  SET(Z, OR(GT(Y, X), EQ(Y, X))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
