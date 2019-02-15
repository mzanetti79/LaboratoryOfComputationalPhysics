import numpy as np
import matplotlib.pyplot as plt

from mgen import generatePayoffMatrix
from strategy import *
    
def IPD2players(p1, p2, num_iter):
    for _ in range(num_iter):
        p1.play(p2)
    return p1, p2

def main():
    # number of iterations
    NUM_ITER = 50

    print("Testing {} iterations of 2-people IPD".format(NUM_ITER))

    # define k for strategy probabilities
    # strategies = [ProbStrategy(0), ProbStrategy(100), ProbStrategy(kL), ProbStrategy(kH), ProbStrategy(50), TitForTat()]
    kH = np.random.randint(51,100)
    kL = np.random.randint(0,50)
    k_strategies = np.array([0, 100, kL, kH, 50, -1])
    probS = k_strategies >=0

    for (k1, probS1) in zip(k_strategies, probS):
        for (k2, probS2) in zip(k_strategies, probS):
            print("Evaluating {} - {}...".format(k1,k2))
            p1 = Player(k=k1, probS=probS1)
            p2 = Player(k=k2, probS=probS2)
            p1, p2 = IPD2players(p1, p2, NUM_ITER)
            print(p1.stratHist, p1.payoffHist, p1.playedHist)

if __name__ == "__main__":
    main()