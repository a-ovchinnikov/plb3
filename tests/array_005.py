#> (arrget-works-with-constants
#>   (mem 0 0 0 2 0 0 0 0 0 2 0...)
#> )

ARRAY(("X", 3))
VAR("W")

PROG(
    ARRSET(X, 0, 2),
    SET(W, ARRGET(X, 0))
    )
