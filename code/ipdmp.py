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
            # todo: for _ in range(NUM_REPETITIONS): -> CLEVER but get_points needs change
            p1.play_iter(p2, num_iter)

    # calculate ranking and matches dataframes
    # has to be done after the tournament

    ranking_df = pd.DataFrame()
    # all matches played sorted by time
    matches_df = pd.DataFrame()

    for (i, p) in zip(np.arange(n), round_robin_p):
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
    
    round_robin_p = np.array(ranking_df['rrp'])
    ranking_df = ranking_df[['Player','points']]    
    return round_robin_p, ranking_df, matches_df
    
def main():
    np.random.seed(100)
    pd.set_option('display.max_columns', None)

    # number of iterations
    NUM_ITER = 50
    # number of players
    NUM_PLAYERS = 10
    # num repetitions
    NUM_REPETITIONS = 10
    print("Testing round-robin tournament with {}-people".format(NUM_PLAYERS))

    repeated_round_robin_p = []

    # define k for strategy probabilities
    # append NUM_PLAYERS-4 strategies with k between 1 and 99 included
    # todo check if replace=True or False
    k_strategies = Strategy.generatePlayers(num_players=NUM_PLAYERS)
    
    for _ in range(NUM_REPETITIONS):
        round_robin_p, ranking_df, matches_df = IPDRoundRobin(k_strategies, NUM_ITER, True)
        repeated_round_robin_p.append(round_robin_p)

        # print(ranking_df.to_latex(index=False))
        # print(matches_df.to_latex(index=False))
    
    # save points and other stuff if necessary
    saved_points = []

    # save plots
    for (r, round_robin_p) in zip(np.arange(NUM_REPETITIONS), repeated_round_robin_p):
        for p in round_robin_p:
            #points = p.get_points()
            points = p.get_points_alt()
            # plt.plot(points, label=p.s)
            # plt.title("Multi pl. game: {}".format(NUM_PLAYERS))
            # plt.xlabel('Match number')
            # plt.ylabel('Points')

            # save points for each repetition
            saved_points.append(int(points[-1]))

        # plt.legend()
        # plt.show()
        #plt.savefig('../img_v1/idpmp-scores-{}.png'.format(NUM_PLAYERS))
        #plt.close()

    one_round_results = []
    for p in round_robin_p:
        one_round_results.append(p.results)

    one_round = pd.DataFrame(one_round_results).T
    meds = one_round.median()
    meds = meds.sort_values(ascending=False)
    one_round = one_round[meds.index]
    one_round.boxplot()
    plt.xticks(np.arange(NUM_PLAYERS)+1, [round_robin_p[p].s for p in meds.index], rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig('../img_v1/idpmp-boxplot-single-match-{}.png'.format(NUM_PLAYERS))
    plt.close()
    
    saved_points = pd.DataFrame(np.reshape(saved_points, (NUM_REPETITIONS, int(len(saved_points)/NUM_REPETITIONS))))
    meds = saved_points.median()
    meds = meds.sort_values(ascending=False,)
    saved_points = saved_points[meds.index]
    saved_points.boxplot()
    plt.xticks(np.arange(NUM_PLAYERS)+1, [round_robin_p[p].s for p in meds.index], rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig('../img_v1/idpmp-boxplot-final-points-{}.png'.format(NUM_PLAYERS))
    plt.close()

if __name__ == "__main__":
    main()
