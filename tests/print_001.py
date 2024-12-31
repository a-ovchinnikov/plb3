# print does not touch _any_ of the vars.
#> (printing-minimal-tests-work
#>   (out "012328")
#>   (mem X 0...)
#> )

VAR("X")
PROG(
  SET(X, 0),
  PRINT(X),
  INC(X), #1
  PRINT(X),
  INC(X), #2
  PRINT(X),
  INC(X), #3
  PRINT(X),
  SET(X, 28),
  PRINT(X),
)
