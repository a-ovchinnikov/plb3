#> (several-subprograms-can-coexist-in-a-library
#>   (out "!")
#>   (mem X X 0...)
#> )

LOADLIB("tests/testlib_002.plbl")

VAR("X")
PROG(
  SET(X, 5),
  DO_SOME_MAGIC(),
  VERIFY_SOME_MAGIC(),
)
