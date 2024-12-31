#> (sequence-of-ifs-remains-independent
#>   (out "!_!"))

VAR("X, Y")
PROG(
  SET(Y, 5),
  IF(Y,
    THEN: PRINT("!"),
    ELSE: PRINT("_")),
  IF(X,
    THEN: PRINT("!"),
    ELSE: PRINT("_")),
  IF(Y,
    THEN: PRINT("!"),
    ELSE: PRINT("_")),
  )
