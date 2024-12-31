#> (not-2
#>   (out "!")
#>   (mem X X 0...)
#> )

VAR("X, Z")
PROG(
  SET(X, 0),
  SET(Z, NOT(X)),
  IF(Z,
    THEN: PRINT("!"),
    ELSE: PRINT("*")
    ),
  )
