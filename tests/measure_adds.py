# This test is for quick measurement of time it takes to
# do operations on native cells versus time it takes to
# do operation on INTs.
# Summary: ADD with all necessary set-up clearly beats INTADD 
# with all necessary set-up.
#> (add-vs-intadd-measurement
#>  (out just-capture)
#> )

#VAR("W, Y, X")
#VAR("IX, IY", INT)
VAR("IW, IY, IX", INT)
PROG(
    # Test1.
    # Arrangement           Results                                 Comment
    # -------------------------------------------------------------------------------
    # X, Y, W, IX, IY, IW   Code length: 1645; steps taken: 229841  Bad arrangement,
    #                                                               bad idea.
    # X, Y, W               Code length:  403; steps taken:  20495
    # W, X, Y               Code length:  399; steps taken:  20499
    # W, Y, X               Code length:  401; steps taken:  20493
    #
    # W, Y, X, IX           Code length:  815; steps taken:  90275
    # W, Y, X, IX, IY       Code length: 1229; steps taken: 160057
    # Note. how introduction of any amount of INTs drops performance in the sense
    # of increased travel distance.
    # SET(X, 127), SET(Y, 126),
    # SET(W, ADD(X, Y)),
    ## PRINT(W),  # -- it kills prtformance by adding extra 1.8Msteps
    # End test1

    # Test2
    # Arrangement           Results                                 Comment
    # -------------------------------------------------------------------------------
    # X, Y, W, IX, IY, IW   Code length: 40920; steps taken: 185882
    # IX, IY, IW            Code length: 40914; steps taken: 185876
    # IW, IX, IY            Code length: 38522; steps taken: 175480
    # IW, IY, IX            Code length: 38602; steps taken: 175468
     INTSET(IX, 127), INTSET(IY, 126),
     INTADD(IX, IY, IW),
    ## INTPRINT(IW),
    # End test2
)
