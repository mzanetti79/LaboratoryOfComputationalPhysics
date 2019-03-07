import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ipdmp import IPDRoundRobin
from mgen import generatePayoffMatrix
from strategy import *
    
def main():
    np.random.seed(100)
    pd.set_option('display.max_columns', None)

    NUM_ITER = 100
    NUM_PLAYERS = 50
    PERCENTAGE = 0.3
    print("Testing repeated round-robin tournament with {}-people".format(NUM_PLAYERS))

    repeated_players = []

    k_strategies = Strategy.generatePlayers(NUM_PLAYERS, replace=True)
    
    strategies_df = pd.DataFrame() # strategies evolution

    # equal split initialization
    #kH = np.random.randint(51,100)
    #kL = np.random.randint(0,50)
    #k_strategies = [0, 100, kL, kH, 50, -1]
    #for i in range(NUM_PLAYERS//6-1):
    #    k_strategies.extend(k_strategies)
    #if(NUM_PLAYERS%6 != 0):
    #    k_strategies.extend(k_strategies[:(NUM_PLAYERS)%6])
    #k_strategies = np.array(k_strategies)

    NUM_REPETITIONS = 0
    # while not np.array_equal(k_strategies, np.repeat(k_strategies[0], k_strategies.size)):
    # this is the largest number of elements of a strategy
    while np.unique(k_strategies, return_counts=True)[1].max() < k_strategies.size*3/4:
        print(k_strategies.size, k_strategies.size*3/4, np.unique(k_strategies, return_counts=True)[1].max())
        print(k_strategies)
        NUM_REPETITIONS += 1
        players, ranking_df, matches_df = IPDRoundRobin(k_strategies, NUM_ITER) # no strategy change, not against itself
        repeated_players.append(players)

        # create strategies history
        unique, counts = np.unique(k_strategies, return_counts=True)
        df = pd.DataFrame([counts],columns=unique)
        strategies_df = strategies_df.append(df)
        
        # easy fix (depending on task)
        # add one winner strategy or multiple previous winners?
        for i in range(0,int(NUM_PLAYERS * PERCENTAGE)):
            k_strategies = np.append(k_strategies, players[i].s.id)
            k_strategies = np.delete(k_strategies,np.argmax(players[NUM_PLAYERS-i-1].s.id))

        # print(matches_df)
        # ranking_df = pd.DataFrame(ranking_df)
        # matches_df = pd.DataFrame(matches_df)
        # display(ranking_df)
        # display(matches_df)

    print("Convergence speed of round-robin tournament is {} with {}-people".format(NUM_REPETITIONS, NUM_PLAYERS))

    # save plots
    strategies_df.index = np.arange(strategies_df.index.size)
    strategies_df = strategies_df.fillna(0)
    strategies_df.plot()
    plt.legend(ncol=int(NUM_PLAYERS/5))
    plt.title('Strategies evolution')
    plt.ylabel('Number of strategies')
    plt.xlabel('Time')
    plt.show()

    for (r, players) in zip(np.arange(NUM_REPETITIONS), repeated_players):
        for p in players:
            points = p.get_points()
            plt.plot(points, label=p.s)
            plt.title("Multi pl. game: {}".format(NUM_PLAYERS))
            plt.xlabel('Match number')
            plt.ylabel('Points')

        plt.legend()
        plt.show()
        #plt.savefig('../img/ripdmp-scores-{}-r{}.png'.format(NUM_PLAYERS, r))
        #plt.close()

if __name__ == "__main__":
    main()
