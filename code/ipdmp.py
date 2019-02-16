import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mgen import generatePayoffMatrix
from strategy import *

def IPDRoundRobin(k_strategies, num_iter):
    n = num_strat = k_strategies.size
    num_rounds = int( ((n-1)/2) * n)

    # initialize players with given strategies
    round_robin_p = np.array([])
    for k in k_strategies:
        p = MultiPlayer(k)
        round_robin_p = np.append(round_robin_p, p)

    # each player plays against another in a round robin scheme
    for (i, p1) in zip(np.arange(n), round_robin_p):
        for (j, p2) in zip(np.arange(i+1,n), round_robin_p[i+1:]):
            # print(i, j)
            p1.play_iter(p2, num_iter)

    return round_robin_p
    
def main():
    np.random.seed(1234)
    pd.set_option('display.max_columns', None)

    # number of iterations
    NUM_ITER = 50
    # number of players
    NUM_PLAYERS = 10

    print("Testing round-robin tournament with {}-people".format(NUM_PLAYERS))

    # define strategies for players
    # -1 = TfT
    # -2 = random
    k_strategies = np.random.choice([0, 100, 50, -1, -2, -2], NUM_PLAYERS)
    mask = k_strategies == -2
    k_strategies[mask] = np.random.randint(1,100,size=np.sum(mask))

    round_robin_p = IPDRoundRobin(k_strategies, NUM_ITER)

    # serie A table
    # todo: store final rewards sum as well as opponent rewards sum
    # (Goal Fatti, Goal Subiti)
    ranking_df = pd.DataFrame()
    # all matches played sorted by time
    matches_df = pd.DataFrame()

    for (i, p) in zip(np.arange(NUM_PLAYERS), round_robin_p):

        points = np.zeros(len(p.results))
        points[np.array(p.results) == 'd'] = 1
        points[np.array(p.results) == 'w'] = 3
        points[np.array(p.results) == 'l'] = 0
        points = np.cumsum(points)
        plt.plot(points, label=p.s)
        plt.title("Multi pl. game: {}".format(NUM_PLAYERS))
        plt.xlabel('Match number')
        plt.ylabel('Points')

        df = pd.DataFrame(
            [[p.s, p.count_wins(), p.count_draws(), p.count_losses(), int(points[-1])]],
            columns=['Player','W','D','L','points']
        )
        ranking_df = ranking_df.append(df)

        for j in range(i+1, len(p.results)):
            # can now access any property from p1 or p2 for plots
            # each match can be explored
            # print(i, j)
                df = pd.DataFrame(
                    [[p.s, p.prevOpponent[j].s, p.results[j], p.prevOpponent[j].results[i], np.sum(p.prevPayoffHist[j]), np.sum(p.prevOpponent[j].prevPayoffHist[i])]],
                    columns=['p1','p2','p1-result', 'p2-result','p1-score','p2-score']
                )
                matches_df = matches_df.append(df)

    plt.legend()
    # plt.show()
    plt.savefig('../img_v1/idpmp-scores-{}.png'.format(NUM_PLAYERS))
    plt.close()

    ranking_df = ranking_df.sort_values(['W', 'D', 'L'], ascending=[False, True, True])
    print(ranking_df)
    print(matches_df)

if __name__ == "__main__":
    main()
