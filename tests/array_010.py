#> (arrays-reversal-works
#>   (mem X X X   0 0 0 4 0 5 0 6 0   0 0 0 6 0 5 0 4 0   0...)
#> )

VAR("W, T, R")
ARRAY(("X, Y", 3))

SUBPROG("REVERT_ARRAY", lambda SRC, TGT, W, R, SZ: PROG(
    SET(R, SZ),
    WHILE(R, PROG(
        DEC(R),
        SET(T, ARRGET(X, R)),
        ARRSET(Y, W, T),
        INC(W),
        )),
    ))

PROG(
    SET(W, 3),
    WHILE(W, PROG(
        DEC(W),
        SET(T, ADD(4, W)),
        ARRSET(X, W, T),
        )),
    REVERT_ARRAY(X, Y, W, R, 3),
    )
