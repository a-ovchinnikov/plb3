#> (not-1
#>   (out "*")
#>   (mem X X 0...)
#> )

VAR("X, Z")
PROG(
  SET(X, 1),
  SET(Z, NOT(X)),
  IF(Z,
    THEN: PRINT("!"),
    ELSE: PRINT("*")
    ),
  )
