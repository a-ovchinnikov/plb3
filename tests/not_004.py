#> (not-negation-of-expression-evalutaion
#>   (out "!**!"))

VAR("Z")
PROG(
  SET(Z, NOT(EQ(1, 2))),
  IF(Z,
    THEN: PRINT("!"),
    ELSE: PRINT("*")
    ),

  SET(Z, NOT(EQ(1, 1))),
  IF(Z,
    THEN: PRINT("!"),
    ELSE: PRINT("*")
    ),

  SET(Z, NOT(NOT(EQ(1, 2)))),
  IF(Z,
    THEN: PRINT("!"),
    ELSE: PRINT("*")
    ),

  SET(Z, NOT(NOT(NOT(EQ(1, 2))))),
  IF(Z,
    THEN: PRINT("!"),
    ELSE: PRINT("*")
    ),
  )
