#> (divmod-basics-works
#>   (out "!!!!!!!!!!!!!!")
#>   (mem X X X 0...)
#> )

# ТУДУ: разделить на три теста, с константами, конастанта плюс ретвал, ретвал-ретвал.

VAR("X, Y, Z")
PROG(
 DIVMOD(9, 2, X, Y),
 SET(Z, EQ(X, 4)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
 SET(Z, EQ(Y, 1)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

 DIVMOD(4, 2, X, Y),
 SET(Z, EQ(X, 2)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
 SET(Z, EQ(Y, 0)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

 DIVMOD(35, 11, X, Y),
 SET(Z, EQ(X, 3)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
 SET(Z, EQ(Y, 2)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

 DIVMOD(10, 11, X, Y),
 SET(Z, EQ(X, 0)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
 SET(Z, EQ(Y, 10)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

 DIVMOD(10, ADD(6, 5), X, Y),
 SET(Z, EQ(X, 0)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
 SET(Z, EQ(Y, 10)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

 DIVMOD(ADD(5, 5), ADD(6, 5), X, Y),
 SET(Z, EQ(X, 0)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
 SET(Z, EQ(Y, 10)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),

 DIVMOD(ADD(30, 5), ADD(6, 5), X, Y),
 SET(Z, EQ(X, 3)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
 SET(Z, EQ(Y, 2)),
 IF(Z, THEN: PRINT("!"), ELSE: PRINT("*")),
)
