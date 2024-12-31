#> (subprograms-can-be-loaded-from-a-library
#>   (out "!")
#>   (mem 5 1 0...)  ; This is a primitive test, unlikely to change, so some constants
#>                   ; are added directly to the verifier.
#> )

LOADLIB("tests/testlib_001.plbl")

VAR("X, Z")
PROG(
  SET(X, 5),
  SET(Z, EQ(2, ADD(1, 1))),
  VERIFY_Z_IS_1(),
)
