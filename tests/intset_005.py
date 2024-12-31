#> (intset-can-set-an-int-from-global-variable
#>   (mem 0 0 0   0 0  0 0  0 0  0 0  0 0   0 0  0 0  0 0  1 0  1 0  X 0...)
#> )

VAR("X", INT)
VAR("Y")
PROG(
# Код ниже работает без ошибок, но с текущей реализацией DIVMOD выполняется 37.611с
#     SET(Y, 255),
     SET(Y, 11),
     INTSET(X, Y),
)
