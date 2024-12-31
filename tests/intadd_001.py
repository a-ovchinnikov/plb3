# Компиляция: ~5.874с, исполнение: ~11.243с
# Без необходимости не включать!
#> (intadd-works-with-positive-addenda
#>   (mem 0 0 0   0 0  0 0  0 0  0 0  0 0   X 0  0 0  X 0  X 0  X 0
#>        0 0 0   0 0  0 0  0 0  0 0  0 0   X 0  0 0  X 0  X 0  X 0
#>        0 0 0   0 0  0 0  0 0  0 0  0 0   X 0  0 0  X 0  X 0  X 0
#>        0 0 0   0 0  0 0  0 0  0 0  0 0   X 0  0 0  X 0  X 0  X 0 X 0...)
#> (out "!!!!"  ; Section 1.
#>      "!!!!"  ; Section 2.)
#> )

VAR("X, Y, R, EXPECTED", INT)
VAR("W")
PROG(
    # 1.
    INTSET(X, 1), INTSET(Y, 2), INTSET(EXPECTED, 3), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 12), INTSET(Y, 9), INTSET(EXPECTED, 21), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 12), INTSET(Y, 109), INTSET(EXPECTED, 121), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 11), INTSET(Y, 109), INTSET(EXPECTED, 120), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    # 2.
    INTSET(X, 1), INTSET(Y, 9), INTSET(EXPECTED, 10), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 1), INTSET(Y, 99), INTSET(EXPECTED, 100), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 27), INTSET(Y, 284), INTSET(EXPECTED, 311), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 284), INTSET(Y, 27), INTSET(EXPECTED, 311), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
)
