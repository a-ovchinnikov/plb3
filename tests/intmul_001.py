#> (intmul-multiplies-ints
#> (out "!!!!!!!"
#> ))


VAR("X, Y, RES, EXPECTED", INT)
VAR("W")
PROG(
        # All work
        INTSET(X, 193), INTSET(Y, 21), INTSET(EXPECTED, 21*193), SET(W, 0),
        INTMUL(X, Y, RES),
        SET(W, INTEQ(RES, EXPECTED)),
        IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

        INTSET(X, 9), INTSET(Y, 2), INTSET(EXPECTED, 18), SET(W, 0),
        INTMUL(X, Y, RES),
        SET(W, INTEQ(RES, EXPECTED)),
        IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

        INTSET(X, 9), INTSET(Y, 22), INTSET(EXPECTED, 22*9), SET(W, 0),
        INTMUL(X, Y, RES),
        SET(W, INTEQ(RES, EXPECTED)),
        IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

        INTSET(X, -9), INTSET(Y, -22), INTSET(EXPECTED, 22*9), SET(W, 0),
        INTMUL(X, Y, RES),
        SET(W, INTEQ(RES, EXPECTED)),
        IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

        INTSET(X, 9), INTSET(Y, -22), INTSET(EXPECTED, -22*9), SET(W, 0),
        INTMUL(X, Y, RES),
        SET(W, INTEQ(RES, EXPECTED)),
        IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
        # This works too, takes 59.751s to complete

        INTSET(X, 999999), INTSET(Y, 999), INTSET(EXPECTED, 999999*999),
        INTMUL(X, Y, RES),
        SET(W, INTEQ(RES, EXPECTED)),
        IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

        INTSET(X, 524000), INTSET(Y, 524), INTSET(EXPECTED, 524000*524),
        INTMUL(X, Y, RES),
        SET(W, INTEQ(RES, EXPECTED)),
        IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
        )
