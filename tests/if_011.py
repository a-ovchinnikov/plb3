#> (three-nested-ifs-operate-correctly-1
#>   (out "!")
#>   (mem X X X 0...)
#> )

VAR("X, Y, Z")
PROG(
  SET(Y, 1),
  SET(X, 1),
  SET(Z, 1),
  IF(Y,
    THEN: IF(X,
             THEN: IF(Z,
                    THEN: PRINT("!"),
                    ELSE: PRINT("$")),
             ELSE: PRINT("*")),
    ELSE: PRINT("_")),
  )
