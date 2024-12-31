#> (eq-between-two-variables-computed-correctly-2
#>   (out "*"))

VAR("X, Y, Z")
PROG(
  SET(Y, 1),
  SET(X, 2),
  SET(Z, EQ(X, Y)),
  IF(Z,
    THEN: PRINT("!"),
    ELSE: PRINT("*")
    ),
  )
