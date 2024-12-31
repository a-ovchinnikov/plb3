#> (parts-of-code-can-be-tucked-away-into-a-subprogram
#>   (out "!")
#>   (mem 5 1 0...)  ; This is a primitive test, unlikely to change, so some constants
#>                   ; are added directly to the verifier.
#> )

SUBPROG("VERIFY_Z_IS_1",
        BODY: PROG(IF(Z, THEN: PRINT("!"), ELSE: PRINT("*"))))

VAR("X, Z")
PROG(
  SET(X, 5),
  SET(Z, EQ(2, ADD(1, 1))),
  VERIFY_Z_IS_1(),
)
