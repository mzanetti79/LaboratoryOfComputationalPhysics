from ipdmp import IPDRoundRobin
from strategy import *

def main():
    np.random.seed(100)
    pd.set_option('display.max_columns', None)

    SAVE_IMG = False

    NUM_ITER = 100
    NUM_PLAYERS = 50
    print("Testing repeated round-robin tournament with {}-people".format(NUM_PLAYERS))

    k_strategies = Strategy.generatePlayers(NUM_PLAYERS, replace=(NUM_PLAYERS>Strategy.TOT_STRAT), fixed=True)

    NUM_REPETITIONS = 0
    MAX_ALLOWED = 20
    repeated_players = []
    strategies_df = pd.DataFrame() # strategies evolution

    while np.unique(k_strategies, return_counts=True)[1].max() < k_strategies.size*3/4 and NUM_REPETITIONS < MAX_ALLOWED:
        NUM_REPETITIONS += 1
        # initialize players with given strategies
        players = np.array([MultiPlayer(k) for k in k_strategies])
        
        players, ranking_df, matches_df = IPDRoundRobin(players, NUM_ITER) # no strategy change, not against itself
        repeated_players.append(players)

        score = ranking_df.groupby(['labels'], as_index = False).sum()
        score = score.sort_values(by=['points'], ascending=False)
        # to keep the same stucture as incr_pop
        score['points'] = score.max().points-score['points']
        # score['percentage'] = score['points']/np.sum(score['points'])
        # score['users_to_add'] = round((score['percentage']*len(players)))
        print(score)
        # print('adding this many people: ', score['users_to_add'].sum())
        
        for index, row in score.iterrows():
            draw = np.random.randint(score.max().points)
            # k_strategies = np.append(k_strategies, np.repeat(row['labels'], row['users_to_add']))
            if draw > row['points']:
                k_strategies = np.append(k_strategies, row['labels'])
        # k_strategies = np.append(k_strategies, Strategy.generatePlayers(NUM_PLAYERS, replace=(NUM_PLAYERS>Strategy.TOT_STRAT), fixed=True))

        # create strategies history
        unique, counts = np.unique(k_strategies, return_counts=True)
        df = pd.DataFrame([counts],columns=unique)
        strategies_df = strategies_df.append(df)

    if np.unique(k_strategies, return_counts=True)[1].max() > k_strategies.size*3/4:
        print("Convergence speed of round-robin tournament is {} with {}-people".format(NUM_REPETITIONS, NUM_PLAYERS))
    else:
        print("Convergence not reached")

    print(k_strategies)
    print(strategies_df)

    # save plots
    strategies_df = strategies_df.rename(index=str,
        columns={-3: "TitForTwoTat", -2: "GrimTrigger", -1: "TitForTat", 0: "Nice", 100: "Bad", 50: "Indifferent"})
    strategies_df.index = np.arange(strategies_df.index.size)
    strategies_df = strategies_df.fillna(0)
    strategies_df.plot(figsize=(12,5))
    plt.legend()
    plt.title('Strategies evolution')
    plt.ylabel('Number of strategies')
    plt.xlabel('Time')
    plt.show()
    
    for (r, players) in zip(np.arange(MAX_ALLOWED), repeated_players):
        for p in players:
            points = p.get_points()
            plt.plot(points, label=p.s)
            plt.title("Multi pl. game: {}".format(NUM_PLAYERS))
            plt.xlabel('Match number')
            plt.ylabel('Points')
    
        plt.legend()
        if SAVE_IMG:
            plt.savefig('../img/ripdmp-alt/ripdmp-scores-{}-r{}.eps'.format(NUM_PLAYERS, r),format='eps',bbox_inches='tight')
            plt.close()
        else:
            plt.show()
if __name__ == "__main__":
    main()
