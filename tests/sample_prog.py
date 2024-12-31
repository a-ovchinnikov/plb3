# Простая тестовая программа, которая должна скомпилирловаться
#
#> (smoke-test-1-some-definitions-and-a-print
#>   (runner SimpleRunner)
#>   (out "HI!" 10))
VAR("X, Y")
PROG(
        SET(X, 2),
        SET(Y, X),
        PRINT("HI!\n"),
)
