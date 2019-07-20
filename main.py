import sys
sys.path.insert(0, '/strategies.py')
sys.path.insert(0, '/pdFunctions.py')
import numpy as np
import matplotlib.pyplot as plt
from strategies import Nice_guy, Bad_guy
from pdFunctions import IPD, MIPD, rMIPD, createPlayers, plot_cunsum, barPlot, plot_box

p1 = Nice_guy()
p2 = Bad_guy()

# print(IPD(p1,p2,2))
players = createPlayers([['tit for tat', 5], ['bad guy', 10], ['main nice', 10],['tit for tat', 4]])
# print(IPD(players[0], players[1]))
# print(IPD(players[0], players[2]))
# print(players[1].getMemory())
w= MIPD(createPlayers([['nice guy',1],['bad guy',2]], False),10,mode = 0)
print(w)
players2 = createPlayers([['main nice', 5], ['main bad', 5], ['bad guy', 5], ['nice guy', 5]])
iterPlayers, iterScores, totals = rMIPD(players2,10,5)
print(totals)
# plot_cunsum(IPD(players[0], players[1],10),[players[0].getName(), players[1].getName()])
scores = MIPD(players,10)
# barPlot(players,scores)
# plot_cunsum(IPD(players[0], players[1],100),[players[0].getName(), players[1].getName()])
rMIPD(players,100,10)
# print(rMIPD(players,100,10))

NUM_REPETITIONS=100
plot_box(players[0], players[1],NUM_REPETITIONS)