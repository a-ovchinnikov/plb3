#> (gt-basic-expressions-work
#>   (out "!*!")
#>   (mem X 0...)
#> )

VAR("Z")
PROG(
  SET(Z, GT(2, EQ(1, 1))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, GT(EQ(1, 1), 2)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, GT(EQ(1, 1), EQ(1, 0))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
