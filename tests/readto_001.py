#> (readto-reads-a-valu-from-stdin
#>  (mem 3 2 0...)
#>  (in  1 2 3)
#>  (out  "123")
#> )

VAR("X, Y")
PROG(
        READTO(X),
        PRINT(X),
        READTO(Y),
        PRINT(Y),
        READTO(X),
        PRINT(X),
)
