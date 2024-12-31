#> (more-complex-arithmetics-works-add-sub
#>   (out "!!!!!")
#>   (mem X X 0...)
#> )

VAR("X, Z")
PROG(
  SET(X, ADD(ADD(1, 2), SUB(3, 5))),
  SET(Z, EQ(5, X)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(X, ADD(SUB(ADD(1, 2), 4), SUB(3, 5))),
  SET(Z, EQ(3, X)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(X, ADD(SUB(ADD(1, 2), SUB(3, 7)),
             ADD(SUB(3, 5), SUB(1, 2)))),
  SET(Z, EQ(4, X)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(X, 5),
  SET(X, SUB(3, X)),
  SET(Z, EQ(2, X)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(X, 5),
  SET(X, SUB(X, 7)),
  SET(Z, EQ(2, X)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
