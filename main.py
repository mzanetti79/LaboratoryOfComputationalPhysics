import sys
sys.path.insert(0, '/strategies.py')
sys.path.insert(0, '/pdFunctions.py')
import numpy as np
import matplotlib.pyplot as plt
from strategies import Nice_guy, Bad_guy
from pdFunctions import IPD, MIPD, createPlayers, plot_cunsum

p1 = Nice_guy()
p2 = Bad_guy()

# print(IPD(p1,p2,2))
players = createPlayers(['main nice','main bad', 'nice guy'])
# print(IPD(players[0], players[1],10)[1])
# print(IPD(players[0], players[1],10)[0])

plot_cunsum(IPD(players[0], players[1],10),[players[0].getName(), players[1].getName()])
# print(IPD(players[0], players[2]))
# print(players[1].getMemory())
# print(MIPD(players,10))
