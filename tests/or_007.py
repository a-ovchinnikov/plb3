#> (or-not-mixture-works-for-nested-expressions
#>   (out "!*!*!")
#>   (mem X 0...)
#> )

VAR("Z")
PROG(
  SET(Z, OR(NOT(OR(0, 0)), NOT(OR(1, 2)))),  # 1
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, NOT(OR(NOT(OR(0, 0)), NOT(OR(1, 2))))),  # 0
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(NOT(OR(NOT(OR(0, 0)), NOT(OR(1, 2)))), OR(1, 0))),  # 1
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(NOT(OR(NOT(OR(0, 0)), NOT(OR(1, 2)))), NOT(OR(1, 0)))),  # 0
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

  SET(Z, OR(NOT(OR(NOT(OR(0, 0)), NOT(OR(1, 2)))),  # 1
            NOT(NOT(OR(NOT(OR(0, 0)), NOT(OR(1, 2)))))
      )),
  IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
  )
