# Компиляция: ~6.555с, исполнение: ~11.243с
# Без необходимости не включать!
#> (intadd-works-with-negative-addenda
#> ;; ; ; 0 1 2   3 4  5 6  7 8  9 1  1 1   1 1  1 1  1 1  1 2  2 2
#> ;; ; ;                          0  1 2   3 4  5 6  7 8  9 0  1 2
#>   (mem 0 0 0   1 0  0 0  0 0  0 0  0 0   X 0  0 0  X 0  X 0  X 0   ; X
#> ;; ; ; 2 2 2   2 2  2 2  3 3  3 3  3 3   3 3  3 3  4 4  4 4  4 4
#> ;; ; ; 3 4 5   6 7  8 9  0 1  2 3  4 5   6 7  8 9  0 1  2 3  4 5
#>        0 0 0   1 0  0 0  0 0  0 0  0 0   X 0  0 0  X 0  X 0  X 0   ; Y
#> ;; ; ; 4 4 4   4 5  5 5  5 5  5 5  5 5   5 6  6 6  6 6  6 6  6 6
#> ;; ; ; 6 7 8   9 0  1 2  3 4  5 6  7 8   9 0  1 2  3 4  5 6  7 8
#>        0 0 0   1 0  0 0  0 0  0 0  0 0   X 0  0 0  X 0  X 0  X 0   ; R
#>        0 0 0   1 0  0 0  0 0  0 0  0 0   X 0  0 0  X 0  X 0  X 0 X 0...)
#> (out "!!!!"  ; Section 1.
#>      "!!!!"  ; Section 2.)
#> )

VAR("X, Y, R, EXPECTED", INT)
VAR("W")
PROG(
    # 1.
    INTSET(X, -1), INTSET(Y, -2), INTSET(EXPECTED, -3), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, -12), INTSET(Y, -9), INTSET(EXPECTED, -21), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, -12), INTSET(Y, -109), INTSET(EXPECTED, -121), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, -11), INTSET(Y, -109), INTSET(EXPECTED, -120), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    # 2.
    INTSET(X, -1), INTSET(Y, -9), INTSET(EXPECTED, -10), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, -1), INTSET(Y, -99), INTSET(EXPECTED, -100), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, -27), INTSET(Y, -284), INTSET(EXPECTED, -311), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, -284), INTSET(Y, -27), INTSET(EXPECTED, -311), SET(W, 0),
    INTADD(X, Y, R),
    SET(W, INTEQ(R, EXPECTED)), IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
)
