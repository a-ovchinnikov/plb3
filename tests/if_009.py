#> (two-nested-ifs-operate-correctly-3
#>   (out "_")
#>   (mem X X 0...)
#> )

VAR("X, Y")
PROG(
  SET(Y, 0),
  SET(X, 2),
  IF(Y,
    THEN: IF(X,
             THEN: PRINT("!"),
             ELSE: PRINT("*")),
    ELSE: PRINT("_")),
  )
