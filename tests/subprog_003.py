#> (it-is-possible-to-sneak-variables-into-a-subprog
#>   (out "!")
#>   (mem X X 0...)
#> )

SUBPROG("VERIFY_IS_1", lambda Z: PROG(IF(Z, THEN: PRINT("!"), ELSE: PRINT("*"))))

VAR("X, W")
PROG(
  SET(X, 5),
  SET(W, EQ(X, 5)),
  VERIFY_IS_1(W),
)
