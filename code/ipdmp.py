import pandas as pd
import matplotlib.pyplot as plt

from mgen import generatePayoffMatrix
from strategy import *

def IPDRoundRobin(k_strategies, num_iter, itself):
    n = num_strat = k_strategies.size
    num_rounds = int( ((n-1)/2) * n)

    # initialize players with given strategies
    round_robin_p = np.array([])
    for k in k_strategies:
        p = MultiPlayer(k)
        round_robin_p = np.append(round_robin_p, p)

    # each player plays against another in a round robin scheme
    for (i, p1) in zip(np.arange(n), round_robin_p):
        #todo reason if A vs A makes sense
        for (j, p2) in zip(np.arange(i if itself else i+1 ,n), round_robin_p[i if itself else i+1:]):
            p1.play_iter(p2, num_iter)

    return round_robin_p
    
def main():
    np.random.seed(100)
    pd.set_option('display.max_columns', None)

    # number of iterations
    NUM_ITER = 500
    # number of players
    NUM_PLAYERS = 15

    print("Testing round-robin tournament with {}-people".format(NUM_PLAYERS))

    # define strategies for players
    # -1 = TfT
    # -2 = random
    #k_strategies = np.random.choice([0, 100, 50, -1, -2, -2], NUM_PLAYERS)
    #mask = k_strategies == -2
    #k_strategies[mask] = np.random.randint(1,100,size=np.sum(mask))

    # define k for strategy probabilities
    # use k=-1 for TfT
    k = []
    for i in range(NUM_PLAYERS-4):
        k.append(np.random.randint(1,100))
    k_strategies = np.append(np.array([0, 100, 50, -1]), k)
    
    round_robin_p = IPDRoundRobin(k_strategies, NUM_ITER, True)

    # serie A table
    # todo: store final rewards sum as well as opponent rewards sum
    # (Goal Fatti, Goal Subiti)
    ranking_df = pd.DataFrame()
    # all matches played sorted by time
    matches_df = pd.DataFrame()

    for (i, p) in zip(np.arange(NUM_PLAYERS), round_robin_p):
        #points = p.get_points()
        points = p.get_points_alt()
        plt.plot(points, label=p.s)
        plt.title("Multi pl. game: {}".format(NUM_PLAYERS))
        plt.xlabel('Match number')
        plt.ylabel('Points')

        df = pd.DataFrame(
            [[p.s, p.count_wins(), p.count_draws(), p.count_losses(), int(points[-1])]],
            columns=['Player','W','D','L','points']
        )
        ranking_df = ranking_df.append(df)

        for j in range(i, len(p.results)):
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
    #plt.savefig('../img_v1/idpmp-scores-{}.png'.format(NUM_PLAYERS))
    #plt.close()

    ranking_df = ranking_df.sort_values(['W', 'D', 'L','points'], ascending=[False, False, False, False])

    # print(ranking_df)
    print(ranking_df.to_latex(index=False))
    # print(matches_df)
    print(matches_df.to_latex(index=False))
    # ranking_df = pd.DataFrame(ranking_df)
    # matches_df = pd.DataFrame(matches_df)
    # display(ranking_df)
    # display(matches_df)

if __name__ == "__main__":
    main()
