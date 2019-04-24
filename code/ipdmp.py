import os
from strategy import *
from base_options import *
from player import MultiPlayer

def IPDRoundRobin(players, num_iter, against_itself=False, return_ranking=False, save_plot=False, save_img=False, DEBUG=False, root=''):
    """Round Robin tournament."""
    n = len(players)

    p = {obj:[0] * num_iter for obj in players}
    yields = {obj:[] for obj in players}
    achieves = {obj:[] for obj in players}

    for (i, p1) in zip(np.arange(n), players):
        if DEBUG:
            print("Match progress = {}/{}".format((i+1), players.size))

        start = i if against_itself else i+1
        for (j, p2) in zip(np.arange(start, n), players[start:]):
            p1.clear_history()
            p2.clear_history()
            p1.play_iter(p2, num_iter)

            rew1, yield1, best1 = p1.metrics()
            rew2, yield2, best2 = p2.metrics()

            yields[p1].append(rew1[-1]/yield1[-1])
            yields[p2].append(rew2[-1]/yield2[-1])
            achieves[p1].append(rew1[-1]/best1[-1])
            achieves[p2].append(rew2[-1]/best2[-1])

            if save_plot:
                p[p1] += rew1
                p[p2] += rew2

    if save_plot:
        plt.figure(figsize=(12,5))
        for i in p:
            plt.plot(p[i], label=i.s)
        plt.xlabel('Iteration')
        plt.ylabel('Cum. reward')
        plt.title("Evolution of the game")
        plt.legend(bbox_to_anchor=(0,-0.1), ncol=5, loc=2)
        if save_img: # we only save images for ipdmp script
            plt.savefig('{}/img/ipdmp/ipdmp-evolution-of-game-{}.eps'.format(root,len(p)),format='eps',bbox_inches='tight')
            plt.close()
        else:
            plt.show()

    # calculate ranking and matches dataframes
    # has to be done after the tournament
    ranking_df = pd.DataFrame() # all points gained by players

    for (i, p) in zip(np.arange(n), players):
        if DEBUG:
            print("Point progress = {}/{}".format((i+1), players.size))

        points = p.get_points()
        cooperate_count, defect_count = p.get_coop_def_count()

        df = pd.DataFrame(
            [[str(p.s), int(points[-1]), cooperate_count, defect_count, p, p.s.id, 100*np.mean(yields[p]), 100*np.mean(achieves[p])]],
            columns=['Player', 'points', 'coop_count', 'defect_count', 'rrp', 'labels', 'yield', 'achieve']
        )
        ranking_df = ranking_df.append(df)
        # ranking_df = ranking_df.sort_values(['points'], ascending=False)

    players = np.array(ranking_df.sort_values(['points'], ascending=False)['rrp'])
    ranking_df = ranking_df.drop(columns=['rrp']).reset_index(drop=True)

    # rank calculation is expensive when players are a lot, but necessary to have rank
    if not return_ranking:
        return players

    return players, ranking_df

def main():
    pd.set_option('display.max_columns', None)

    root = os.path.dirname(os.path.abspath(__file__))[:-5]

    opt = BaseOptions().parse(BaseOptions.IPDMP)
    NUM_ITER = opt.niter
    NUM_PLAYERS = opt.nplay
    NUM_REPETITIONS = opt.nrep
    FIXED = opt.fixed
    SAVE_IMG = opt.saveimg
    LATEX = opt.latex
    np.random.seed(opt.seed) # None = clock, no-number = 100

    print("Testing round-robin tournament with {}-people".format(NUM_PLAYERS))

    # define k for strategy probabilities
    k_strategies = Strategy.generatePlayers(NUM_PLAYERS, replace=(NUM_PLAYERS > Strategy.TOT_STRAT), fixed=FIXED)
    #k_strategies = np.array([GRT,GRT, TFT,TFT, TF2T,TF2T, BAD,BAD, NICE,NICE]) # paper test
    #k_strategies = np.array([TFT,TFT, TFT, TFT, BAD, BAD, BAD, BAD, NICE,NICE]) # paper test 2

    repeated_players = []
    for i in range(NUM_REPETITIONS):
        # initialize players with given strategies
        players = np.array([MultiPlayer(k) for k in k_strategies])

        players, ranking_df = IPDRoundRobin(players, NUM_ITER, return_ranking=True,
            save_plot=(i==(NUM_REPETITIONS-1)), save_img=SAVE_IMG, root=root) # not against itself, plot last rep.

        repeated_players.append(players)
        repeated_ranking_df = repeated_ranking_df.append(ranking_df) if i!=0 else ranking_df

    # print tables
    pd.set_option('precision', 2)

    group = repeated_ranking_df[['points', 'coop_count', 'defect_count']].groupby(repeated_ranking_df.index)
    group_mean = group.mean()
    group_mean.columns = [str(col) + '_mean' for col in group_mean.columns]
    group_std = group.std()
    group_std.columns = [str(col) + '_std' for col in group_std.columns]
    group_df = group_mean.merge(group_std, left_index=True, right_index=True, how='left')
    group_df['coop_perc'] = group_df['coop_count_mean']*100/(group_df['coop_count_mean']+group_df['defect_count_mean'])
    group_df['str'] = repeated_ranking_df['Player'][:NUM_PLAYERS]
    group_df['yield'] = repeated_ranking_df['yield'][:NUM_PLAYERS]
    group_df['achieve'] = repeated_ranking_df['achieve'][:NUM_PLAYERS]
    group_df = group_df[['str','points_mean','points_std','yield','achieve',
        'coop_count_mean','coop_count_std','defect_count_mean','defect_count_std','coop_perc']] # column reordering
    group_df = group_df.sort_values(by=['points_mean'], ascending=False)
    if LATEX:
        print(group_df.to_latex(index=False))
    else:
        print(group_df)

    # box plot of last match
    one_round_results = [p.results for p in players]
    one_round = pd.DataFrame(one_round_results).T
    meds = one_round.median().sort_values(ascending=False)
    one_round = one_round[meds.index]
    one_round.boxplot(figsize=(12,5))
    plt.xticks(np.arange(NUM_PLAYERS)+1, [players[p].s for p in meds.index], rotation=90)
    plt.suptitle('Mean and variance for each type vs the other players \n One complete round')
    plt.ylabel('Points')
    plt.xlabel('Player')
    if SAVE_IMG:
        plt.savefig('{}/img/ipdmp/ipdmp-boxplot-single-match-{}.eps'.format(root, NUM_PLAYERS),format='eps',bbox_inches='tight')
        plt.close()
    else:
        plt.show()

    # box plot of all points
    group_median = group.median().sort_values(by=['points'], ascending=False)
    temp_df = pd.DataFrame()
    for index in group_median.index:
        temp_df = temp_df.append(group.get_group(index))
    temp_df['index'] = np.repeat(np.arange(NUM_PLAYERS), NUM_REPETITIONS)
    temp_df.boxplot(column='points', by='index', figsize=(12,5))
    plt.xticks(np.arange(NUM_PLAYERS)+1, group_df['str'][group_median.index], rotation=90)
    plt.suptitle(("Mean and variance for each type at the end of the tournament - {} repetitions").format(NUM_REPETITIONS))
    plt.ylabel('Points')
    plt.xlabel('Player')
    if SAVE_IMG:
        plt.savefig('{}/img/ipdmp/ipdmp-boxplot-final-points-{}.eps'.format(root,NUM_PLAYERS),format='eps',bbox_inches='tight')
        plt.close()
    else:
        plt.show()

if __name__ == "__main__":
    main()
