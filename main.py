import sys
sys.path.insert(0, '/strategies.py')

from strategies import Nice_guy, Bad_guy, Main_nice, Main_bad, Grudger, GoByMajority, Tit_for_tat, TitFor2Tats, SuspiciousTitForTat

p1 = Nice_guy()
p2 = Bad_guy()
p3 = Main_nice(40)
p4 = Main_bad(70)
p5 = Grudger()
p6 = GoByMajority()

p1_score = []
p2_score = []
p3_score = []
p4_score = []
p5_score = []
p6_score = []

for i in range(1,10):
    p1_move = p1.play() # 1 or 0
    p2_move = p2.play()
    p3_move = p3.play()
    p4_move = p4.play()
    p5_move = p5.play()
    p6_move = p6.play()
    p1_score.append(p1.setScore(p1_move, p2_move)) # store in p1 memory and return p1 score of this play
    p2_score.append(p2.setScore(p2_move, p1_move))
    p3_score.append(p3.setScore(p3_move, p4_move))
    p4_score.append(p4.setScore(p4_move, p3_move))
    p5_score.append(p5.setScore(p5_move, p4_move))
    p6_score.append(p6.setScore(p6_move, p4_move))

print(p3_score)
print(p4_score)
print(p5_score)
print(p6_score)
