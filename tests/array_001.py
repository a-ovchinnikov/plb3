#> (minimal-array-allocation-works
#>   (out "!")
#>   (mem 0...)
#> )

ARRAY(("X", 5))
ARRAY(("Y", 5))
ARRAY(("W, Z", 10))
ARRAY(("Q, P", 3), ("A, B, C, D", 2))

PROG(PRINT("!"))
