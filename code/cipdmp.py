import os
from strategy import *
from base_options import *
from ipdmp import IPDRoundRobin
from player import MultiPlayer

def main():
    root = os.path.dirname(os.path.abspath(__file__))[:-5]

    opt = BaseOptions().parse(BaseOptions.CIPDMP)
    NUM_ITER = opt.niter
    NUM_PLAYERS = opt.nplay
    NUM_REPETITIONS = -1 # arg override
    MAX_ALLOWED = opt.maxrep
    ALTERNATIVE = opt.altern
    FIXED = opt.fixed
    SAVE_IMG = opt.saveimg
    LATEX = opt.latex
    np.random.seed(opt.seed) # None = clock, no-number = 100

    print("Testing changing round-robin tournament with {}-people".format(NUM_PLAYERS))

    if ALTERNATIVE < 1 or ALTERNATIVE > 2:
        print("Wrong alternative. Possible values: 1 or 2. Exiting")
        return

    # define initial population
    k_strategies = Strategy.generatePlayers(NUM_PLAYERS,replace=(NUM_PLAYERS > Strategy.TOT_STRAT), fixed=FIXED)
    players = np.array([MultiPlayer(k, changing=True) for k in k_strategies])

    repeated_players = [] # strategies evolution
    strategies_df = pd.DataFrame()

    while np.unique(players, return_counts=True)[1].max() < players.size*3/4 and NUM_REPETITIONS < MAX_ALLOWED:
        NUM_REPETITIONS += 1
        print("Reached rep {} of max {} - pop = {}".format(NUM_REPETITIONS, MAX_ALLOWED, players.size))

        players = IPDRoundRobin(players, NUM_ITER)
        repeated_players.append(players)

        # get changes in strategies and accumulate in the dataframe
        unique, counts = np.unique(k_strategies, return_counts=True)
        df = pd.DataFrame([counts], columns=unique)
        if strategies_df.size > 0:
            # get stripped version of previous run, add this run (cumulative approach)
            temp = strategies_df.tail(1).drop(columns=["count", "more_coop", "less_coop"])
            df = temp.add(df, fill_value=0).astype(int)
        df['count'] = players.size # complete with other data

        # add new players as per ripdmp (incr. population) alternative 1
        k_strategies = []
        for i in range(len(players)):
            draw = np.random.uniform(0,1)
            if draw > i/len(players):
                k_strategies.append(players[i].s.id)
        k_strategies = np.array(k_strategies)
        players_to_add = np.array([MultiPlayer(k, changing=True) for k in k_strategies])

        players, count_bad, count_good = MultiPlayer.change_strategy(players, FIXED, ALTERNATIVE)
        players = np.append(players, players_to_add)

        df['more_coop'] = count_good
        df['less_coop'] = count_bad
        strategies_df = strategies_df.append(df,sort=True) # sort fixes FutureWarning
        print("{} players changed to more cooperative, {} to less cooperative.".format(count_good, count_bad))

    if np.unique(players, return_counts=True)[1].max() >= players.size*3/4:
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

    # move count columns to the end
    tmp = strategies_df[['count','more_coop','less_coop']]
    strategies_df = strategies_df.drop(columns=['count','more_coop','less_coop'])
    strategies_df[['count','more_coop','less_coop']] = tmp
    
    if LATEX:
        print(strategies_df.T.to_latex())
    else:
        print(strategies_df.T)
    #strategies_df.T.to_excel("Alt{}.xlsx".format(ALTERNATIVE)) # DEBUG only

    fig = strategies_df.drop(columns=["count", "more_coop", "less_coop"]).plot(figsize=(12,5))
    plt.legend(bbox_to_anchor=(0,-0.1), ncol=5, loc=2)
    plt.title('Strategies evolution')
    plt.ylabel('Number of strategies')
    plt.xlabel('Time')
    fig.xaxis.set_major_locator(MaxNLocator(integer=True))
    if SAVE_IMG:
        plt.savefig('{}/img/cipdmp-incr/alt{}/cipdmp-evolution-increasing-pop-{}.eps'.format(root, ALTERNATIVE, NUM_PLAYERS),format='eps',bbox_inches='tight')
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
            plt.savefig('{}/img/cipdmp-incr/alt{}/cipdmp-scores-increasing-pop-{}-r{}.eps'.format(root, ALTERNATIVE, NUM_PLAYERS, r),format='eps',bbox_inches='tight')
            plt.close()
        else:
            plt.show()

if __name__ == "__main__":
    main()
