#> (or-works-for-nested-expressions-with-depth-of-three
#>   (out "!**")
#>   (mem X 0...)
#> )

VAR("Z")
PROG(
  SET(Z, OR(OR(OR(0, 0), OR(0, 1)), OR(OR(0, 1), OR(0, 1)))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(OR(OR(0, 0), OR(0, 0)), OR(OR(0, 0), OR(0, 0)))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(OR(OR(0, 0), OR(0, 0)), OR(NOT(OR(0, 1)), OR(0, 0)))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  )
