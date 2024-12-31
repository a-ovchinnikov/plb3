#> (sub-works-with-self-reference
#>   (out "!")
#>   (mem 1 X 0...)
#> )

VAR("X, Z")
PROG(
  SET(X, 11),
  SET(X, SUB(10, X)),
  SET(Z, EQ(1, X)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
