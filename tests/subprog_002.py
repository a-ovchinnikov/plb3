#> (complex-subprogs-work-and-interact-nicely
#>   (out "!!!!")
#>   (mem X X X 0...)
#> )

SUBPROG("VERIFY_Z_IS_1", BODY: PROG(IF(Z, THEN: PRINT("!"), ELSE: PRINT("*"))))

# Consumes X and Y
# Uses Z as output variable
SUBPROG("COMPLEX_EXPRESSION_1",
        BODY: PROG(SET(Z, (OR(NOT(OR(X, X)), NOT(OR(Y, Y))))),))

# Consumes X and Y
# Uses Z as output variable
SUBPROG("COMPLEX_EXPRESSION_2",
        BODY: PROG( SET(Z, NOT(OR(NOT(OR(X, X)), NOT(OR(Y, Y))))),))

# Consumes X and Y
# Uses Z as output variable
SUBPROG("COMPLEX_EXPRESSION_3",
        BODY: PROG(
                   SET(Z, 0), SET(X, 1), SET(Y, 1),
                   SET(Z, OR(OR(OR(0, Y), OR(0, Y)), OR(NOT(OR(Y, X)), OR(Y, 0)))),
                   VERIFY_Z_IS_1(),))

# Consumes X and Y
# Uses Z as output variable
SUBPROG("COMPLEX_EXPRESSION_4",
        BODY: PROG(
                   SET(Z, 0), SET(X, 1), SET(Y, 1),
                   COMPLEX_EXPRESSION_2(),
                   VERIFY_Z_IS_1(),))

VAR("X, Y, Z")
PROG(
  SET(X, 0), SET(Y, 0),
  COMPLEX_EXPRESSION_1(),
  VERIFY_Z_IS_1(),
  SET(Z, 0), SET(X, 1), SET(Y, 1),
  COMPLEX_EXPRESSION_2(),
  VERIFY_Z_IS_1(),
  COMPLEX_EXPRESSION_3(),
  COMPLEX_EXPRESSION_4(),
)
