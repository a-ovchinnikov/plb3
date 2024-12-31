#> (gt-variables-work
#>   (out "!**")
#>   (mem X X X 0...)
#> )

VAR("X, Y, Z")
PROG(
  SET(X, 1), SET(Y, 2),

  SET(Z, GT(Y, X)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, GT(X, Y)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, GT(EQ(1, 1), Y)),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
