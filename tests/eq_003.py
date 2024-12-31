#> (eq-between-variable-and-constant-computed-correctly
#>   (out "!")
#>   (mem X X 0...)
#>)

VAR("X, Z")
PROG(
  SET(X, 2),
  SET(Z, EQ(X, 2)),
  IF(Z,
    THEN: PRINT("!"),
    ELSE: PRINT("*")
    ),
  )
