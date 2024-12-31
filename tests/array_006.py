#> (arrset-works-with-variable-index-and-any-var-order
#>; Memory layout isquite complex: two 3-el arrays with
#>; three padding cells per array, each cell taking two
#>; memory elements plus a constant allocated after arrays (due to test layout).
#>; Data cell -- ptr cell
#>   (mem X 0 0 0 0 0 0 0 X 0 0 0 2 0 3 0 0 0 0...)
#> )

VAR("W")
ARRAY(("FOO", 2))
VAR("Y")
ARRAY(("X", 3))

PROG(
    SET(W, 0),
    ARRSET(X, W, 2),
    SET(W, 1),
    ARRSET(X, W, 5),
    ARRSET(X, W, 3),
    )
