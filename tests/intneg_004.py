#> (intnegself-correctly-negates-self
#>   (mem 0 0 0   1 0  0 0  0 0  0 0  0 0   9 0  9 0  0 0  0 0  9 0  0...)
#> )

VAR("X", INT)
PROG(
     INTSET(X, 99009),
     INTNEGSELF(X),
)
