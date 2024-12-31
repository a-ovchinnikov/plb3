#> (eq-operates-correctly-when-nested-and-mixed-with-other-ops
#>   (out "!*!!!")
#>   (mem X 0...)
#> )

VAR("Z")
PROG(
  SET(Z, EQ(EQ(OR(1, 0), 1), EQ(3, 3))),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(EQ(OR(1, 0), 1),
            OR(EQ(4, 3), EQ(3, 4))
           )),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(EQ(OR(1, 0), 0),
            OR(EQ(4, 3), EQ(3, 4))
           )),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(EQ(OR(1, 0), 0),
            OR(EQ(EQ(4, 3), OR(1, 1)), EQ(3, 4))
           )),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, EQ(                   # -> 1
            EQ(OR(1, 0),       # =? 1     -> 0
               EQ(OR(1, 0),    #    =? 1
                  OR(0, 0))),  #       0
            OR(EQ(EQ(4, 3),    # =? 0    ->0 ->0
                  OR(1, 1)),   #    1
               EQ(3, 4))       #    0
           )),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
