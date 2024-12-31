#> (two-nested-ifs-operate-correctly-1-else-branch
#>   (out "!")
#>   (mem X X 0...)
#> )

VAR("X, Y")
PROG(
  SET(Y, 0),
  SET(X, 2),
  IF(Y,
    THEN: PRINT("_"),
    ELSE: IF(X,
             THEN: PRINT("!"),
             ELSE: PRINT("*"))),
  )
