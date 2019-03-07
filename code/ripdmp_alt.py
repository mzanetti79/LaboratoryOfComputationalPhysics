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
    NUM_PLAYERS = 8
    NUM_REPETITIONS = 10
    print("Testing repeated round-robin tournament with {}-people".format(NUM_PLAYERS))

    repeated_players = []
    prev_winning_k = None
    #k = 5
    # random initialization of NUM_PLAYERS-6 agents
    # k_strategies = Strategy.generatePlayers(NUM_PLAYERS, replace=False)
    k_strategies = Strategy.generatePlayers(8, replace=False, fixed=True) #GENERATE STRATEGIES WRONG
    strategies_df = pd.DataFrame() # strategies evolution

    for _ in range(NUM_REPETITIONS):
        players, ranking_df, matches_df = IPDRoundRobin(k_strategies, NUM_ITER) # no strategy change, not against itself
        repeated_players.append(players)

        score = ranking_df.groupby(['labels'], as_index = False).sum()
        total_score = np.sum(score['points']) # total score
        score['percentage'] = round((score['points']/total_score*10)**2) # ^2 to evaluate the difference
        #
        for index, row in score.iterrows():
            k_strategies = np.append(k_strategies, np.repeat(row['labels'], row['percentage']))


        # create strategies history
        unique, counts = np.unique(k_strategies, return_counts=True)
        df = pd.DataFrame([counts],columns=unique)
        strategies_df = strategies_df.append(df)

    score = score.sort_values(['points'], ascending = False)
    print(score)
    print(k_strategies)
    print(strategies_df)

        # easy fix (depending on task)
        # add one winner strategy or multiple previous winners?
        # for i in range(0,int(NUM_PLAYERS * PERCENTAGE)):
        #     pl_strat_str = str(players[i].s)
        #     if pl_strat_str == 'TitForTat':
        #         value = TFT
        #     elif pl_strat_str == 'TitFor2Tat':
        #         value = TF2T
        #     elif pl_strat_str == 'GrimTrigger':
        #         value = GRT
        #     else:
        #         value = players[i].s.k
        #     k_strategies = np.append(k_strategies, value)
        #
        #     pl_strat_str = str(players[NUM_PLAYERS-i-1].s)
        #     if pl_strat_str == 'TitForTat':
        #         value = TFT
        #     elif pl_strat_str == 'TitFor2Tat':
        #         value = TF2T
        #     elif pl_strat_str == 'GrimTrigger':
        #         value = GRT
        #     else:
        #         value = players[NUM_PLAYERS-i-1].s.k
        #     k_strategies = np.delete(k_strategies,np.argmax(value))

        # print(matches_df)
        # ranking_df = pd.DataFrame(ranking_df)
        # matches_df = pd.DataFrame(matches_df)
        # display(ranking_df)
        # display(matches_df)

    # print("Convergence speed of round-robin tournament is {} with {}-people".format(NUM_REPETITIONS, NUM_PLAYERS))
    #
    # # save plots
    # strategies_df.index = np.arange(strategies_df.index.size)
    # strategies_df = strategies_df.fillna(0)
    # strategies_df.plot()
    # plt.legend(ncol=int(NUM_PLAYERS/5))
    # plt.title('Strategies evolution')
    # plt.ylabel('Number of strategies')
    # plt.xlabel('Time')
    # plt.show()
    #
    # for (r, players) in zip(np.arange(NUM_REPETITIONS), repeated_players):
    #     for p in players:
    #         points = p.get_points_alt()
    #         plt.plot(points, label=p.s)
    #         plt.title("Multi pl. game: {}".format(NUM_PLAYERS))
    #         plt.xlabel('Match number')
    #         plt.ylabel('Points')
    #
    #     plt.legend()
    #     plt.show()
    #     #plt.savefig('../img/ripdmp-scores-{}-r{}.png'.format(NUM_PLAYERS, r))
    #     #plt.close()

if __name__ == "__main__":
    main()
