import numpy as np
from strategies import Nice_guy, Bad_guy

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
# playersNames: array of strings; values of the array must be one of the startigies
# nice guy, bad guy, tit-for-tat
# return array of objects of type Player
def createPlayers(playersNames):
    players = []
    stat = {
        'nice guy': (lambda: Nice_guy()),
        'bad guy': (lambda: Bad_guy())
    }
    for name in playersNames:
        # check if stratigy name exists    
        assert(name in stat)

        players.append(stat[name]())
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
