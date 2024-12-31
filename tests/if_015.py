#> (three-nested-ifs-operate-correctly-1-second-else-branch-2
#>   (out "!")
#>   (mem X X X 0...)
#> )

VAR("X, Y, Z")
PROG(
  SET(Y, 0),
  SET(X, 0),
  SET(Z, 1),
  IF(Y,
    THEN: PRINT("_"),
    ELSE: IF(X,
             THEN: PRINT("*"),
             ELSE: IF(Z,
                    THEN: PRINT("!"),
                    ELSE: PRINT("$")),
            ),
    ),
  )
