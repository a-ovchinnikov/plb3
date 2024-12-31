#> (inttobytes-converts-ints-to-bytes-the-best-it-can
#> ;                               1  1 1   1 1  1 1  1 1  1 2  2 2
#> ;      0 1 2   3 4  5 6  7 8  9 0  1 2   3 4  5 6  7 8  9 0  1 2
#> ;      ---------------------------------------------------------
# >   (mem 0 0 0   X 0  0 0  0 0  0 0  0 0   X 0  0 0  X 0  X 0  X 0   ; X
#> ;
#> (out "!")
#> )

VAR("X", INT)
VAR("Y, W")
PROG(
        INTSET(X, 235),
        SET(Y, INTTOBYTE(X)),
        SET(W, EQ(Y, 235)),
        IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
)
