import sys
sys.path.insert(0, '/strategies.py')
import random
import numpy as np
import matplotlib.pyplot as plt
from strategies import Nice_guy, Bad_guy, Main_nice, Main_bad, Grudger, GoByMajority, Tit_for_tat, TitFor2Tats, SuspiciousTitForTat


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
    assert(name in stat), "Strategy does not exsit: %s" % name
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

# calculate alfa for each strategy according to its score
# the higher the score, the lower alfa it gets
# args:
#   strategies: object {strategy_name: average_score}
# returns:
#   {strategy_name: strategy_alfa}
def calcAlfa(strategies):
    stratsArr = [] # stratigies names
    avScores = []
    aflaDic = {}
    for s in strategies:
        stratsArr.append(s)
        avScores.append(strategies[s])
    maxScore = max(avScores)
    avScores = 1-(np.array(avScores)*0.9/maxScore)
    for i in range(0,len(stratsArr)):
        aflaDic[stratsArr[i]]= avScores[i]
    return aflaDic

# mode = 0 => len(output) = (#players,turns)
# mode = 1 => len(output) = (#players,#players)
def MIPD(players, turns=1, mode=1):
    if(mode == 1): scores = np.zeros([len(players),len(players)])
    else: scores = np.zeros([len(players),turns])
    for i in range(0,len(players)):
        for j in range(i+1,len(players)):
            _scores = IPD(players[i],players[j], turns)
            if(mode == 1):
                scores[i][j] = sum(_scores[0])
                scores[j][i] = sum(_scores[1])
            else:
                scores[i] = np.add(scores[i],_scores[0])
                scores[j] = np.add(scores[j],_scores[1])
    return scores 

# players: list of objects of type Player
# turns: int; number of turns of each match between two players
# iters: int; number of iterations
# alfa: float; the probabilty for a player to mutate
#   set alfa = 1 to remove its effect; all players will change their startigies in each iteration
#   set alfa = -1 to let alfa be calculated for each strategy according to it's scores
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
            strats[strat] = avg # average score for each strategy
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
        # Calculate alfa for each strategy if needed
        if(alfa == -1):
            alfas = calcAlfa(strats) 
        # Create new players with same population but different startegy distribution
        newPlayers = []
        for i in range(0, len(players)):
            if(alfa == -1): prob = 1 - alfas[players[i].getName()]
            else: prob = (1 - alfa)
            if(random.uniform(0, 1) >= prob):
                # flip a coin for each player to select his new strategy based on the 'spinner'
                _id = int(np.random.choice(spinner))
                newPlayers.append(strategyGenerator(idStrat[_id]))
            # or dont change strategy
            else: newPlayers.append(strategyGenerator(players[i].getName()))
        iterPlayers.append(newPlayers)
        players = newPlayers
    return iterPlayers, iterScores, totals