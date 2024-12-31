#> (arrset-works-with-variables-and-expressions-as-values
#>; Memory layout isquite complex: two 3-el arrays with
#>; three padding cells per array, each cell taking two
#>; memory elements plus a constant allocated after arrays (due to test layout).
#>   (mem 0 0 0 2 0 0 0 0 0 0 0 0 0 0 3 0 0 0 3 0...)
#> )

ARRAY(("X", 3))
ARRAY(("Y", 3))

VAR("W")

PROG(
    SET(W, 3),
    ARRSET(X, 0, ADD(1, 1)),
    ARRSET(Y, 1, W),
    )
