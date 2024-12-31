#> (fxpdiv-works-a-little
#>  (out "!"
#>  )
#> )


VAR("X, Y, RES", INT)
PROG(
        # TODO: add some reading mechanism
     INTSET(X, 103910000),  # i.e. 0.52400000
     INTSET(Y, 245083100),
    PRINT("\n x   = "),
    FXPPRINT(X),
    PRINT("\n Y   = "),
    FXPPRINT(Y),

    FXPDIV(X, Y, RES),
    PRINT("\n x/y = "),
    FXPPRINT(RES),
)
