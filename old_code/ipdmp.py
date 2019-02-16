import numpy as np
import matplotlib.pyplot as plt

from mgen import generatePayoffMatrix
from strategy import *

def IPDRoundRobin(m, strategies, num_round):
    num_strat = len(strategies)
    n = num_strat
    actual_round = 0
    index = 0
    num_iter = int((((n-1)/2)*(n))*num_round)
    
    
    m1 = m   # R, S; T, P for player 1
    m2 = m.T # R, T; S, P for player 2

    rewards = np.zeros(num_strat,dtype='int') # cumulative reward for both players
    hist = np.zeros((num_iter,8),dtype='int') # history of moves
    
    while(actual_round < num_round):
        # player1 e.g s1 is index i
        for i in range(num_strat):
            #player2 e.g s2 is index j
            for j in range(num_strat):
                
                if j>i:
                    s1 = strategies[i]
                    s2 = strategies[j]
                    if type(s1) != TitForTat:
                        action1 = s1.get()
                    else:
                        action1 = 0 # cooperate
                        if actual_round > 0:
                            # in RR the other player2 is always the next
                            # that is num_player-1 rows behind in the history
                            # 5 = pl2 last action
                            action1 = s1.get(hist[actual_round*num_strat-num_strat+1,5])
                    # note: by this logic, a TfT class is totally useless 
                    if type(s2) != TitForTat:
                        action2 = s2.get()
                    else:
                        action2 = 0
                        if actual_round > 0:
                            # in RR the other player1 is always the previous
                            # that is num_player+1 row behind in the history
                            # 1 = pl1 last action
                            action2 = s2.get(hist[actual_round*num_strat-num_strat-1,1])

    
                    # get payoffs from matrix, based on chosen actions
                    payoff1 = m1[action1,action2]
                    payoff2 = m2[action1,action2]
                    rewards[i] += payoff1
                    rewards[j] += payoff2
        
                    # save current players, actions, payoffs, cumulative results
                    hist[index] = [i, action1, payoff1, rewards[i],
                                   j, action2, payoff2, rewards[j]]
                    index += 1
                    
        actual_round += 1
    return { 'history': hist, 'total_rewards': rewards }
    
def main():
    # number of rounds and players
    NUM_ROUND = 5
    NUM_PLAYERS = 10

    # define payoff matrix
    M1 = np.array([[2,0],[3,1]]) # one default payoff matrix
    M2 = np.array([[3,0],[5,2]]) # another good choice
    # or use M = generatePayoffMatrix()

    print("Testing {} rounds of {}-people IPD with\nM={}".format(NUM_ROUND, NUM_PLAYERS, M1))

    # define strategies for players
    strategies = []
    for _ in range(NUM_PLAYERS):
        ch = np.random.randint(0,6) # currently 6 possible strategies
        if ch == 0: #Nice
            s = ProbStrategy(0)
        elif ch == 1: #Bad
            s = ProbStrategy(100)
        elif ch == 2: #MNice
            k = np.random.randint(1,50)
            s = ProbStrategy(k)
        elif ch == 3: #MBad
            k = np.random.randint(51,100)
            s = ProbStrategy(k)
        elif ch == 4: #Indifferent
            s = ProbStrategy(50)
        elif ch == 5:
            s = TitForTat()
            
        strategies.append(s)
    
    # save names to display later
    snames = [str(s) for s in strategies]
    snames_stripped = []
    for s in snames:
        if ' (' in s:
            snames_stripped.append(s[0:s.find(' (')])
        else:
            snames_stripped.append(s)

    print("\nStrategies:")
    print("\n".join(snames))

    res_dict = IPDRoundRobin(M1, strategies, NUM_ROUND)
    hist = res_dict['history']

    # plot cumulative rewards
    plt.figure(figsize=(15,5)) 
    plt.subplot(1,2,1)
    for pl in range(NUM_PLAYERS):
        hp1 = hist[ hist[:,0] == pl ] # when they were first player
        hp2 = hist[ hist[:,4] == pl]   # when they were second player
        rewards1 = hp1[:,3]
        # try e catch because rewars1 can have zero shape
        try:
            rewards2 = rewards1[-1] + hp2[:,7] # had to add a costant term 
        except:
            rewards2 = hp2[:,7]
        rewards = np.concatenate((rewards1, rewards2), axis = 0)
        plt.plot(rewards) # plot only when they were pl1 and pl2
    plt.title("{} players game".format(NUM_PLAYERS))
    plt.xlabel('Iteration')
    plt.ylabel('Cum. reward')
    plt.legend(["P"+str(i)+" "+snames[i].replace('ainly','') for i in range(NUM_PLAYERS)])
    plt.subplot(1,2,2)
    coop_h = []
    def_h = []
    time = []
    for i in range(0, int(hist.shape[0]/NUM_PLAYERS)):
        coop = (sum(1 if x==0 else 0 for x in hist[:,1][i:i+10])/NUM_PLAYERS)
        def_h.append(1-coop)
        coop_h.append(coop)
        time.append(i)
    plt.ylim(top=1.1)
    plt.ylim(bottom=-0.1)
    plt.plot(time,coop_h,'r')
    plt.plot(time,def_h)
    plt.legend(['Cooperate','Deflect'])
    plt.title('Percentage of cooperation/deflection')
    #plt.show()
    plt.savefig('../img/idpmp-rewards-{}.png'.format( '-'.join(snames_stripped) ))
    plt.close()

if __name__ == "__main__":
    main()
