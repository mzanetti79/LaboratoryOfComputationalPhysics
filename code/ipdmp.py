import numpy as np
import matplotlib.pyplot as plt

from mgen import generatePayoffMatrix
from strategy import *

def IPDRoundRobin(m, strategies, num_iter):
    if num_iter == 0: return
    num_strat = len(strategies)
    if num_strat == 0: return
    
    m1 = m   # R, S; T, P for player 1
    m2 = m.T # R, T; S, P for player 2

    rewards = np.zeros(num_strat,dtype='int') # cumulative reward for both players
    hist = np.zeros((num_iter,8),dtype='int') # history of moves

    for i in range(num_iter):
        # get strategies of current players
        # round robin = circular
        cur_pl1 = i % num_strat
        cur_pl2 = (i+1) % num_strat
        s1 = strategies[cur_pl1]
        s2 = strategies[cur_pl2]
        
        # get actions, to use as indexes in matrix
        # 0 = coop, 1 = defect
        if type(s1) != TitForTat:
            action1 = s1.get()
        else:
            action1 = 0 # cooperate
            if i > 0:
                # in RR the other player2 is always the next
                # that is num_player-1 rows behind in the history
                # 5 = pl2 last action
                action1 = s1.get(hist[i-num_strat+1,5])
            # note: by this logic, a TfT class is totally useless
        
        if type(s2) != TitForTat:
            action2 = s2.get()
        else:
            action2 = 0
            if i > 0:
                # in RR the other player1 is always the previous
                # that is num_player+1 row behind in the history
                # 1 = pl1 last action
                action2 = s2.get(hist[i-num_strat-1,1])

        # get payoffs from matrix, based on chosen actions
        payoff1 = m1[action1,action2]
        payoff2 = m2[action1,action2]
        rewards[cur_pl1] += payoff1
        rewards[cur_pl2] += payoff2
        
        # save current players, actions, payoffs, cumulative results
        hist[i] = [cur_pl1, action1, payoff1, rewards[cur_pl1],
                   cur_pl2, action2, payoff2, rewards[cur_pl2]]
    return { 'history': hist, 'total_rewards': rewards }
    
def main():
    # number of iterations and players
    NUM_ITER = 10
    NUM_PLAYERS = 10

    # define payoff matrix
    M1 = np.array([[2,0],[3,1]]) # one default payoff matrix
    M2 = np.array([[3,0],[5,2]]) # another good choice
    # or use M = generatePayoffMatrix()

    print("Testing {} iterations of {}-people IPD with\nM={}".format(NUM_ITER, NUM_PLAYERS, M1))

    # define strategies for players
    strategies = []
    for _ in range(NUM_PLAYERS):
        ch = np.random.randint(0,5) # currently 5 possible strategies
        if ch == 0:
            s = NiceStrategy()
        elif ch == 1:
            s = BadStrategy()
        elif ch == 2:
            k = np.random.randint(0,50)
            s = MainlyNiceStrategy(k)
        elif ch == 3:
            k = np.random.randint(50,101)
            s = MainlyBadStrategy(k)
        elif ch == 4:
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

    res_dict = IPDRoundRobin(M1, strategies, NUM_ITER*NUM_PLAYERS)
    hist = res_dict['history']

    # plot cumulative rewards
    plt.figure(figsize=(15,5)) 
    plt.subplot(1,2,1)
    for pl in range(NUM_PLAYERS):
        hp = hist[ hist[:,0] == pl ]
        plt.plot(hp[:,3],'*') # plot only when they were pl1 in the game
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
    plt.plot(time,coop_h,'r')
    plt.plot(time,def_h)
    plt.legend(['Cooperate','Deflect'])
    plt.title('Percentage of cooperation/deflection')
    #plt.show()
    plt.savefig('../img/idpmp-rewards-{}.png'.format( '-'.join(snames_stripped) ))
    plt.close()

if __name__ == "__main__":
    main()