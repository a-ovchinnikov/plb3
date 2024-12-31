#> (arrset-works-with-variable-index
#>; Memory layout isquite complex: two 3-el arrays with
#>; three padding cells per array, each cell taking two
#>; memory elements plus a constant allocated after arrays (due to test layout).
#>; Data cell -- ptr cell
#>   (mem 0 0 0 2 0 3 0 0 0 X 0...)
#> )

ARRAY(("X", 3))
VAR("W")

PROG(
    SET(W, 0),
    ARRSET(X, W, 2),
    SET(W, 1),
    ARRSET(X, W, 5),
    ARRSET(X, W, 3),
    )
