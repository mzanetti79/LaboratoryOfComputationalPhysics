import numpy as np
def generatePayoffMatrix(max=20, use_positive=True):
    """Generates a valid payoff matrix for the IPD problem."""
    # M = [R,S;T,P] where T>R>P>S, 2R>T+S

    ok = False
    while not ok:
        if use_positive:
            P = np.random.randint(0,max)
            S = np.random.randint(0,P)
        else:
            P = np.random.randint(-max,max)
            S = np.random.randint(-max,P)
        R = np.random.randint(P,max)
        T = 2*R-S-1
        if T>R and R>P and P>S and 2*R>T+S:
            ok = True
    M = np.array([[R,S],[T,P]])	
    return M