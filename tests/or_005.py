#> (or-works-for-combo-of-constant-and-expression
#>   (out "!!" "!!" "!!" "*!")
#>   (mem X 0...)
#> )

VAR("Z")
PROG(
  SET(Z, OR(1, EQ(1, 2))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  SET(Z, 0),
  SET(Z, OR(1, NOT(EQ(1, 1)))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, 0),
  SET(Z, OR(1, NOT(2))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  SET(Z, 0),
  SET(Z, OR(1, NOT(NOT(NOT(2))))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(1, NOT(NOT(NOT(2))))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  SET(Z, OR(0, EQ(1, 1))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(0, EQ(1, 2))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  SET(Z, OR(1, EQ(1, 1))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  )
