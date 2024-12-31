#> (eq-between-two-variables-computed-correctly
#>   (out "!"))

VAR("X, Y, Z")
PROG(
  SET(Y, 1),
  SET(X, 1),
  SET(Z, EQ(X, Y)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
