#> (fibonacci-demo-program-computes-nth-fibonacci-number
#>  (in "4" "0" 10)
#>  (out "Welcome to Fibonacci computer!" 10
#>        "It computes n-th Fibonacci number."
#>        "Please enter n>2:"
#>        "Result is:"
#>        "832040"
#>  )
#> )

VAR("FIB1, FIB2, NEXT, N", INT)
VAR("LOOP", BYTE)
PROG(
        INTSET(FIB2, 1),
        PRINT("\n * Welcome to Fibonacci computer!"),
        PRINT("\n * It computes n-th Fibonacci number."),
        PRINT("\n * Please enter n>2: "),
        INTREAD(N),
	INTPRINT(N),
	SET(LOOP, SUB(1, INTTOBYTE(N))),
        WHILE(LOOP, PROG(
            INTADD(FIB1, FIB2, NEXT),
            INTSET(FIB1, FIB2),
            INTSET(FIB2, NEXT),
            DEC(LOOP),
            )),
        PRINT("\n===\n * Result is:"),
        INTPRINT(NEXT),
)
