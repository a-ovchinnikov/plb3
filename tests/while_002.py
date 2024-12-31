#> (nested-while-loops-work-together
#>   (out "!!!!!!!!!!!!!!!")
#>   (mem X X X 0...)
#> )

VAR("X, Y, Z")
PROG(
  SET(X, 5),
  WHILE(X,
    PROG(
      SET(Z, 3),
      WHILE(Z,
        PROG(
          DEC(Z),
          PRINT("!"))),
      DEC(X))))
