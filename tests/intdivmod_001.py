#> (intdovmod-works-too
#> (out "!!" "!!" "!!" "!!" "!!"
#> ))

#x = 12930
#y = 217301
x = 12930
y = 2170
x1 = -12930
y1 = -2170
x2 = -19
y2 = 5
x3 = -279
y3 = 19
x4 = 19
y4 = -5

SUBPROG("VERIFY_W_IS_1", BODY: PROG(IF(W, THEN: PRINT("!"), ELSE: PRINT("*"))))

VAR("X, Y, DIV_RES, MOD_RES, EXPECTED_DR, EXPECTED_MR", INT)
VAR("W")
PROG(
        INTSET(X, x), INTSET(Y, y), SET(W, 0),
        INTSET(EXPECTED_DR, x//y), INTSET(EXPECTED_MR, x%y),
        INTDIVMOD(X, Y, DIV_RES, MOD_RES),
        SET(W, INTEQ(DIV_RES, EXPECTED_DR)), VERIFY_W_IS_1(), SET(W, 0),
        SET(W, INTEQ(MOD_RES, EXPECTED_MR)), VERIFY_W_IS_1(), SET(W, 0),
        # Comment out the code below to get size measurement
        # Last measure: 475629 symbols (down from 1091584).
        # Full execution time is 0.481213

        INTSET(X, x1), INTSET(Y, y1), SET(W, 0),
        INTSET(EXPECTED_DR, x1//y1), INTSET(EXPECTED_MR, x1%y1),
        INTDIVMOD(X, Y, DIV_RES, MOD_RES),
        SET(W, INTEQ(DIV_RES, EXPECTED_DR)), VERIFY_W_IS_1(), SET(W, 0),
        SET(W, INTEQ(MOD_RES, EXPECTED_MR)), VERIFY_W_IS_1(), SET(W, 0),

        INTSET(X, x2), INTSET(Y, y2), SET(W, 0),
        INTSET(EXPECTED_DR, x2//y2), INTSET(EXPECTED_MR, x2%y2),
        INTDIVMOD(X, Y, DIV_RES, MOD_RES),
        SET(W, INTEQ(DIV_RES, EXPECTED_DR)), VERIFY_W_IS_1(), SET(W, 0),
        SET(W, INTEQ(MOD_RES, EXPECTED_MR)), VERIFY_W_IS_1(), SET(W, 0),

        INTSET(X, x3), INTSET(Y, y3), SET(W, 0),
        INTSET(EXPECTED_DR, x3//y3), INTSET(EXPECTED_MR, x3%y3),
        INTDIVMOD(X, Y, DIV_RES, MOD_RES),
        SET(W, INTEQ(DIV_RES, EXPECTED_DR)), VERIFY_W_IS_1(), SET(W, 0),
        SET(W, INTEQ(MOD_RES, EXPECTED_MR)), VERIFY_W_IS_1(), SET(W, 0),

        INTSET(X, x4), INTSET(Y, y4), SET(W, 0),
        INTSET(EXPECTED_DR, x4//y4), INTSET(EXPECTED_MR, x4%y4),
        INTDIVMOD(X, Y, DIV_RES, MOD_RES),
        SET(W, INTEQ(DIV_RES, EXPECTED_DR)), VERIFY_W_IS_1(), SET(W, 0),
        SET(W, INTEQ(MOD_RES, EXPECTED_MR)), VERIFY_W_IS_1(), SET(W, 0),
)
