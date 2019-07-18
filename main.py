import sys
sys.path.insert(0, '/strategies.py')
sys.path.insert(0, '/pdFunctions.py')
import numpy as np
import matplotlib.pyplot as plt
from strategies import Nice_guy, Bad_guy
from pdFunctions import IPD, MIPD, createPlayers, plot_cunsum,barPlot

p1 = Nice_guy()
p2 = Bad_guy()

# print(IPD(p1,p2,2))
players = createPlayers([['nice guy', 5], ['bad guy', 10], ['main nice', 10],['tit for tat', 4]])
print(IPD(players[0], players[1]))
print(IPD(players[0], players[2]))
print(players[1].getMemory())
scores = MIPD(players,10)
barPlot(players,scores)
plot_cunsum(IPD(players[0], players[1],10),[players[0].getName(), players[1].getName()])
