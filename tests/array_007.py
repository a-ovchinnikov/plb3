#> (arrget-works-with-constants-in-revers-alloc-order
#>   (mem 2 0 0 0 2 0 0 0 0 0 0 0...)
#> )

VAR("W")
ARRAY(("X", 3))

PROG(
    ARRSET(X, 0, 2),
    SET(W, ARRGET(X, 0))
    )
