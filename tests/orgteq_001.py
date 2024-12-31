#> (nested-or-eq-gt-work-together
#>   (out "!!!!!")
#>   (mem 2 3 2 X 0...)
#> )

VAR("X, Y, W, Z")
PROG(
  SET(X, 2), SET(Y, 3), SET(W, 2),

  SET(Z, 0),
  SET(Z, OR(EQ(X, W), GT(X, W))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, 0),
  SET(Z, OR(EQ(Y, W), GT(Y, W))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, 0),
  SET(Z, OR(GT(Y, W), EQ(Y, W))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, 0),
  SET(Z, OR(GT(X, W), EQ(X, W))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, 0),
  SET(Z, OR(EQ(X, W), GT(X, W))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
