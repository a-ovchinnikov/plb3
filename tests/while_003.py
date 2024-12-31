#> (smoke-test-4-nested-while-loop-if-tests
#>   (out "!!!!!!!!!!!!!!!!!!!!")
#>   (mem X X X X 0...)
#> )

VAR("X, Y, Z")
VAR("TMP")
PROG(
  SET(X, 10),
  WHILE(X,
    PROG(
      SET(Z, 4),
      WHILE(Z,
        PROG(
          DEC(Z),
          PRINT("!"))),
      DEC(X),
      SET(TMP, EQ(X, 5)),
      IF(TMP,
         THEN: SET(X, 0),
         ELSE: NOP())
      )))
