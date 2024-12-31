# Простая тестовая программа, которая должна скомпилирловаться
#
#> (while-loop-works-in-general
#>   (out "!!!!!!!!!!")
#>   (mem X X X 0...)
#> )

VAR("X, Y, Z")
PROG(
        SET(Z, 10),
        WHILE(Z,
            PROG(
                DEC(Z),
                PRINT("!")))
)
