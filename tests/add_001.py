#> (add-basics-works
#>   (out "!!!!!!")
#>   (mem 5 X 0...)  ; First variable is essentialy a constant.
#> )

VAR("X, Z")
PROG(
  SET(X, 5),
  SET(Z, EQ(2, ADD(1, 1))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(3, ADD(2, 1))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(X, 5),
  SET(Z, EQ(8, ADD(3, X))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(ADD(4, 4), ADD(3, X))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, GT(ADD(7, 4), ADD(X, X))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, GT(ADD(ADD(X, 1), 5), ADD(X, X))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
