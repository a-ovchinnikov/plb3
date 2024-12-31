#> (intnegself-correctly-negates-self-negative-int
#>   (mem 0 0 0   0 0  0 0  0 0  0 0  0 0   9 0  9 0  0 0  0 0  9 0  0...)
#> )

VAR("X", INT)
PROG(
     INTSET(X, -99009),
     INTNEGSELF(X),
)
