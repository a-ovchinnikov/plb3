#> (or-works-with-eqpressions
#>   (out "!!*!")
#>   (mem X 0...)
#> )

VAR("Z")
PROG(
  SET(Z, OR(EQ(1, 2), EQ(1, 1))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(EQ(1, 1), EQ(1, 2))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(EQ(1, 2), EQ(1, 2))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(EQ(1, 1), EQ(1, 1))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  )
