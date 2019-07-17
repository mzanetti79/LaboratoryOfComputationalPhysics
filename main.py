import sys
sys.path.insert(0, '/strategies.py')
sys.path.insert(0, '/pdFunctions.py')

from strategies import Nice_guy, Bad_guy
from pdFunctions import IPD, MIPD, createPlayers

p1 = Nice_guy()
p2 = Bad_guy()

print(IPD(p1,p2,2))
players = createPlayers(['nice guy', 'bad guy', 'nice guy'])
print(IPD(players[0], players[1]))
print(IPD(players[0], players[2]))
print(players[1].getMemory())
print(MIPD(players,10))