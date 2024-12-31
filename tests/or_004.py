#> (or-works-for-combo-of-eqpression-and-constant
#>   (out "!!*!")
#>   (mem X 0...)
#> )

VAR("Z")
PROG(
  SET(Z, OR(EQ(1, 2), 1)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(EQ(1, 1), 0)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(EQ(1, 2), 0)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(EQ(1, 1), 1)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  )
