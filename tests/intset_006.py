#> (intset-can-set-an-int-from-expression-evaluation-result
#>   (mem   0 0 0   0 0  0 0  0 0  0 0  0 0   0 0  0 0  0 0  1 0  1 0  0...)
#> )

VAR("X", INT)
PROG(
     INTSET(X, ADD(5, 6)),
)
