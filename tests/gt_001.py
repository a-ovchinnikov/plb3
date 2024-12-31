#> (gt-basic-check-that-it-works
#>   (out "!**")
#>   (mem X 0...)
#> )

VAR("Z")
PROG(
  SET(Z, GT(2, 1)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, GT(1, 1)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, GT(0, 1)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*"))
)
