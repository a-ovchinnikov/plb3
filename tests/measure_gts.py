# This test is for quick measurement of time it takes to
# do operations on native cells versus time it takes to
# do operation on INTs.
# Preliminary summary: Layuot of variables matter a lot. I cannot fix that
#                      automatically without running some analyzis.
# Summary: for GT family integers clearly outperform native cells for
#          bigger numbers: there is no significant growth of the number of
#          steps.
#> (gt-vs-intgt-measurement
#>  (out just-capture)
#> )

VAR("IY", INT)
VAR("IX", INT)
VAR("W")
#VAR("IW, IY, IX", INT)
PROG(
    # Test1.1
    # Arrangement           Results                                 Comment
    # -------------------------------------------------------------------------------
    # X, Y, W               Code length: 489; steps taken: 297661
    # W, X, Y               Code length: 485; steps taken: 295649
    # W, Y, X               Code length: 487; steps taken: 295643
    #SET(X, 127), SET(Y, 126),
    #SET(W, GT(X, Y)),
    # End test1

    # Test1.2
    # Arrangement           Results                                 Comment
    # -------------------------------------------------------------------------------
    # X, Y, W               Code length: 745; steps taken: 1151549
    # W, X, Y               Code length: 741; steps taken: 1147489
    # W, Y, X               Code length: 743; steps taken: 1147483
    # SET(X, 255), SET(Y, 254),
    # SET(W, GT(X, Y)),
    # End test1

    # Test2.1
    # Arrangement           Results                                 Comment
    # -------------------------------------------------------------------------------
    # W, IX, IY             Code length: 14201; steps taken: 167415
    # W, IY, IX             Code length: 14281; steps taken: 167311
    # IX, IY, W             Code length: 14149; steps taken: 169259
    # IY, IX, W             Code length: 14229; steps taken: 169155
    # IX, W, IY             Code length: 14175; steps taken: 168341
    # IY, W, IX             Code length: 14257; steps taken: 168231
    #INTSET(IX, 127), INTSET(IY, 126),
    #SET(W, INTGT(IX, IY)),
    ## INTPRINT(IW),
    # End test2

    # Test2.2
    # Arrangement           Results                                 Comment
    # -------------------------------------------------------------------------------
    # W, IX, IY             Code length: 14205; steps taken: 171155
    # W, IY, IX             Code length: 14285; steps taken: 171051
    # IX, IY, W             Code length: 14153; steps taken: 173031
    # IY, IX, W             Code length: 14233; steps taken: 172927
    # IX, W, IY             Code length: 14179; steps taken: 172097
    # IY, W, IX             Code length: 14261; steps taken: 171987
    INTSET(IX, 255), INTSET(IY, 254),
    SET(W, INTGT(IX, IY)),
    ## INTPRINT(IW),
    # End test2
)
