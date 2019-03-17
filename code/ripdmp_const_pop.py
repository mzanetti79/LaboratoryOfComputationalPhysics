from strategy import *
from base_options import *
from ipdmp import IPDRoundRobin

def main():
    np.random.seed(100)
    pd.set_option('display.max_columns', None)
    pd.set_option('precision', 2)

    opt = BaseOptions().parse(BaseOptions.RIPDMP_C)
    SAVE_IMG = opt.saveimg
    NUM_ITER = opt.niter
    NUM_PLAYERS = opt.nplay
    NUM_REPETITIONS = opt.nrep
    MAX_ALLOWED = opt.maxrep
    PERCENTAGE = opt.percent
    FIXED = opt.fixed
	
    print("Testing repeated round-robin tournament with {}-people".format(NUM_PLAYERS))

    k_strategies = Strategy.generatePlayers(NUM_PLAYERS, replace=(NUM_PLAYERS>Strategy.TOT_STRAT), fixed=FIXED) # TODO or both fixed or both free

    repeated_players = []
    # strategies evolution
    unique, counts = np.unique(k_strategies, return_counts=True)
    strategies_df = pd.DataFrame([counts],columns=unique)

    while np.unique(k_strategies, return_counts=True)[1].max() < k_strategies.size*3/4 and NUM_REPETITIONS < MAX_ALLOWED:
        NUM_REPETITIONS += 1
        # initialize players with given strategies
        players = np.array([MultiPlayer(k) for k in k_strategies])
        
        players, ranking_df, matches_df = IPDRoundRobin(players, NUM_ITER) # no strategy change, not against itself
        repeated_players.append(players)

        # create strategies history
        unique, counts = np.unique(k_strategies, return_counts=True)
        df = pd.DataFrame([counts],columns=unique)
        strategies_df = strategies_df.append(df)

        # easy fix (depending on task)
        # add one winner strategy or multiple previous winners?
        for i in range(0,int(NUM_PLAYERS * PERCENTAGE)):
            k_strategies = np.append(k_strategies, players[i].s.id)
            k_strategies = np.delete(k_strategies,np.argmax(players[NUM_PLAYERS-i-1].s.id))
        #display(ranking_df)
        # display(matches_df)

    if np.unique(k_strategies, return_counts=True)[1].max() > k_strategies.size*3/4:
        print("Convergence speed of round-robin tournament is {} with {}-people".format(NUM_REPETITIONS, NUM_PLAYERS))
    else:
        print("Convergence not reached")
        
    # save plots
    strategies_df = strategies_df.rename(index=str,
        columns={-3: "GrimTrigger", -2: "TitForTwoTat", -1: "TitForTat", 0: "Nice", 100: "Bad", 50: "Indifferent"})
    for c in strategies_df.columns:
        if str.isdigit(str(c)):
            if c > 50:
                strategies_df = strategies_df.rename(index=str, columns={c: "MainlyBad (k={})".format(c)})
            else:
                strategies_df = strategies_df.rename(index=str, columns={c: "MainlyNice (k={})".format(c)})

    strategies_df.index = np.arange(strategies_df.index.size)
    strategies_df = strategies_df.fillna(0)
    print(strategies_df.to_latex(index=False))
    strategies_df.plot(figsize=(12,5))    
    plt.legend(bbox_to_anchor=(0,-0.1), ncol=5, loc=2)
    plt.title('Strategies evolution')
    plt.ylabel('Number of strategies')
    plt.xlabel('Time')
    if SAVE_IMG:
        plt.savefig('../img/ripdmp-const/ripdmp-evolution-const-pop-{}.eps'.format(NUM_PLAYERS),format='eps',bbox_inches='tight')
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
            plt.savefig('../img/ripdmp-const/ripdmp-scores-const-pop-{}-r{}.eps'.format(NUM_PLAYERS, r),format='eps',bbox_inches='tight')
            plt.close()
        else:
            plt.show()
            
if __name__ == "__main__":
    main()