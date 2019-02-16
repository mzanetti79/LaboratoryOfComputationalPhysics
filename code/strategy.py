import numpy as np

class Strategy:
    """Abstract Strategy class to derive other."""

    def __str__(self):
        return "Base"

    def get(self):
        pass


class Player(Strategy):
    M1 = np.array([[2,0],[3,1]])
    # M1 = np.array([[3,0],[5,2]]) # another good choice
    # or use M = generatePayoffMatrix()
    M2 = M1.T
    
    """Class to describe a player with strategy and history"""
    def __str__(self):
           return "Player with strategy: {}".format(self.s)
    
    #the idea is to create player of index n, eventually changing it's strategy
    #and have a list of players inside this class to manage all part of the homework
    def __init__(self, probS = True, k = 0):
        if probS:
            self.s = ProbStrategy(k)
        else:
            self.s = TitForTat()
        self.stratHist = []
        self.payoffHist = []
        self.playedHist = []
    
    def play_iter(self, sOpponent, num_iter):
        for _ in range(num_iter):
            self.play(sOpponent)

    def play(self, sOpponent): 
        if type(self.s) != TitForTat:
            action1 = self.s.get()
        else:
            action1 = 0 # cooperate
            if len(sOpponent.playedHist) > 0:
                action1 = self.s.get(sOpponent.playedHist[-1]) # pass opponent's move
            
        if type(sOpponent) != TitForTat:
            action2 = sOpponent.s.get()
        else:
            action2 = 0
            if len(self.playedHist) > 0:
                action2 = s2.get(self.playedHist[-1])
        self.update(action1, action2, False)
        sOpponent.update(action1, action2, True)
        
    def update(self, action1, action2, opponent):
        self.stratHist.append(str(self.s)) #todo check if better this or k
        if opponent:
            self.payoffHist.append(self.M2[action1,action2])
            self.playedHist.append(action2)
        else:
            self.payoffHist.append(self.M1[action1,action2])
            self.playedHist.append(action1)

    def clearHist(self):
        self.stratHist = []
        self.payoffHist = []
        self.playedHist = []

class MultiPlayer(Player):
    def __init__(self, probS, k):
        Player.__init__(self, probS, k)
        
        # save results for multiple rounds played by user
        self.prevStratHist = []
        self.prevPayoffHist = []
        self.prevPlayedHist = []

    def play_iter(self, sOpponent, num_iter):
        Player.play_iter(self, sOpponent, num_iter)

        self.prevStratHist.append(self.stratHist)
        self.prevPayoffHist.append(self.payoffHist)
        self.prevPlayedHist.append(self.playedHist)

        sOpponent.prevStratHist.append(sOpponent.stratHist)
        sOpponent.prevPayoffHist.append(sOpponent.payoffHist)
        sOpponent.prevPlayedHist.append(sOpponent.playedHist)

        # set actual history to zero
        self.clearHist()
        sOpponent.clearHist()

    def actual_round(self):
        return len(self.prevStratHist)

class ProbStrategy(Strategy):
    """Strategy class when probability is used."""

    def __init__(self, k): #todo put limit check on k
        self.k = k

    def get(self):
        num = np.random.randint(0,100)
        return 0 if num >= self.k else 1
        # coop if more than k, else defect

    def __str__(self):
        if (self.k == 0):
            return "Nice"
        elif (self.k == 100):
            return "Bad"
        elif (self.k > 50):
            return "MainlyBad (k={})".format(self.k)
        elif (self.k < 50):
            return "MainlyNice (k={})".format(self.k)
        else:
            return "Indifferent"
        
class TitForTat(Strategy):
    """Plays opponent's last move."""

    def __str__(self):
        return "TitForTat"

    def get(self, last_move=None):
        if last_move is None:
            return 0 # cooperate the first time
        return last_move # repeat past opponent move
