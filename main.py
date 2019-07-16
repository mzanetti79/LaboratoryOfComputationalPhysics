import sys
sys.path.insert(0, '/strategies.py')

from strategies import Nice_guy, Bad_guy

p1 = Nice_guy()
p2 = Bad_guy()
p1_score = []
p2_score = []
for i in range(1,10):
    p1_move = p1.play() # 1 or 0
    p2_move = p2.play()
    p1_score.append(p1.setScore(p1_move, p2_move)) # store in p1 memory and return p1 score of this play
    p2_score.append(p2.setScore(p2_move, p1_move))
print(p1_score)