#> (several-subprograms-can-coexist-in-several-libraries
#>   (out "!!")
#>   (mem X X X 0...)
#> )

LOADLIB("tests/testlib_001.plbl")
LOADLIB("tests/testlib_002.plbl")

VAR("X, Z")
PROG(
  SET(X, 5),
  SET(Z, EQ(X, 5)),
  VERIFY_Z_IS_1(),
  DO_SOME_MAGIC(),
  VERIFY_SOME_MAGIC(),
)
