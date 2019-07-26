import sys
sys.path.insert(0, '/strategies.py')
sys.path.insert(0, '/pdFunctions.py')
import numpy as np
import matplotlib.pyplot as plt
from strategies import Nice_guy, Bad_guy
from pdFunctions import IPD, MIPD, rMIPD, createPlayers, plot_cunsum, barPlot, plot_box_multiple

p1 = Nice_guy()
p2 = Bad_guy()

# print(IPD(p1,p2,2))
players = createPlayers([['tit for tat', 2], ['bad guy', 1], ['main nice', 1], ['main bad', 1]])
# print(IPD(players[0], players[1]))
# print(IPD(players[0], players[2]))
# print(players[1].getMemory())
w= MIPD(createPlayers([['nice guy',1],['bad guy',2]], False),10,mode = 0)
# print(w)
players2 = createPlayers([['main nice', 5], ['main bad', 5], ['bad guy', 5], ['nice guy', 5]])
iterPlayers, iterScores, totals = rMIPD(players2,10,5)
# print(totals)
# plot_cunsum(IPD(players[0], players[1],10),[players[0].getName(), players[1].getName()])

# barPlot(players,scores)
# plot_cunsum(IPD(players[0], players[1],100),[players[0].getName(), players[1].getName()])
players3 = createPlayers([['nice guy', 5], ['bad guy', 5], ['main bad', 5]])
rMIPD(players3,100,10,-1)

NUM_REPETITIONS=100
scores = MIPD(players,NUM_REPETITIONS,mode=0)
# print(scores)
# plot_box(players[0], players[1],NUM_REPETITIONS)
plot_box_multiple(players,NUM_REPETITIONS)
plot_cunsum(scores,players)