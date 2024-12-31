#> (BF-can-compute-sines-easily
#>  (out "!"))

#VAR("X0, X1, X2, X3, T, I, D, RES", FXP)
#VAR("X0, X1, T, I, RES", FXP)
VAR("RES, T, I, X1, X0", FXP)
PROG(
    PRINT("\n * This program computes sines\n"),
    PRINT(" * of angles in radians.\n"),
    PRINT(" *\n"),

    FXPSET(X0,  0.785398),
    PRINT(" * computing for x = "), FXPPRINT(X0), PRINT("\n"),

    # Second term
    # X^3
    FXPMUL(X0, X0, X1), FXPMUL(X1, X0, X1),
    FXPSET(T, 6.0),
    FXPDIV(X1, T, I),
    FXPSUB(I, X0, RES),
    # Third term
    # X^5
    FXPMUL(X1, X0, X1), FXPMUL(X1, X0, X1),
    FXPSET(T, 1.2),
    FXPDIVBY10(X1),  # D should be 120, but due to 1.8 limitations I make it 1.2
    FXPDIVBY10(X1),  # and divide X2 by 100 instead.
    FXPDIV(X1, T, I),
    FXPADD(RES, I, T),
    FXPSET(RES, T),
    # Fourth term
    _int_shift_left_in_place(X1),
    _int_shift_left_in_place(X1),
    FXPMUL(X1, X0, X1), FXPMUL(X1, X0, X1),
    FXPSET(T, 5.04), # 5040, but trimmed to FXP limitations.
    FXPDIVBY10(X1),
    FXPDIVBY10(X1),
    FXPDIVBY10(X1),
    FXPDIV(X1, T, I),
    FXPSUB(I, RES, T),
    FXPSET(RES, T),

    PRINT(" * ------\n"),
    PRINT(" * Answer: sin(x) = "), FXPPRINT(RES), PRINT("\n"),
)
