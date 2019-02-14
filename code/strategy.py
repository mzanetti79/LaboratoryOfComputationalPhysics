import numpy as np

class Strategy:
    """Abstract Strategy class to derive other."""

    def __str__(self):
        return "Base"

    def get(self):
        pass


class Player(Strategy):
    """Class to describe a player with strategy and history"""
    def __str__(self):
           return "Player number {} with strategy: {}".format(self.n, self.s)
    
    #the idea is to create player of index n, eventually changing it's strategy
    #and have a list of players inside this class to manage all part of the homework
    def __init__(self, n, probS = True, k = 0):
        if probS:
            self.s = ProbStrategy(k)
        else:
            self.s = TipForTat()
        self.n = n
    
    def __get__(self): #Todo Not working
        return self.s.get()
    
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
