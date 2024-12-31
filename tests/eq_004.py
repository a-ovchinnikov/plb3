#> (eq-between-variable-and-constant-computed-correctly-2
#>   (out "*")
#>   (mem X X 0...)
#>)

VAR("X, Z")
PROG(
  SET(X, 2),
  SET(Z, EQ(X, 1)),
  IF(Z,
    THEN: PRINT("!"),
    ELSE: PRINT("*")
    ),
  )
