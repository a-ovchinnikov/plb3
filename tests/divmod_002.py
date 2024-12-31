#> (divmod-works-with-nested-expressions
#>   (out "!!!!!!")
#>   (mem X X X 0...)
#> )

VAR("X, Y, Z")
PROG(
  DIVMOD(ADD(ADD(5, 2), 2), SUB(3, 5), X, Y),
  SET(Z, EQ(X, 4)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  SET(Z, EQ(Y, 1)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  DIVMOD(ADD(ADD(5, 2), SUB(2, 6)), SUB(3, 5), X, Y),
  SET(Z, EQ(X, 5)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  SET(Z, EQ(Y, 1)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  DIVMOD(ADD(ADD(5, 2), SUB(2, 6)), SUB(SUB(1, 4), ADD(3, 2)), X, Y),
  SET(Z, EQ(X, 5)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  SET(Z, EQ(Y, 1)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
