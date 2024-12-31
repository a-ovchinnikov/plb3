#> (printing-of-variables-works-in-general
# >   (out "012345678910111228")
#>   (mem X 0...)
#> )

# Заглушка для тестового файла.
VAR("X")
PROG(
  SET(X, 1)
)

# Закомментированно для экономии времени. См. print_003
# VAR("X")
# PROG(
#   SET(X, 0),
#   PRINT(X),
#   INC(X), #1
#   PRINT(X),
#   INC(X), #2
#   PRINT(X),
#   INC(X), #2
#   PRINT(X),
#   INC(X), #2
#   PRINT(X),
#   INC(X), #2
#   PRINT(X),
#   INC(X), #2
#   PRINT(X),
#   INC(X), #2
#   PRINT(X),
#   INC(X), #2
#   PRINT(X),
#   INC(X), #2
#   PRINT(X),
#   INC(X), #2
#   PRINT(X),
#   INC(X), #2
#   PRINT(X),
#   INC(X), #2
#   PRINT(X),
#   SET(X, 28),
#   PRINT(X),
#   # This prob does not work well
# #  SET(X, 128),
# #  PRINT(X),
# )
