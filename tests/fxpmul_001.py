#> (fxpmul-works-a-little
#>  (out "!"
#>  )
#> )


#VAR("X, Y, RES", INT)
VAR("X, RES", INT)
PROG(
        # TODO: add some reading mechanism
     INTSET(X, 52400000),  # i.e. 0.52400000
     # Not needed
#     INTSET(Y, 52400000),
    #INTSET(X, 60000000),  # i.e. 0.52400000
    PRINT("\n x   = "),
    FXPPRINT(X),
    #INTSET(Y, 50000000),
    FXPMUL(X, X, RES),
    PRINT("\n x^2 = "),
    FXPPRINT(RES),
    FXPMUL(RES, X, RES),
    PRINT("\n x^3 = "),
    FXPPRINT(RES),
    FXPMUL(RES, X, RES),
    PRINT("\n x^4 = "),
    FXPPRINT(RES),
    FXPMUL(RES, X, RES),
    PRINT("\n x^5 = "),
    FXPPRINT(RES),
    #INTPRINT(RES),
)
