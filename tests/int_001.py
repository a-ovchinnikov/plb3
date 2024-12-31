#> (integer-variables-could-be-created-and-reated-as-arrays
# Это очень плохой пример, просто базовый тест на вшивость.
#>   (mem 0 0 0   5 0  0 0  0 0  0 0  0 0   0 0  0 0  0 0  0 0  5 0
#>        0 0 0   0 0  2 0  0 0  2 0  0 0   2 0  0 0  2 0  0 0  2 0)
#> )

VAR("X, Y", INT)
PROG(
     ARRSET(X, 0, 5),
     ARRSET(X, 9, 5),
     ARRSET(Y, 1, 2),
     ARRSET(Y, 3, 2),
     ARRSET(Y, 5, 2),
     ARRSET(Y, 7, 2),
     ARRSET(Y, 9, 2),
)
