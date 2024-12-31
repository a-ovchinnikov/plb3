#> (arrget-works-with-variable-index
#>   (mem 1 0 0 0 0 0 5 0 0 0 2 5 0...)
#> )

VAR("W")
ARRAY(("X", 3))
VAR("C")
VAR("D")

PROG(
    SET(W, 1),
    ARRSET(X, 1, 2),
    SET(C, ARRGET(X, W)),
    ARRSET(X, 1, 5),
    SET(D, ARRGET(X, W)),
    )
