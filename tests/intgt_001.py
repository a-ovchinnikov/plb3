#> (intgt-works
#> ; Тест заканчивается на отрицательных числах, надо убедиться, что они остаются
#> ; отрицательными.
#>   (mem 0 0 0   1 0  0 0  0 0  0 0  0 0   9 0  9 0  0 0  X 0  X 0
#>        0 0 0   1 0  0 0  0 0  0 0  X 0   9 0  9 0  0 0  X 0  X 0 X 0...)
#>   (out "!!!!"  ; Первая секция с положительными числами и со смешанными.
#>        "****"  ; Негативные состояния для положительных чисел.
#>        "!!**"  ; Отрицательные числа.
#>   )
#> )
# ТУДУ: этот тест огромен и ужасен. Подумать на досуге, как бы его уместить на один экран.
# Помимо размеров он ещё компилируется 3.3 секунды, а исполняется семь.

VAR("X, Y", INT)
VAR("W")
PROG(
    # ! (все Х строго больше Y)
    INTSET(X, -99010), INTSET(Y, 99009), SET(W, NOT(INTGT(X, Y))),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 99010), INTSET(Y, -99009), SET(W, 0), SET(W, INTGT(X, Y)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 99010), INTSET(Y, 99009), SET(W, 0), SET(W, INTGT(X, Y)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 99009), INTSET(Y, 99008), SET(W, 0), SET(W, INTGT(X, Y)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
    # * (все Х меньше или равны Y)

    INTSET(X, 99009), INTSET(Y, 99009), SET(W, INTGT(X, Y)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 99008), INTSET(Y, 99009), SET(W, 1), SET(W, INTGT(X, Y)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 99009), INTSET(Y, 99010), SET(W, 1), SET(W, INTGT(X, Y)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

    INTSET(X, 9), INTSET(Y, 10), SET(W, 1), SET(W, INTGT(X, Y)),
    IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

     # ! для отрицательных Х строго больше чем Y
     INTSET(X, -99008), INTSET(Y, -99009), SET(W, 0), SET(W, INTGT(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

     INTSET(X, -99008), INTSET(Y, -99010), SET(W, 0), SET(W, INTGT(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
     # * для отрицательных Х меньших или равных Y
     INTSET(X, -99008), INTSET(Y, -99007), SET(W, 1), SET(W, INTGT(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),

     INTSET(X, -99010), INTSET(Y, -99009), SET(W, 1), SET(W, INTGT(X, Y)),
     IF(W, THEN: PRINT("!"), ELSE: PRINT("*")),
)
