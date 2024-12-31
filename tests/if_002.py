#> (ifs-are-independent
#>   (out "!_")
#>   (mem X X 0...)
#> )

VAR("X, Y")
PROG(
  SET(Y, 5),
  IF(Y,
    THEN: PRINT("!"),
    ELSE: PRINT("_")),
  IF(X,
    THEN: PRINT("!"),
    ELSE: PRINT("_")),
  )
