import random

class Player(object):
    """A class for a player in the tournament.
    This is an abstract base class, not intended to be used directly.
    """ 
    
    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        self.score = 0
        self.memory = []

    def getMemory(self):
        return self.memory
    
    def setScore(self, self_move, opp_move):
        self.memory.append(opp_move)
        T=3
        R=2
        P=1 
        S=0
        newScore = 0
        if (self_move == 1 and opp_move == 1): newScore = R
        elif (self_move == 1 and opp_move == 0): newScore = T
        elif (self_move == 0 and opp_move == 1): newScore = S
        else: newScore = P
        self.score += newScore
        return newScore
    
    def play(self):
        # To be overrided in the next classes
        return None

# for i in range(1,10):
#     p1_move = obj1.play() # 1 or 0
#     p2_move = obj2.play()
#     p1_score[i] = obj1.setScore(p1_move, p2_move) # store in p1 memory and return p1 score of this play
#     p2_score[i] = obj2.setScore(p2_move, p1_move)

class Nice_guy(Player):
    def play(self):
        return 1


class Bad_guy(Player):
    def play(self):
        return 0

class Main_bad(Player):
    """randomly defect k\% of the times and cooperate 100-k%, k>50"""
    def __init__(self,K):
        Player.__init__(self)
        self.K = K/10

    def play(self):
        number = random.randint(1,10)
        if number >= self.K:
            return 1
        else:
            return 0

class Main_nice(Player):
    """randomly defect k\% of the times and cooperate 100-k%, k<50"""
    def __init__(self,K):
        Player.__init__(self)
        self.K = K/10

    def play(self):
        number = random.randint(1,10)
        if number >= self.K:
            return 1
        else:
            return 0

class Grudger(Player):
    """A player starts by cooperating however will defect if
    at any point the opponent has defected."""

    def play(self):
        if len(self.memory)==0:
            return 1
        else:
            if 0 in self.memory:
                return 0
            else:
                return 1

class GoByMajority(Player):
    """A player examines the history of the opponent:
    if the opponent has more defections than cooperations then the player defects."""
    def play(self):
        if sum([s == 0 for s in self.memory]) > sum([s == 1 for s in self.memory]):
            return 0
        return 1
