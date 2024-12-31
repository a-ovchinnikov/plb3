#> (intset-can-set-a-negative-int-from-another-int-constant
#>   (mem 0 0 0   1 0  0 0  0 0  0 0  0 0   9 0  9 0  0 0  0 0  9 0
#>        0 0 0   1 0  0 0  0 0  0 0  0 0   9 0  9 0  0 0  0 0  9 0)
#> )

VAR("X, Y", INT)
PROG(
     INTSET(X, -99009),
     INTSET(Y, X),
)
