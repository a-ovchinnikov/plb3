#> (sub-basics-works
#>   (out "!!!!")
#>   (mem X 0...)
#> )

VAR("Z")
PROG(
  SET(Z, EQ(2, SUB(2, 4))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(2, SUB(2, SUB(3, 7)))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, GT(3, SUB(2, SUB(3, 7)))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(0, SUB(2, 2))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
