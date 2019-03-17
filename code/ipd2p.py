from strategy import *
from base_options import *

def main():
    np.random.seed(100)
    opt = BaseOptions().parse(BaseOptions.IPD2P)
	
    SAVE_IMG = opt.saveimg

    NUM_ITER = opt.niter
    NUM_PLAYERS = opt.nplay
    NUM_REPETITIONS = opt.nrep
    FIXED = opt.fixed
    LATEX = opt.latex

    print("Testing {} iterations of 2-people IPD".format(NUM_ITER))

    # define k for strategy probabilities
    k_strategies = Strategy.generatePlayers(NUM_PLAYERS, replace=(NUM_PLAYERS>Strategy.TOT_STRAT), fixed = FIXED)
    matches_df = pd.DataFrame() # all matches played
                 
    for first in range(NUM_PLAYERS):
        for second in range(first, NUM_PLAYERS):
            k1 = k_strategies[first]
            k2 = k_strategies[second]

            p1 = Player(k1)
            p2 = Player(k2)
            rew1 = np.zeros_like(NUM_ITER)
            rew2 = np.zeros_like(NUM_ITER)
            print("Evaluating {} - {}...".format(p1.s, p2.s))

            # repeat the match to get some statistics (mean and std)
            cum_results = { k1:[], k2:[] }
            yields = {k1:[], k2:[]}
            achieves = {k1:[], k2:[]}
            for _ in range(NUM_REPETITIONS):
                p1.clear_history()
                p2.clear_history()
                p1.play_iter(p2, NUM_ITER)
            
                rew1 = np.cumsum(p1.payoffHist)
                rew2 = np.cumsum(p2.payoffHist)
                yield1 = np.cumsum(p1.bestGivenOther)
                yield2 = np.cumsum(p2.bestGivenOther)
                best1 = np.cumsum(p1.bestAch)
                best2 = np.cumsum(p2.bestAch)
                
                cum_results[k1].append(rew1[-1])
                cum_results[k2].append(rew2[-1])
                yields[k1].append(rew1[-1]/yield1[-1])
                yields[k2].append(rew2[-1]/yield2[-1])
                achieves[k1].append(rew1[-1]/best1[-1])
                achieves[k2].append(rew2[-1]/best2[-1])
                
            # table
            df = pd.DataFrame(
                [[p1.s, p2.s, 
                np.mean(cum_results[k1]), np.std(cum_results[k1]), 
                np.mean(yields[k1])*100, np.mean(achieves[k1])*100,
                np.mean(cum_results[k2]), np.std(cum_results[k2]),
                np.mean(yields[k2])*100, np.mean(achieves[k2])*100]],
                columns=['p1','p2','p1-avg','p1-std', 'p1-yield', 'p1-achieves',
                         'p2-avg', 'p2-std','p2-yield', 'p2-achieves']
            )
            matches_df = matches_df.append(df)

            # boxplots for 100 matches -> A vs B
            plt.boxplot([cum_results[k1], cum_results[k2]])
            plt.xticks([1, 2], [p1.s, p2.s])
            plt.ylabel('Reward')
            plt.title("Meand and std for {} iterations".format(NUM_REPETITIONS))
            if SAVE_IMG:
                plt.savefig('../img/ipd2p/ipd2p-boxplot-{}-{}.eps'.format(str(p1.s).replace(" ",""),str(p2.s).replace(" ","")),format='eps',bbox_inches='tight')
                plt.close()
            else:
                plt.show()
            
            # plot cumulative rewards
            # show only the last iteration's plot
            plt.figure(figsize=(12,5))    
            plt.plot(rew1)
            plt.plot(rew2)
            for i in range(rew1.size):
                if p1.playedHist[i] == COOPERATE:
                    plt.plot(i, rew1[i], 'bx', markersize=8)
                else:
                    plt.plot(i, rew1[i], 'rx', markersize=8)

                if p2.playedHist[i] == COOPERATE:
                    plt.plot(i, rew2[i], 'bo', markersize=5)
                else:
                    plt.plot(i, rew2[i], 'ro', markersize=5)

            plt.title("2 pl. game: {} - {}".format(p1.s,p2.s))
            plt.xlabel('Iteration')
            plt.ylabel('Cum. reward')
            plt.legend(handles=[
                Line2D([0], [0], color='w', marker='x', label='P.1 Defect', markeredgecolor='r'), 
                Line2D([0], [0], color='w', marker='x', label='P.1 Cooperate', markeredgecolor='b'),      
                Line2D([0], [0], color='w', marker='o', label='P.2 Defect', markerfacecolor='r'), 
                Line2D([0], [0], color='w', marker='o', label='P.2 Cooperate', markerfacecolor='b')
            ])

            if SAVE_IMG:
                plt.savefig('../img/ipd2p/ipd2p-rewards-{}-{}.eps'.format(str(p1.s).replace(" ",""),str(p2.s).replace(" ","")),format='eps',bbox_inches='tight')
                plt.close()
            else:
                plt.show()

    pd.set_option('precision', 2)
    if LATEX:
        print(matches_df.to_latex(index=False))
    else:
        print(matches_df)

if __name__ == "__main__":
    main()