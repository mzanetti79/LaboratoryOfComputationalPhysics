import numpy as np
import matplotlib.pyplot as plt

from mgen import generatePayoffMatrix
from strategy import *

from ipd2p_v1 import IPD2players

def IPDRoundRobin(k_strategies, probS, num_round):
    n = num_strat = k_strategies.size
    actual_round = 0
    index = 0
    num_iter = int((((n-1)/2)*(n))*num_round)

    # rewards = np.zeros(num_strat,dtype='int') # cumulative reward for both players
    # hist = np.zeros((num_iter,8),dtype='int') # history of moves
    round_robin_p = np.array([])
    for actual_round in range(num_round):
        # player1 e.g s1 is index i
        for (i, k1, probS1) in zip(np.arange(num_strat), k_strategies, probS):
            #player2 e.g s2 is index j
            for (j, k2, probS2) in zip(np.arange(num_strat), k_strategies, probS):

                if j>i:
                    # to be checked
                    p1 = Player(k=k1, probS=probS1)
                    p2 = Player(k=k2, probS=probS2)
                    p1, p2 = IPD2players(p1, p2, num_iter)
                    round_robin_p = np.append(round_robin_p, [p1, p2])

    return round_robin_p.reshape(int(round_robin_p.size/2), 2)
    
def main():
    # number of rounds and players
    NUM_ROUND = 5
    NUM_PLAYERS = 10

    print("Testing {} rounds of {}-people IPD".format(NUM_ROUND, NUM_PLAYERS))

    # define strategies for players
    # -1 = TfT
    k_strategies = np.random.choice([0, 100, 50, -1, -2, -2], NUM_PLAYERS)
    # set random k if k == -2
    mask = k_strategies == -2
    k_strategies[mask] = np.random.randint(0,100,size=np.sum(mask))
    probS = k_strategies >=0

    round_robin_p = IPDRoundRobin(k_strategies, probS, NUM_ROUND)
    print(round_robin_p.shape)
    # # plot cumulative rewards
    # plt.figure(figsize=(15,5)) 
    # plt.subplot(1,2,1)
    # for pl in range(NUM_PLAYERS):
    #     hp1 = hist[ hist[:,0] == pl ] # when they were first player
    #     hp2 = hist[ hist[:,4] == pl]   # when they were second player
    #     rewards1 = hp1[:,3]
    #     # try e catch because rewars1 can have zero shape
    #     try:
    #         rewards2 = rewards1[-1] + hp2[:,7] # had to add a costant term 
    #     except:
    #         rewards2 = hp2[:,7]
    #     rewards = np.concatenate((rewards1, rewards2), axis = 0)
    #     plt.plot(rewards) # plot only when they were pl1 and pl2
    # plt.title("{} players game".format(NUM_PLAYERS))
    # plt.xlabel('Iteration')
    # plt.ylabel('Cum. reward')
    # plt.legend(["P"+str(i)+" "+snames[i].replace('ainly','') for i in range(NUM_PLAYERS)])
    # plt.subplot(1,2,2)
    # coop_h = []
    # def_h = []
    # time = []
    # for i in range(0, int(hist.shape[0]/NUM_PLAYERS)):
    #     coop = (sum(1 if x==0 else 0 for x in hist[:,1][i:i+10])/NUM_PLAYERS)
    #     def_h.append(1-coop)
    #     coop_h.append(coop)
    #     time.append(i)
    # plt.ylim(top=1.1)
    # plt.ylim(bottom=-0.1)
    # plt.plot(time,coop_h,'r')
    # plt.plot(time,def_h)
    # plt.legend(['Cooperate','Deflect'])
    # plt.title('Percentage of cooperation/deflection')
    # #plt.show()
    # plt.savefig('../img/idpmp-rewards-{}.png'.format( '-'.join(snames_stripped) ))
    # plt.close()

if __name__ == "__main__":
    main()
