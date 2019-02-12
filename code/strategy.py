
import numpy as np

class Strategy:
    """Abstract Strategy class to derive other."""

    def __str__(self):
        return "Base"

    def get(self):
        pass

class NiceStrategy(Strategy):
    """Always cooperate."""

    def __str__(self):
        return "Nice"

    def get(self):
        return 0 # cooperate

class BadStrategy(Strategy):
    """Always defect."""

    def __str__(self):
        return "Bad"

    def get(self):
        return 1 # defect

class ProbStrategy(Strategy):
    """Abstract Strategy class when probability is used."""

    def __init__(self, k):
        self.k = k

    def get(self):
        num = np.random.randint(0,101)
        return 0 if num >= self.k else 1
        # coop if more than k, else defect

class MainlyNiceStrategy(ProbStrategy):
    """Cooperates most times."""

    def __str__(self):
        return "MainlyNice (k={})".format(self.k)

class MainlyBadStrategy(ProbStrategy):
    """Defect most times."""

    def __str__(self):
        return "MainlyBad (k={})".format(self.k)

class TitForTat(Strategy):
    """Plays opponent's last move."""

    def __str__(self):
        return "TitForTat"

    def get(self, last_move=None):
        if last_move is None:
            return 0 # cooperate the first time
        return last_move # repeat past opponent move
