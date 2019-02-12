import numpy as np
import matplotlib.pyplot as plt

from mgen import generatePayoffMatrix
from strategy import *

def IPD2players(m, s1, s2, num_iter):
    if num_iter == 0: return
    
    m1 = m   # R, S; T, P for player 1
    m2 = m.T # R, T; S, P for player 2

    rew1 = 0 # cumulative reward for both players
    rew2 = 0
    hist1 = np.zeros((num_iter,3),dtype='int') # history of moves
    hist2 = np.zeros((num_iter,3),dtype='int')
    for i in range(num_iter):
        # get actions, to use as indexes in matrix
        # 0 = coop, 1 = defect
        
        if type(s1) != TitForTat:
            action1 = s1.get()
        else:
            action1 = 0 # cooperate
            if i > 0:
                action1 = s1.get(hist2[i-1,0]) # pass opponent's move
            # note: by this logic, a TfT class is totally useless
        
        if type(s2) != TitForTat:
            action2 = s2.get()
        else:
            action2 = 0
            if i > 0:
                action2 = s2.get(hist1[i-1,0])

        # get payoffs from matrix, based on chosen actions
        payoff1 = m1[action1,action2]
        payoff2 = m2[action1,action2]
        rew1 += payoff1
        rew2 += payoff2
        
        # save action, payoff, cumulative result
        hist1[i] = [action1, payoff1, rew1]
        hist2[i] = [action2, payoff2, rew2]
    return hist1, hist2
    
def main():
    # number of iterations
    NUM_ITER = 50

    # define payoff matrix
    M1 = np.array([[2,0],[3,1]]) # one default payoff matrix
    M2 = np.array([[3,0],[5,2]]) # another good choice
    # or use M = generatePayoffMatrix()

    print("Testing {} iterations of 2-people IPD with\nM={}".format(NUM_ITER, M1))

    # define k for strategy probabilities
    kH = np.random.randint(50,101)
    kL = np.random.randint(0,50)
    strategies = [NiceStrategy(), BadStrategy(), MainlyNiceStrategy(kL), MainlyBadStrategy(kH), TitForTat()]
    
    for s1 in strategies:
        for s2 in strategies:
            s1name = str(s1)
            s2name = str(s2)
            print("Evaluating {} - {}...".format(s1name,s2name))

            # play the game
            h1,h2 = IPD2players(M1, s1, s2, NUM_ITER)
            
            # plot cumulative rewards
            plt.plot(h1[:,2])
            plt.plot(h2[:,2])
            plt.title("2 pl. game: {} - {}".format(s1name,s2name))
            plt.xlabel('Iteration')
            plt.ylabel('Cum. reward')
            plt.legend(['Player1','Player2'])

            # strip k from names if necessary
            if '(' in s1name:
                s1name = s1name[0:s1name.find(' (')]
            if '(' in s2name:
                s2name = s2name[0:s2name.find(' (')]
            
            plt.savefig('../img/idp2p-rewards-{}-{}.png'.format(s1name,s2name))
            plt.close()

if __name__ == "__main__":
    main()