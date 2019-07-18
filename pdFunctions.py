import random
import numpy as np
import matplotlib.pyplot as plt
from strategies import Nice_guy, Bad_guy, Main_nice, Main_bad, Grudger, GoByMajority, Tit_for_tat, TitFor2Tats, SuspiciousTitForTat
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt; plt.rcdefaults()
import statistics

## Iterative Prisoner's Dilemma
# p1,p2 of type Player
# turns: int; number of turns
# return scores: 2D array of scores for both players
def IPD(p1, p2, turns=1):
    scores = [[],[]]
    for i in range(0,turns):
        p1_move = p1.play() # 1 or 0
        p2_move = p2.play()
        scores[0].append(p1.setScore(p1_move, p2_move)) # store in p1 memory and return p1 score of this play
        scores[1].append(p2.setScore(p2_move, p1_move))
    return scores

# generates player by startegy name
# name: string; name of startegy
def strategyGenerator(name):
    stat = {
        'nice guy': (lambda: Nice_guy()),
        'bad guy': (lambda: Bad_guy()),
        'main nice': (lambda: Main_nice(random.randint(1, 49))),
        'main bad': (lambda: Main_bad(random.randint(51, 99) )),
        'grudger': (lambda: Grudger()),
        'go by majority': (lambda: GoByMajority()),
        'tit for tat': (lambda: Tit_for_tat()),
        'tit for 2 tats': (lambda: TitFor2Tats()),
        'suspicious tit for tat': (lambda: SuspiciousTitForTat())
    }
    # check if stratigy name exists
    assert(name in stat)
    return stat[name]()
    
# create an array of players
# playersNames: array of array; values of the array must be one of the startigies and the number of instances
# [['nice guy', 10], ['bad guy', 5]]
# suffle
# return array of objects of type Player
def createPlayers(playersNames, shuffle=True):
    players = []
    for name, num in playersNames:
     
        for i in range(0,num):
            players.append(strategyGenerator(name))
    
    # shuffle
    if(shuffle): random.shuffle(players)
    return players

def MIPD(players, turns=1):
    scores = np.zeros([len(players),len(players)])
    for i in range(0,len(players)):
        for j in range(i+1,len(players)):
            if i == j: # if player play vs himself
                scores[i][j] = 0
                break
            _scores = IPD(players[i],players[j], turns)
            scores[i][j] = sum(_scores[0])
            scores[j][i] = sum(_scores[1])
    return scores

# players: list of objects of type Player
# turns: int; number of turns of each match between two players
# iters: int; number of iterations
# alfa: float; the probabilty for a player to mutate
#   set alfa = 0 to remove its effect
# returns iterPlayers, iterScores, totals
#   iterPlayers: 2D array of Player objects; number of rows is the number of iterations
#       number of columns is the number of players
#   iterScores: 2D array of float;
#       each row is a set of total scores of each player one iteration
#   totals: array of float; number of elements = number of iterations
#       each element is the total score of all players in one iteration
def rMIPD(players, turns=1,iters=1, alfa=0.5):
    iterPlayers = [] # each row is a set of players in one iteration
    iterScores = [] # each row is a set of total scores of each player one iteration
    totals = [] # total scores for all players in each iteration
    # create id for each strategy
    idStrat = {} # { id : name }
    stratId = {} # { name : id }
    for p in players:
        stratId[p.getName()] = 0
    for i, strat in enumerate(stratId.keys()):
        stratId[strat] = i
        idStrat[i] = strat
    # start iterations
    for itr in range(0,iters):
        scores = MIPD(players, turns)
        scores = np.sum(scores,axis=1) # final score for each player
        iterScores.append(scores)
        strats = {} # total score for each strategy
        for i, player in enumerate(players):
            name = player.getName()
            if (name not in strats.keys()): strats[name] = [scores[i]]
            else: strats[name].append(scores[i])
        
         # average score for each strategy
        _totalAvg = 0
        _total = 0
        for strat in strats:
            _total = np.sum(strats[strat])
            avg = np.average(strats[strat])
            strats[strat] = avg
            _totalAvg += avg
        totals.append(_total)
        # normalize scores of strategies then multiply by 100 and round it
        spinner = []
        for strat in strats:
            strats[strat] = strats[strat] / _totalAvg # normalize scores
            strats[strat] = int(round(strats[strat] * 100)) # eg. strats = { strat1: 40, strat2: 60}
            # create spinner weel to be used in random selection
            spinner = np.append(spinner, [stratId[strat] for i in range(0,strats[strat])])
            # eg. spinner = [start1_id, start1_id,... 40 times, start2_id,.. x60 times]
        
        # Create new players with same population but different startegy distribution
        newPlayers = []
        for i in range(0, len(players)):
            if(random.uniform(0, 1) >= alfa):
                # flip a coin for each player to select his new strategy based on the 'spinner'
                _id = int(np.random.choice(spinner))
                newPlayers.append(strategyGenerator(idStrat[_id]))
            # or dont change strategy
            else: newPlayers.append(strategyGenerator(players[i].getName()))
        iterPlayers.append(newPlayers)
    return iterPlayers, iterScores, totals

        
def barPlot(players, scores):
    bins = []
    playersNames = []
    counts = []
    avg_scores = []
    for i in range(len(players)):
        avg_scores.append(statistics.mean(scores[i]))
        playersNames.append(players[i].getName())
    bins = list(dict.fromkeys(playersNames))

    for x in range(len(bins)):
        counts.append(playersNames.count(bins[x]))
    
    startigies_avg = [0] * len(bins)
    for i in range(len(playersNames)):
        for x in range(len(bins)):
            if(bins[x] == playersNames[i]):
                startigies_avg[x]+=avg_scores[i]
    
    for x in range(len(startigies_avg)):
        startigies_avg[x] = startigies_avg[x]/counts[x]
    
    plt.figure(1)      
    y_pos = np.arange(len(bins))
    plt.bar(y_pos, counts, align='center', alpha=0.5)
    plt.xticks(y_pos, bins)
    plt.xlabel('Name')
    plt.ylabel('Number')
    plt.title('Players with strategies names')
    plt.show()

    plt.figure(2)
    y_pos = np.arange(len(startigies_avg))
    plt.bar(y_pos, startigies_avg, align='center', alpha=0.5)
    plt.xticks(y_pos, bins)
    plt.xlabel('Name')
    plt.ylabel('Average score')
    plt.title('Players with average scores')
    plt.show()


def plot_cunsum(players_score_matrix, players):
    players_len= len(players_score_matrix)
    turns=len(players_score_matrix[0])
    x = range(1,turns+1)
    fig, ax = plt.subplots(figsize=(8, 4))
    for i in range(players_len):
        r = lambda: random.randint(20,200)
        g = lambda: random.randint(20,200)
        b = lambda: random.randint(20,200)
        color = '#{:02x}{:02x}{:02x}'.format(r(), g(), b())
        y = np.asarray(players_score_matrix[i])
        y = y.cumsum()
        label= players[i] + str(i)
        ax.plot(x, y, 'k--', linewidth=1.5, label=label, color=color)
    # tidy up the figure
    ax.grid(True)
    ax.legend(loc='right')
    ax.set_title('Cumulative Player Score over turns')
    ax.set_xlabel('Turns')
    ax.set_ylabel('Comulative Score')
    plt.show()


