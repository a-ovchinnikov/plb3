#> (intset-can-set-a-negative-value
#>   (mem 0 0 0   1 0  0 0  0 0  0 0  0 0   9 0  9 0  0 0  0 0  9 0)
#> )

VAR("X", INT)
PROG(
     INTSET(X, -99009),
)
