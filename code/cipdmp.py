from ipdmp import IPDRoundRobin
from strategy import *
def main():
    np.random.seed(100)
    pd.set_option('display.max_columns', None)

    SAVE_IMG = False

    NUM_ITER = 50
    NUM_PLAYERS = 10
    NUM_REPETITIONS = 0
    MAX_ALLOWED = 10
    print("Testing changing round-robin tournament with {}-people".format(NUM_PLAYERS))

    repeated_players = []
    strategies_df = pd.DataFrame() # strategies evolution

    # define k for strategy probabilities
    k_strategies = Strategy.generatePlayers(NUM_PLAYERS,replace=(NUM_PLAYERS > Strategy.TOT_STRAT))

    # initialize players with given strategies
    players = np.array([MultiPlayer(k, changing=True) for k in k_strategies])
    while np.unique(k_strategies, return_counts=True)[1].max() < k_strategies.size*3/4 and NUM_REPETITIONS < MAX_ALLOWED:
        NUM_REPETITIONS += 1
        
        #plot population per strategy
        #total payoff evolution
        players, ranking_df, matches_df = IPDRoundRobin(players, NUM_ITER) # no strategy change, not against itself
        repeated_players.append(players)

        # create strategies history
        unique, counts = np.unique(k_strategies, return_counts=True)
        df = pd.DataFrame([counts],columns=unique)
        strategies_df = strategies_df.append(df)
    
        k_strategies = []
        for i in range(0,len(players)):
            draw = np.random.uniform(0,1)
            if(draw > i/len(players)):
                k_strategies.append(players[i].s.id)
        k_strategies = np.array(k_strategies)
        playersToAdd = np.array([MultiPlayer(k, changing=True) for k in k_strategies])

        players = MultiPlayer.change_strategy(players)

        players = np.append(players, playersToAdd)
        
    if SAVE_IMG:
        plt.savefig('../img/cipdmp_elia/cipdmp-scores-{}.png'.format(NUM_PLAYERS))
        plt.close()
    else:
        plt.show()
        
if __name__ == "__main__":
    main()