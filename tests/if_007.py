#> (two-nested-ifs-operate-correctly-1
#>   (out "!")
#>   (mem X X 0...)
#> )

VAR("X, Y")
PROG(
  SET(Y, 5),
  SET(X, 3),
  IF(Y,
    THEN: IF(X,
             THEN: PRINT("!"),
             ELSE: PRINT("*")),
    ELSE: PRINT("_")),
  )
