from strategy import *
SAVE_IMG = False

def IPDRoundRobin(players, num_iter, against_itself=False, plot=False):
    n = len(players)
    
    # each player plays against another in a round robin scheme
    if(plot):
        plt.figure(figsize=(12,5))
    
    p = {obj:[0] * num_iter for obj in players}
    
    for (i, p1) in zip(np.arange(n), players):
        start = i if against_itself else i+1
        for (j, p2) in zip(np.arange(start, n), players[start:]):
            p1.clear_history()
            p2.clear_history()
            p1.play_iter(p2, num_iter)
            if(plot):
                p[p1] += np.cumsum(p1.payoffHist)
                p[p2] += np.cumsum(p2.payoffHist)
                
    if plot:
        for i in p:
            plt.plot(p[i],label=i.s)
            plt.xlabel('Iteration')
            plt.ylabel('Cum. reward')
        plt.title("Evolution of the game")
        plt.legend( bbox_to_anchor=(1, 1))
        if SAVE_IMG:
            plt.savefig('../img/ipdmp/ipdmp-evolution-of-game-{}.eps'.format(len(p)),format='eps')
            plt.close()
        else:
            plt.show()


    # calculate ranking and matches dataframes
    # has to be done after the tournament
    ranking_df = pd.DataFrame() # all points gained by players
    matches_df = pd.DataFrame() # all matches played sorted by time

    for (i, p) in zip(np.arange(n), players):
        points = p.get_points()
        df = pd.DataFrame(
            [[p.s, int(points[-1]), p, p.s.id]],
            columns=['Player','points', 'rrp', 'labels']
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

    players = np.array(ranking_df['rrp'])

    ranking_df = ranking_df[['Player','points', 'labels']]
    return players, ranking_df, matches_df

def main():
    np.random.seed(100)
    pd.set_option('display.max_columns', None)

    NUM_ITER = 50
    NUM_PLAYERS = 20
    NUM_REPETITIONS = 10
    print("Testing round-robin tournament with {}-people".format(NUM_PLAYERS))

    # define k for strategy probabilities
    k_strategies = Strategy.generatePlayers(NUM_PLAYERS, replace=(NUM_PLAYERS > Strategy.TOT_STRAT))

    repeated_players = []
    for i in range(NUM_REPETITIONS):
        # initialize players with given strategies
        players = np.array([MultiPlayer(k) for k in k_strategies])
        
        players, ranking_df, matches_df = IPDRoundRobin(players, NUM_ITER, plot=(i==(NUM_REPETITIONS-1))) # no strategy change, not against itself
        repeated_players.append(players)

        # print(ranking_df.to_latex(index=False))
        # print(matches_df.to_latex(index=False))

    # save points and other stuff if necessary
    saved_points = []

    # save plots
    for players in repeated_players:
        for p in players:
            # save points for each repetition
            points = p.get_points()
            saved_points.append(int(points[-1]))

    # box plot of single match
    one_round_results = [p.results for p in players]
    one_round = pd.DataFrame(one_round_results).T
    meds = one_round.median().sort_values(ascending=False)
    one_round = one_round[meds.index]
    one_round.boxplot()
    plt.xticks(np.arange(NUM_PLAYERS)+1, [players[p].s for p in meds.index], rotation=90)
    plt.suptitle('Mean and variance for each type vs the other players \n One complete round')
    plt.ylabel('Points')
    plt.xlabel('Player')
    if SAVE_IMG:
        plt.savefig('../img/ipdmp/ipdmp-boxplot-single-match-{}.eps'.format(NUM_PLAYERS),format='eps')
        plt.close()
    else:
        plt.show()

    # box plot of all points
    saved_points = pd.DataFrame(np.reshape(saved_points, (NUM_REPETITIONS, int(len(saved_points)/NUM_REPETITIONS))))
    meds = saved_points.median().sort_values(ascending=False)
    saved_points = saved_points[meds.index]
    saved_points.boxplot()
    plt.xticks(np.arange(NUM_PLAYERS)+1, [players[p].s for p in meds.index], rotation=90)
    plt.suptitle(("Mean and variance for each type at the end of the tournament - {} repetitions").format(NUM_REPETITIONS))
    plt.ylabel('Points')
    plt.xlabel('Player')
    if SAVE_IMG:
        plt.savefig('../img/ipdmp/ipdmp-boxplot-final-points-{}.eps'.format(NUM_PLAYERS),format='eps')
        plt.close()
    else:
        plt.show()
    
if __name__ == "__main__":
    main()