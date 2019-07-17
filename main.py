import sys
sys.path.insert(0, '/strategies.py')

from strategies import Nice_guy, Bad_guy, Tit_for_tat,SuspiciousTitForTat,TitFor2Tats

p1 = Nice_guy()
p2 = Bad_guy()
p3 = Tit_for_tat()
p4 = TitFor2Tats()
p1_score = []
p2_score = []
p3_score = []
p4_score = []

for i in range(1,10):
    p1_move = p1.play() # 1 or 0
    p2_move = p2.play()
    p3_move = p3.play()
    p1_score.append(p1.setScore(p1_move, p3_move)) # store in p1 memory and return p1 score of this play
    p3_score.append(p3.setScore(p3_move, p2_move))
print(p3_score)