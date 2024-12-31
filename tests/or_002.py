#> (or-with-constants-works
#>   (out "!!*!")
#>   (mem X 0..))
#> )

VAR("Z")
PROG(
  SET(Z, OR(1, 0)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(0, 1)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(0, 0)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(1, 1)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  )
