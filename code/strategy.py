import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
#from mgen import generatePayoffMatrix

# pandas options for dataframe visualization
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('precision', 2)

# global variables for ground truth about strategies
COOPERATE = 0
DEFECT = 1

NICE = 0
IND  = 50
BAD  = 100

TFT  = -1
TF2T = -2
GRT  = -3
PRBL = -10 # just placeholders
PRBH = -11

class Strategy:
    """Abstract Strategy class to derive other."""
    TOT_STRAT = 8

    def __str__(self):
        return "Base"

    def get(self):
        pass

    @staticmethod
    def generatePlayers(num_players, replace=False, fixed=False):
        """Generates a set of players with random strategies."""
        str_choices = [NICE, BAD, IND, TFT, TF2T, GRT, PRBL, PRBH]
        k = np.random.choice(str_choices, num_players, replace=replace)

        # substitute with useful values if needed
        maskL = k==PRBL # 1 to 49 exclude nice, indifferent
        k[maskL] = np.repeat(25, maskL.sum()) if fixed else np.random.choice(49, size=maskL.sum(), replace=replace) + 1
        maskH = k==PRBH # 51 to 99 exclude bad, indifferent
        k[maskH] = np.repeat(75, maskH.sum()) if fixed else np.random.choice(49, size=maskH.sum(), replace=replace) + 51

        return k

class ProbStrategy(Strategy):
    """Strategy class when probability is used.
    Spans from always nice to always bad players"""

    def __init__(self, k):
        # default value is to cooperate in case of wrong k
        self.k = k if k>=NICE and k<=BAD else NICE
        self.id = k

    def get(self):
        num = np.random.randint(0,100)
        return COOPERATE if num >= self.k else DEFECT

    def __str__(self):
        if (self.k == NICE):
            return "Nice"
        elif (self.k == BAD):
            return "Bad"
        elif (self.k > IND):
            return "MainlyBad (k={})".format(self.k)
        elif (self.k < IND):
            return "MainlyNice (k={})".format(self.k)
        else:
            return "Indifferent"

class TitForTat(Strategy):
    """Plays opponent's last move."""

    def __init__(self):
        self.id = TFT

    def __str__(self):
        return "TitForTat"

    def get(self, last_move=None):
        if last_move == None:
            return COOPERATE # first time
        return last_move # repeat past opponent move

class TitFor2Tat(TitForTat):
    """Defects only if the opponent has defected last two times."""

    def __init__(self):
        self.id = TF2T

    def __str__(self):
        return "TitFor2Tat"

    def get(self, last_moves=None):
        if last_moves == None:
            return COOPERATE
        return (last_moves[0] and last_moves[1])
        # COOPERATE = 0, DEFECT = 1. If both 1 only case to have DEFECT as output

class GrimTrigger(Strategy):
    """Cooperate at first, if opponent defects once then always defect."""

    def __init__(self):
        self.id = GRT
        self.triggered = False

    def __str__(self):
        return "GrimTrigger"

    def get(self, last_move=None):
        if not self.triggered and last_move == DEFECT:
            self.triggered = True

        if self.triggered:
            return DEFECT
        return COOPERATE
