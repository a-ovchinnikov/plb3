#> (or-works-for-nested-expressions-with-depth-of-two
#>   (out "!*")
#>   (mem X 0...)
#> )

VAR("Z")
PROG(
  SET(Z, OR(OR(0, 0), OR(1, 2))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(OR(0, 0), OR(0, 0))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  )
