#> (handling-of-if-does-not-change-program-state-3
#>   (out "!!!!")
#>   (mem X 0...)
#> )

VAR("Y")
PROG(
  SET(Y, 5),
  IF(Y,
    THEN: PRINT("!"),
    ELSE: PRINT("_")),
  IF(Y,
    THEN: PRINT("!"),
    ELSE: PRINT("_")),
  IF(Y,
    THEN: PRINT("!"),
    ELSE: PRINT("_")),
  IF(Y,
    THEN: PRINT("!"),
    ELSE: PRINT("_")),
  )
