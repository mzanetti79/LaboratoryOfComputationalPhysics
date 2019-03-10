import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
#from mgen import generatePayoffMatrix

# Define global variables to have groundtruth about strategies
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

TOT_STRAT = 8 #TODO should be 10??

class Player(object):
    """Class to describe a player with strategy and history."""
    
    def __str__(self):
        """Override standard printer""" 
        return "Player with strategy: {}".format(self.s)
    
    # optional: use M = generatePayoffMatrix()
    def __init__(self, k=0, M=np.array([[3,0],[5,1]])):
        self.M1 = M
        self.M2 = M.T

        self.s = self.get_strategy(k)
        self.clear_history()
    
    def play_iter(self, opponent, num_iter):
        """Plays the game against an opponent num_iter times."""
        for _ in range(num_iter):
            self.play(opponent)

    def play(self, opponent): 
        """Plays the game against an opponent."""
        action1 = self.act(opponent)
        action2 = opponent.act(self)
                
        self.update(action1, action2, False)
        if opponent.s != self.s:
            opponent.update(action1, action2, True)

    def act(self, opponent):
        """Gets the action based on the strategy."""
        if type(self.s) == ProbStrategy:
            return self.s.get()
        elif type(self.s) == TitForTat or type(self.s) == GrimTrigger:
            if len(opponent.playedHist) > 0: #at least 1
                return self.s.get(opponent.playedHist[-1]) # pass opponent's move
            return COOPERATE
        elif type(self.s) == TitFor2Tat:
            if len(opponent.playedHist) > 1: #at least 2
                return self.s.get([opponent.playedHist[-2],opponent.playedHist[-1]]) # pass opponent's second to lastmove
            return COOPERATE
        
    def update(self, action1, action2, opponent):
        """Updates the state based on the actions and if is opponent."""
        self.stratHist.append(str(self.s)) #todo check if better this or k
        if opponent:
            self.payoffHist.append(self.M2[action1,action2])
            self.playedHist.append(action2)
            self.bestPossibleHist.append(max(self.M2[:,action2]))
        else:
            self.payoffHist.append(self.M1[action1,action2])
            self.playedHist.append(action1)
            self.bestPossibleHist.append(max(self.M1[action1,:]))
        
    def get_strategy(self, k):
        """Get strategy object given the id."""
        if k >= NICE and k <= BAD:
            return ProbStrategy(k)
        elif k == TFT:
            return TitForTat()
        elif k == TF2T:
            return TitFor2Tat()
        elif k == GRT:
            return GrimTrigger()

    def clear_history(self):
        """Clears all history of the player."""
        self.stratHist = []
        self.payoffHist = []
        self.playedHist = []
        self.bestPossibleHist = []

class MultiPlayer(Player):
    """Class to describe multiple players with strategy and history."""

    def __init__(self, k, changing=False):
        Player.__init__(self, k)
        
        # save results for multiple rounds played by user
        # this way we can save all the results from the tournament
        self.prevStratHist = []
        self.prevPayoffHist = []
        self.prevPlayedHist = []
        self.prevBestPossibleHist = []
        self.prevOpponent = []
        self.results = []
        self.changing = changing
    
    def winner(self,opponent):
        """Save the total payoff of the player"""
        self.results.append(np.sum(self.payoffHist))
        if opponent.s != self.s:
            opponent.results.append(np.sum(opponent.payoffHist))

    def change_strategy(self):
        """Change the strategy randomly."""
        # watch out: each player has a different kH, kL
        k_strategies = Strategy.generatePlayers(TOT_STRAT, replace=False)
        
        s_next = self.random_strategy(k_strategies)
        while s_next == self.s:
            s_next = self.random_strategy(k_strategies)

        self.s = s_next

    def random_strategy(self, k_list):
        """Generate random strategy object."""
        return self.get_strategy(np.random.choice(k_list))
        
    def play_iter(self, opponent, num_iter):
        # change strategy at the start of each match
        # if self.changing:
        #     self.change_strategy()
        Player.play_iter(self, opponent, num_iter)

        self.prevStratHist.append(self.stratHist)
        self.prevPayoffHist.append(self.payoffHist)
        self.prevPlayedHist.append(self.playedHist)
        self.prevBestPossibleHist.append(self.bestPossibleHist)
        
        if self.s != opponent.s:
            opponent.prevStratHist.append(opponent.stratHist)
            opponent.prevPayoffHist.append(opponent.payoffHist)
            opponent.prevPlayedHist.append(opponent.playedHist)
            opponent.prevBestPossibleHist.append(opponent.bestPossibleHist)
        
        self.prevOpponent.append(opponent)
        if self.s != opponent.s:
            opponent.prevOpponent.append(self)

        # who won? check the sum of rewards
        self.winner(opponent)
    
    def rounds_played(self):
        """Number of rounds each user played."""
        return len(self.prevStratHist)

    def get_points(self):
        return np.cumsum(self.results)

class Strategy:
    """Abstract Strategy class to derive other."""

    def __str__(self):
        return "Base"

    def get(self):
        pass

    @staticmethod
    def generatePlayers(num_players, replace=False, fixed=False):
        str_choices = [NICE, BAD, IND, TFT, TF2T, GRT, PRBL, PRBH]
        #ll = 0 if replace else 1
        #lh = 51 if replace else 50
        #hl = 50 if replace else 51
        #hh = 101 if replace else 100
#
        #k = [] # strategies for players
        #while len(k) < num_players:
        #    val = np.random.choice(str_choices)
#
        #    # substitute with useful values if needed
        #    if val == PRBL:
        #        val = np.random.randint(ll, lh)
        #        if (val != IND and val not in k) or replace:
        #            k.append(val)
        #    elif val == PRBH:
        #        val = np.random.randint(hl, hh)
        #        if (val != IND and val not in k) or replace:
        #            k.append(val)
        #    else:
        #        k.append(val)
        #return np.array(k)
        k = np.random.choice(str_choices, num_players, replace=replace)
        maskL = k==PRBL
        k[maskL] = np.repeat(25, maskL.sum()) if fixed else np.random.choice(49, size=maskL.sum(), replace=replace) + 1 # 1 to 49 exclude nice, indifferent
        maskH = k==PRBH
        k[maskH] = np.repeat(75, maskH.sum()) if fixed else np.random.choice(49, size=maskH.sum(), replace=replace) + 51 # 51 to 99 exclude bad, indifferent

        return k
    
class ProbStrategy(Strategy):
    """Strategy class when probability is used."""
    """Span from always nice to always bad players"""

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
    """Plays opponent's second to last move."""

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
