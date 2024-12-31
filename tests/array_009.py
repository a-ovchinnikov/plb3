#> (arrays-mixed-operations-work-together
#>   (mem X X 0 0 0 4 0 5 0 6 0  0 0 0 4 0 5 0 6 0   0...)
#> )

VAR("W")
VAR("T")
ARRAY(("X, Y", 3))

PROG(
    SET(W, 3),
    WHILE(W, PROG(
        DEC(W),
        SET(T, ADD(4, W)),
        ARRSET(X, W, T),
        )),
    SET(W, 3),
    WHILE(W, PROG(
        DEC(W),
        SET(T, ARRGET(X, W)),
        ARRSET(Y, W, T),
        )),
    )
