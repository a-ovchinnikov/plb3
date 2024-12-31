#> (eq-operates-correctly-when-nested-three-levels-1
#>   (out "!!!*")
#>   (mem X 0...)
#> )

VAR("Z")
PROG(
  SET(Z, EQ(EQ(EQ(2, 2), EQ(4, 4)), EQ(3, 3))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(EQ(EQ(2, 2), EQ(4, 4)), EQ(EQ(3, 3), 1))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(EQ(EQ(2, 2),
               EQ(4, 4)),
            EQ(EQ(3, 3),
               EQ(1, 1)))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(EQ(EQ(2, 2),
               EQ(2, 1)),
            EQ(EQ(3, 3),
               EQ(1, 1)))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
