#> (intprint-works-with-positive-int
#>   (mem 0 0 0   0 0  0 0  0 0  0 0  0 0   9 0  9 0  0 0  0 0  9 0 0...)
#>   (out "99009")
#> )

VAR("X", INT)
PROG(
     INTSET(X, 99009),
     INTPRINT(X),
)
