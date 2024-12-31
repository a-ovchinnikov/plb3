#> (eq-between-constant-and-constant-computed-correctly
#>   (out "*")
#>   (mem X 0...)
#>)
#
# Туду: а вот это надо выбрасывать на этапе компиляции

VAR("Z")
PROG(
  SET(Z, EQ(2, 1)),
  IF(Z,
    THEN: PRINT("!"),
    ELSE: PRINT("*")
    ),
  )
