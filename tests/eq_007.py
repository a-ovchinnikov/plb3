#> (eq-operates-correctly-when-nested-two-levels-1
#>   (out "!**!")
#>   (mem X 0...)
#>)

VAR("Z")
PROG(
  SET(Z, EQ(EQ(2, 2), EQ(2, 2))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(EQ(1, 2), EQ(2, 2))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(EQ(2, 2), EQ(1, 2))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(EQ(2, 2), EQ(0, 0))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
