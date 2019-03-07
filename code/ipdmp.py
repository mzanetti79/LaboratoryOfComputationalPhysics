import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mgen import generatePayoffMatrix
from strategy import *

def IPDRoundRobin(k_strategies, num_iter, changing_str=False, against_itself=False):
    n = k_strategies.size

    # initialize players with given strategies
    players = np.array([ MultiPlayer(k, changing_str) for k in k_strategies ])

    # todo for _ in range(NUM_REPETITIONS): -> CLEVER but get_points needs change

    # each player plays against another in a round robin scheme
    for (i, p1) in zip(np.arange(n), players):
        start = i if against_itself else i+1
        for (j, p2) in zip(np.arange(start, n), players[start:]):
            p1.play_iter(p2, num_iter)

    # for cipdmp: exit without computing points and matches df
    # dirty workaround: fix later when cipdmp points comp is well defined (now they are done in main)
    if changing_str:
        return players

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

    NUM_ITER = 50
    NUM_PLAYERS = 10
    NUM_REPETITIONS = 10
    print("Testing round-robin tournament with {}-people".format(NUM_PLAYERS))

    # define k for strategy probabilities
    # append NUM_PLAYERS-6 strategies with k between 1 and 99 included
    k_strategies = Strategy.generatePlayers(NUM_PLAYERS)
    
    repeated_players = []
    for _ in range(NUM_REPETITIONS):
        players, ranking_df, matches_df = IPDRoundRobin(k_strategies, NUM_ITER) # no strategy change, not against itself
        repeated_players.append(players)

        # print(ranking_df.to_latex(index=False))
        # print(matches_df.to_latex(index=False))
    
    # save points and other stuff if necessary
    saved_points = []

    # save plots
    for (r, players) in zip(np.arange(NUM_REPETITIONS), repeated_players):
        # should we use for players in repeated_players: ? r is not used
        for p in players:
            # save points for each repetition
            points = p.get_points_alt()

            #points = p.get_points()
            # plt.plot(points, label=p.s)
            # plt.title("Multi pl. game: {}".format(NUM_PLAYERS))
            # plt.xlabel('Match number')
            # plt.ylabel('Points')

            saved_points.append(int(points[-1]))

        # plt.legend()
        # plt.show()
        #plt.savefig('../img_v1/idpmp-scores-{}.png'.format(NUM_PLAYERS))
        #plt.close()

    # box plot of single match
    one_round_results = [p.results for p in players]
    one_round = pd.DataFrame(one_round_results).T
    meds = one_round.median().sort_values(ascending=False)
    one_round = one_round[meds.index]
    one_round.boxplot()
    plt.xticks(np.arange(NUM_PLAYERS)+1, [players[p].s for p in meds.index], rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig('../img_v1/idpmp-boxplot-single-match-{}.png'.format(NUM_PLAYERS))
    plt.close()
    
    # box plot of all points
    saved_points = pd.DataFrame(np.reshape(saved_points, (NUM_REPETITIONS, int(len(saved_points)/NUM_REPETITIONS))))
    meds = saved_points.median().sort_values(ascending=False)
    saved_points = saved_points[meds.index]
    saved_points.boxplot()
    plt.xticks(np.arange(NUM_PLAYERS)+1, [players[p].s for p in meds.index], rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig('../img_v1/idpmp-boxplot-final-points-{}.png'.format(NUM_PLAYERS))
    plt.close()

if __name__ == "__main__":
    main()
