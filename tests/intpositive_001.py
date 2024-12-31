#> (intpositive-detects-that-an-integer-is-positive
#>   (mem 0 0 0   X 0  0 0  0 0  0 0  0 0   9 0  9 0  0 0  0 0  9 0  X 0...)
#>   (out "!*!*")
#> )

VAR("X", INT)
VAR("Y")
PROG(
     INTSET(X, 99009),
     SET(Y, INTPOSITIVE(X)),
     IF(Y, THEN: PRINT("!"), ELSE: PRINT("*")),
     INTNEGSELF(X),
     SET(Y, INTPOSITIVE(X)),
     IF(Y, THEN: PRINT("!"), ELSE: PRINT("*")),
     INTNEGSELF(X),
     SET(Y, INTPOSITIVE(X)),
     IF(Y, THEN: PRINT("!"), ELSE: PRINT("*")),
     SET(Y, NOT(INTPOSITIVE(X))),
     IF(Y, THEN: PRINT("!"), ELSE: PRINT("*")),
)
