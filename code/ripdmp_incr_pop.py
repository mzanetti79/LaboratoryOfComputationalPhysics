from strategy import *
from base_options import *
from ipdmp import IPDRoundRobin
from player import MultiPlayer

def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('precision', 2)

    opt = BaseOptions().parse(BaseOptions.RIPDMP_I)
    NUM_ITER = opt.niter
    NUM_PLAYERS = opt.nplay
    NUM_REPETITIONS = 0 # arg override
    MAX_ALLOWED = opt.maxrep
    ALTERNATIVE = opt.altern
    PERCENTAGE = opt.percent
    FIXED = opt.fixed
    SAVE_IMG = opt.saveimg
    LATEX = opt.latex
    np.random.seed(opt.seed) # None = clock, no-number = 100

    print("Testing repeated round-robin tournament with {}-people".format(NUM_PLAYERS))

    # define initial population
    k_strategies = Strategy.generatePlayers(NUM_PLAYERS, replace=(NUM_PLAYERS > Strategy.TOT_STRAT), fixed=FIXED)

    repeated_players = [] # strategies evolution
    unique, counts = np.unique(k_strategies, return_counts=True)
    strategies_df = pd.DataFrame([counts],columns=unique)
    strategies_df['count'] = counts.sum()

    while np.unique(k_strategies, return_counts=True)[1].max() < k_strategies.size*3/4 and NUM_REPETITIONS < MAX_ALLOWED:
        NUM_REPETITIONS += 1
        print("Reached rep {} of max {} - pop = {}".format(NUM_REPETITIONS, MAX_ALLOWED, k_strategies.size))

        # initialize players with given strategies
        players = np.array([MultiPlayer(k) for k in k_strategies])

        if ALTERNATIVE == 3:
            players, ranking_df = IPDRoundRobin(players, NUM_ITER, return_ranking=True) # no strategy change, not against itself

            score = ranking_df.groupby(['labels'], as_index=False).sum()
            score = score.sort_values(by=['points'], ascending=False)
            score['points'] = score.max().points-score['points']  # For this reason we go from 0
            score['percentage'] = score['points']/score.max().points
            print(score) # TODO delete after tests
        else:
            players = IPDRoundRobin(players, NUM_ITER)
        repeated_players.append(players)

        for i in range(len(players)):
            draw = np.random.uniform(0,1)
            if ALTERNATIVE == 1:
                if draw > i/len(players):
                    k_strategies = np.append(k_strategies, players[i].s.id)

            elif ALTERNATIVE == 2:
                if i < int(NUM_PLAYERS * PERCENTAGE):
                   if draw > 0.2:
                       k_strategies = np.append(k_strategies, players[i].s.id)
                elif i < 2*int(NUM_PLAYERS * PERCENTAGE):
                   if draw > 0.5:
                       k_strategies = np.append(k_strategies, players[i].s.id)
                else:
                   if draw > 0.8:
                       k_strategies = np.append(k_strategies, players[i].s.id)

            elif ALTERNATIVE == 3:
                if draw > score[score['labels']==players[i].s.id].percentage.item():
                    k_strategies = np.append(k_strategies, players[i].s.id)

        # create strategies history
        unique, counts = np.unique(k_strategies, return_counts=True)
        df = pd.DataFrame([counts], columns=unique)
        df['count'] = counts.sum()
        strategies_df = strategies_df.append(df)

    if np.unique(k_strategies, return_counts=True)[1].max() >= k_strategies.size*3/4:
        print("Convergence speed of round-robin tournament is {} with {}-people".format(NUM_REPETITIONS, NUM_PLAYERS))
    else:
        print("Convergence not reached")

    # save plots
    strategies_df = strategies_df.rename(index=str,
        columns={-3: "GrimTrigger", -2: "TitFor2Tat", -1: "TitForTat", 0: "Nice", 100: "Bad", 50: "Indifferent"})
    for c in strategies_df.columns:
        if str.isdigit(str(c)):
            if c > 50:
                strategies_df = strategies_df.rename(index=str, columns={c: "MainlyBad (k={})".format(c)})
            else:
                strategies_df = strategies_df.rename(index=str, columns={c: "MainlyNice (k={})".format(c)})

    strategies_df.index = np.arange(strategies_df.index.size)
    strategies_df = strategies_df.fillna(0).astype(int)
    if LATEX:
        if NUM_PLAYERS > 8:
            print(strategies_df.T.to_latex()) # too large, transpose
        else:
            print(strategies_df.to_latex(index=False))
    else:
        print(strategies_df)

    fig = strategies_df.drop(columns=["count"]).plot(figsize=(12,5))
    plt.legend(bbox_to_anchor=(0,-0.1), ncol=5, loc=2)
    plt.title('Strategies evolution')
    plt.ylabel('Number of strategies')
    plt.xlabel('Time')
    fig.xaxis.set_major_locator(MaxNLocator(integer=True))
    if SAVE_IMG:
        plt.savefig('../img/ripdmp-incr/ripdmp-evolution-increasing-pop-{}.eps'.format(NUM_PLAYERS),format='eps',bbox_inches='tight')
        plt.close()
    else:
        plt.show()

    for (r, players) in zip(np.arange(NUM_REPETITIONS), repeated_players):
        plt.figure(figsize=(12,5))
        for p in players:
            points = p.get_points()
            plt.plot(points, label=p.s)
            plt.title("Multi pl. game: {}".format(NUM_PLAYERS))
            plt.xlabel('Match number')
            plt.ylabel('Points')
        plt.legend(bbox_to_anchor=(0,-0.1), ncol=5, loc=2)

        if SAVE_IMG:
            plt.savefig('../img/ripdmp-incr/ripdmp-scores-increasing-pop-{}-r{}.eps'.format(NUM_PLAYERS, r),format='eps',bbox_inches='tight')
            plt.close()
        else:
            plt.show()

if __name__ == "__main__":
    main()
