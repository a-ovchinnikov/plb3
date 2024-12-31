#> (BF-can-compute-sines-easily
#>  (out "!"))

VAR("X0, X1, X2, X3, T, I, D, RES", FXP)
PROG(
    PRINT("\n * This program computes sines\n"),
    PRINT(" * of angles in radians.\n"),
    PRINT(" *\n"),

    FXPSET(X0,  0.785398),
    PRINT(" * computing for x = "), FXPPRINT(X0), PRINT("\n"),

    # X^3
    FXPMUL(X0, X0, I), FXPMUL(I, X0, T), FXPSET(X1, T),

    # X^5
    FXPMUL(X1, X0, X2), FXPMUL(X2, X0, T), FXPSET(X2, T), FXPSET(T, 0),

    # X^7
    FXPMUL(X2, X0, X3), FXPMUL(X3, X0, T), FXPSET(X3, T), FXPSET(T, 0),

    # Second term
    FXPSET(D, 6.0),
    FXPDIV(X1, D, I),
    FXPSUB(I, X0, RES),
    # Third term
    FXPSET(T, 0), FXPSET(I, 0),
    FXPSET(D, 1.2),
    FXPDIVBY10(X2),  # D should be 120, but due to 1.8 limitations I make it 1.2
    FXPDIVBY10(X2),  # and divide X2 by 100 instead.
    FXPDIV(X2, D, I),
    FXPADD(RES, I, T),
    FXPSET(RES, T),
    # Fourth term
    FXPSET(T, 0), FXPSET(I, 0),
    FXPSET(D, 5.04), # 5040, but trimmed to FXP limitations.
    FXPDIVBY10(X3),
    FXPDIVBY10(X3),
    FXPDIVBY10(X3),
    FXPDIV(X3, D, I),
    FXPSUB(I, RES, T),
    FXPSET(RES, T),

    PRINT(" * ------\n"),
    PRINT(" * Answer: sin(x) = "), FXPPRINT(RES), PRINT("\n"),
)
