#> (handling-of-if-does-not-change-program-state-1
#>   (out "!!"))

VAR("Y")
PROG(
  SET(Y, 5),
  IF(Y,
    THEN: PRINT("!"),
    ELSE: PRINT("_")),
  IF(Y,
    THEN: PRINT("!"),
    ELSE: PRINT("_")),
  )
