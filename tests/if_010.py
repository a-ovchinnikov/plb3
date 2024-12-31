#> (two-nested-ifs-operate-correctly-4
#>   (out "_")
#>   (mem X X 0...)
#> )

VAR("X, Y")
PROG(
  SET(Y, 0),
  SET(X, 0),
  IF(Y,
    THEN: IF(X,
             THEN: PRINT("!"),
             ELSE: PRINT("*")),
    ELSE: PRINT("_")),
  )
