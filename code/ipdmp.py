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

    return round_robin_p
    
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

    # define k for strategy probabilities
    # append NUM_PLAYERS-4 strategies with k between 1 and 99 included
    # todo check if replace=True or False
    k_strategies = Strategy.generatePlayer(NUM_PLAYERS=NUM_PLAYERS)
        
    saved_points = []
    
    for n in range(NUM_REPETITIONS):
        
        # save results in tables
        ranking_df = pd.DataFrame()
        matches_df = pd.DataFrame()
        
        round_robin_p = IPDRoundRobin(k_strategies, NUM_ITER, True)
        
        for (i, p) in zip(np.arange(NUM_PLAYERS), round_robin_p):
            #points = p.get_points()
            points = p.get_points_alt()
            # plt.plot(points, label=p.s)
            # plt.title("Multi pl. game: {}".format(NUM_PLAYERS))
            # plt.xlabel('Match number')
            # plt.ylabel('Points')
            # plt.show()
            # plt.close()

            # save points for each repetition
            saved_points.append(int(points[-1]))
            df = pd.DataFrame(
                [[p.s, int(points[-1])]],
                columns=['Player','points']
            )
            ranking_df = ranking_df.append(df)

            for j in range(i, len(p.results)):
                # can now access any property from p1 or p2 for plots
                # each match can be explored

                df = pd.DataFrame(
                        [[p.s, p.prevOpponent[j].s, p.results[j], p.prevOpponent[j].results[i]]],
                        columns=['p1','p2','p1-score','p2-score']
                )
                matches_df = matches_df.append(df)
        # plt.legend()
        # plt.show()
        #plt.savefig('../img_v1/idpmp-scores-{}.png'.format(NUM_PLAYERS))
        #plt.close()

        ranking_df = ranking_df.sort_values(['points'], ascending=[False])

        # print(ranking_df)
        # print(ranking_df.to_latex(index=False))
        # print(matches_df)
        # print(matches_df.to_latex(index=False))
        # ranking_df = pd.DataFrame(ranking_df)
        # matches_df = pd.DataFrame(matches_df)
        #display(ranking_df)
        #display(matches_df)
    
    players_results = []
    for i in round_robin_p:
        players_results.append(i.results)

    one_round = pd.DataFrame(players_results).T
    meds = one_round.median()
    meds = meds.sort_values(ascending=False)
    one_round = one_round[meds.index]
    one_round.boxplot()
    plt.xticks(np.arange(NUM_PLAYERS)+1, [round_robin_p[p].s for p in meds.index], rotation=90)
    plt.show()
    plt.savefig('../img_v1/idpmp-boxplot-single-match-{}.png'.format(NUM_PLAYERS))
    plt.close()
    
    saved_points = pd.DataFrame(np.reshape(saved_points, (NUM_REPETITIONS, int(len(saved_points)/NUM_REPETITIONS))))
    meds = saved_points.median()
    meds = meds.sort_values(ascending=False,)
    saved_points = saved_points[meds.index]
    # plt.figure(figsize=(10,6))
    saved_points.boxplot()
    plt.xticks(np.arange(NUM_PLAYERS)+1, [round_robin_p[p].s for p in meds.index], rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig('../img_v1/idpmp-boxplot-final-points-{}.png'.format(NUM_PLAYERS))
#    plt.close()
#
if __name__ == "__main__":
    main()
