import sys
sys.path.insert(0, '/strategies.py')
sys.path.insert(0, '/pdFunctions.py')
import numpy as np
import matplotlib.pyplot as plt
from strategies import Nice_guy, Bad_guy
from pdFunctions import IPD, MIPD, rMIPD, createPlayers, plot_cunsum, barPlot, plot_box_multiple, plot_box,plot_two_functions

p1 = Nice_guy()
p2 = Bad_guy()

# print(IPD(p1,p2,2))
# players = createPlayers([['tit for tat', 2], ['bad guy', 1], ['nice guy', 1], ['main nice', 1], ['main bad', 1]])
players = createPlayers( [['tit for tat', 1], ['main bad', 1],['main nice', 1],['bad guy', 1]], shuffle=False)
# print('qqq',IPD(players[3], players[1],10))
# print(IPD(players[0], players[2]))
# print(players[1].getMemory())
w= MIPD(createPlayers([['nice guy',1],['bad guy',2]], False),10,mode = 1)
# print('eeeee',w)
players2 = createPlayers([['main nice', 5], ['main bad', 5], ['bad guy', 5], ['nice guy', 5]])
iterPlayers, iterScores, totals = rMIPD(players2,10,5)
# print(totals)
# fig, (ax1,ax2) = plt.subplots(1,2,figsize=(10, 4))
plys=[players[0], players[1]]
NUM_REPETITIONS=10
results=IPD(players[0], players[1],10)
# plot_cunsum(results,plys,ax1)
# plot_box_multiple(results,plys,NUM_REPETITIONS,ax2)
# plt.tight_layout() 
# plt.show()

# barPlot(players,scores)
# plot_cunsum(IPD(players[0], players[1],100),[players[0].getName(), players[1].getName()])
# rMIPD(players,100,10)
# # print('hhhh',rMIPD(players,100,10))
# players3 = createPlayers([['nice guy', 5], ['bad guy', 5], ['main bad', 5]])
# rMIPD(players3,100,10,-1)

# 
# results = MIPD(players,NUM_REPETITIONS,mode=0)
# # print(scores)
# # results=IPD(players[0], players[1], NUM_REPETITIONS)
# print('resres',results)
# # plot_box(results,players[0], players[1], NUM_REPETITIONS)
# # plot_box_multiple(results,players,NUM_REPETITIONS)
# # plot_cunsum(results,players)
# barPlot(players,results)

plot_two_functions(results,plys, NUM_REPETITIONS)