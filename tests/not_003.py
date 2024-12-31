#> (not-constants-negation
#>   (out "*!")
#>   (mem X 0...)
#> )

VAR("Z")
PROG(
  SET(Z, NOT(1)),
  IF(Z,
    THEN: PRINT("!"),
    ELSE: PRINT("*")
    ),
  SET(Z, NOT(0)),
  IF(Z,
    THEN: PRINT("!"),
    ELSE: PRINT("*")
    ),
  )
