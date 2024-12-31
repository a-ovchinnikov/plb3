#> (intset-can-set-an-int-from-direct-constant
#>   (mem 0 0 0   0 0  0 0  0 0  0 0  0 0   9 0  9 0  0 0  0 0  9 0  X X)
#>   (out "!!")
#> )

VAR("X", INT)
VAR("Y, W")
PROG(
     INTSET(X, 5),
        # checkpoint(@addr == 5)  -- это снова потребует лазать в кишки интерпретера
     SET(W, EQ(ARRGET(X, 9), 5)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
     INTSET(X, 0),
     SET(W, NOT(ARRGET(X, 9))),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
     INTSET(X, 99009),
)
