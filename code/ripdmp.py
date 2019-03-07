import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ipdmp import IPDRoundRobin
from mgen import generatePayoffMatrix
from strategy import *

def IPDRR(k_strategies, num_iter, against_itself=False):
    """REMOVE. Original in ipdmp is used instead (same code)."""

    n = k_strategies.size
    #num_rounds = int( ((n-1)/2) * n)

    # initialize players with given strategies
    players = np.array([ MultiPlayer(k) for k in k_strategies ])

    # todo: for _ in range(NUM_REPETITIONS): -> CLEVER but get_points needs change

    # each player plays against another in a round robin scheme
    for (i, p1) in zip(np.arange(n), players):
        start = i if against_itself else i+1
        for (j, p2) in zip(np.arange(start, n), players[start:]):
            p1.play_iter(p2, num_iter)

    # calculate ranking and matches dataframes
    # has to be done after the tournament

    ranking_df = pd.DataFrame() # all points gained by players
    matches_df = pd.DataFrame() # all matches played sorted by time

    for (i, p) in zip(np.arange(n), players):
        points = p.get_points_alt()
        df = pd.DataFrame(
            [[p.s, int(points[-1]), p]],
            columns=['Player','points', 'rrp']
        )
        ranking_df = ranking_df.append(df)
        ranking_df = ranking_df.sort_values(['points'], ascending=[False])

        for j in range(i, len(p.results)):
            # can now access any property from p1 or p2 for plots
            # each match can be explored

            df = pd.DataFrame(
                    [[p.s, p.prevOpponent[j].s, p.results[j], p.prevOpponent[j].results[i]]],
                    columns=['p1','p2','p1-score','p2-score']
            )
            matches_df = matches_df.append(df)
    
    players = np.array(ranking_df['rrp'])
    ranking_df = ranking_df[['Player','points']]    
    return players, ranking_df, matches_df
    
def main():
    np.random.seed(100)
    pd.set_option('display.max_columns', None)

    NUM_ITER = 100
    NUM_PLAYERS = 50
    PERCENTAGE = 0.3
    print("Testing repeated round-robin tournament with {}-people".format(NUM_PLAYERS))

    repeated_players = []
    prev_winning_k = None

    # random initialization of NUM_PLAYERS-6 agents 
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
    while not np.array_equal(k_strategies, np.repeat(k_strategies[0], k_strategies.size)):
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
            pl_strat_str = str(players[i].s)
            if pl_strat_str == 'TitForTat':
                value = TFT
            elif pl_strat_str == 'TitFor2Tat':
                value = TF2T
            elif pl_strat_str == 'GrimTrigger':
                value = GRT
            else:
                value = players[i].s.k
            k_strategies = np.append(k_strategies, value)
            
            pl_strat_str = str(players[NUM_PLAYERS-i-1].s)
            if pl_strat_str == 'TitForTat':
                value = TFT
            elif pl_strat_str == 'TitFor2Tat':
                value = TF2T
            elif pl_strat_str == 'GrimTrigger':
                value = GRT
            else:
                value = players[NUM_PLAYERS-i-1].s.k
            k_strategies = np.delete(k_strategies,np.argmax(value))

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
            points = p.get_points_alt()
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
