from strategy import *
SAVE_IMG = False

def IPDRoundRobin(players, num_iter, against_itself=False, plot=False):
    """Round Robin tournament."""
    n = len(players)

    # each player plays against another in a round robin scheme
    if plot:
        plt.figure(figsize=(12,5))

    p = {obj:[0] * num_iter for obj in players}

    for (i, p1) in zip(np.arange(n), players):
        start = i if against_itself else i+1
        for (j, p2) in zip(np.arange(start, n), players[start:]):
            p1.clear_history()
            p2.clear_history()
            p1.play_iter(p2, num_iter)
            if plot:
                p[p1] += np.cumsum(p1.payoffHist)
                p[p2] += np.cumsum(p2.payoffHist)

    if plot:
        for i in p:
            plt.plot(p[i], label=i.s)
            plt.xlabel('Iteration')
            plt.ylabel('Cum. reward')
        plt.title("Evolution of the game")
        plt.legend(bbox_to_anchor=(1,1))
        if SAVE_IMG: # TODO we save images in ipdmp dir but this method is called also by other scripts
            plt.savefig('../img/ipdmp/ipdmp-evolution-of-game-{}.eps'.format(len(p)),format='eps',bbox_inches='tight')
            plt.close()

    # calculate ranking and matches dataframes
    # has to be done after the tournament
    ranking_df = pd.DataFrame() # all points gained by players
    matches_df = pd.DataFrame() # all matches played sorted by time

    for (i, p) in zip(np.arange(n), players):
        points = p.get_points()
        cooperate_count, defect_count = p.get_coop_def_count()

        df = pd.DataFrame(
            [[p.s, int(points[-1]), cooperate_count, defect_count, p, p.s.id]],
            columns=['Player','points', 'cooperate_count', 'defect_count', 'rrp', 'labels']
        )
        ranking_df = ranking_df.append(df)
        # ranking_df = ranking_df.sort_values(['points'], ascending=False)

        for j in range(i, len(p.results)):
            # can now access any property from p1 or p2 for plots
            # each match can be explored
            df = pd.DataFrame(
                [[p.s, p.prevOpponent[j].s, p.results[j], p.prevOpponent[j].results[i]]],
                columns=['p1','p2','p1-score','p2-score']
            )
            matches_df = matches_df.append(df)

    players = np.array(ranking_df.sort_values(['points'], ascending=False)['rrp'])
    ranking_df = ranking_df.drop(columns=['rrp']).reset_index(drop=True)
    return players, ranking_df, matches_df

def main():
    np.random.seed(100)
    pd.set_option('display.max_columns', None)

    NUM_ITER = 50
    NUM_PLAYERS = 50
    NUM_REPETITIONS = 10
    print("Testing round-robin tournament with {}-people".format(NUM_PLAYERS))

    # define k for strategy probabilities
    k_strategies = Strategy.generatePlayers(NUM_PLAYERS, replace=(NUM_PLAYERS > Strategy.TOT_STRAT))

    repeated_players = []
    for i in range(NUM_REPETITIONS):
        # initialize players with given strategies
        players = np.array([MultiPlayer(k) for k in k_strategies])

        players, ranking_df, matches_df = IPDRoundRobin(players, NUM_ITER, plot=(i==(NUM_REPETITIONS-1))) # not against itself, plot last rep.

        repeated_players.append(players)
        repeated_ranking_df = repeated_ranking_df.append(ranking_df) if i!=0 else ranking_df
        # print(ranking_df.to_latex(index=False))
        # print(matches_df.to_latex(index=False))

    # print tables
    pd.set_option('precision', 2)

    group = repeated_ranking_df[['points', 'cooperate_count', 'defect_count']].groupby(repeated_ranking_df.index)
    group_mean = group.mean()
    group_mean.columns = [str(col) + '_mean' for col in group_mean.columns]
    group_std = group.std()
    group_std.columns = [str(col) + '_std' for col in group_std.columns]
    group_df = group_mean.merge(group_std, left_index=True, right_index=True, how='left')
    group_df['cooperation_perc'] = group_df['cooperate_count_mean']*100/(group_df['cooperate_count_mean']+group_df['defect_count_mean'])
    group_df['str'] = repeated_ranking_df['Player'][:NUM_PLAYERS]
    print(group_df.to_latex(index=False))

    # box plot of last match
    one_round_results = [p.results for p in players]
    one_round = pd.DataFrame(one_round_results).T
    meds = one_round.median().sort_values(ascending=False)
    one_round = one_round[meds.index]
    plt.figure(figsize=(12,5))
    one_round.boxplot()
    plt.xticks(np.arange(NUM_PLAYERS)+1, [players[p].s for p in meds.index], rotation=90)
    plt.suptitle('Mean and variance for each type vs the other players \n One complete round')
    plt.ylabel('Points')
    plt.xlabel('Player')
    if SAVE_IMG:
        plt.savefig('../img/ipdmp/ipdmp-boxplot-single-match-{}.eps'.format(NUM_PLAYERS),format='eps',bbox_inches='tight')
        plt.close()
    else:
        plt.show()

    # box plot of all points
    group_median = group.median().sort_values(by=['points'], ascending=False)
    temp_df = pd.DataFrame()
    for index in group_median.index:
        temp_df = temp_df.append(group.get_group(index))
    temp_df['index'] = np.repeat(np.arange(50), NUM_REPETITIONS)
    plt.figure(figsize=(12,5))
    temp_df.boxplot(column='points', by='index')
    plt.xticks(np.arange(NUM_PLAYERS)+1, group_df['str'][group_median.index], rotation=90)
    plt.suptitle(("Mean and variance for each type at the end of the tournament - {} repetitions").format(NUM_REPETITIONS))
    plt.ylabel('Points')
    plt.xlabel('Player')
    if SAVE_IMG:
        plt.savefig('../img/ipdmp/ipdmp-boxplot-final-points-{}.eps'.format(NUM_PLAYERS),format='eps',bbox_inches='tight')
        plt.close()
    else:
        plt.show()

if __name__ == "__main__":
    main()