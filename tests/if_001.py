#> (if-works-in-general
#>   (out "!")
#>   (mem X X 0...)
#> )

VAR("X, Y")
PROG(
  SET(Y, 5),
  IF(Y, THEN: PRINT("!"), ELSE: PRINT("*")),
)
