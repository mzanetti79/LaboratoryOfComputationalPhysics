import random
import numpy as np
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

# create an array of players
# playersNames: array of array; values of the array must be one of the startigies and the number of instances
# [['nice guy', 10], ['bad guy', 5]]
# suffle
# return array of objects of type Player
def createPlayers(playersNames, shuffle=True):
    players = []
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
    for name, num in playersNames:
        # check if stratigy name exists
        print(name, num)
        assert(name in stat)

        for i in range(0,num):
            players.append(stat[name]())
    
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
