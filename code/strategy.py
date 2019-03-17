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

class Player(object):
    """Class to describe a player with strategy and history."""

    def __str__(self):
        return "Player with strategy: {}".format(self.s)

    # optional: use M = generatePayoffMatrix()
    def __init__(self, k=0, M=np.array([[3,0],[5,1]]), changing=False):
        self.M1 = M
        self.M2 = M.T
        if changing:
            self.c = np.random.uniform(0,1) # probability to change strategy at the end of the round
        else:
            self.c = 0
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
            if len(opponent.playedHist) > 0: # at least 1
                return self.s.get(opponent.playedHist[-1]) # pass opponent's move
            return COOPERATE
        elif type(self.s) == TitFor2Tat:
            if len(opponent.playedHist) > 1: # at least 2
                return self.s.get([opponent.playedHist[-2],opponent.playedHist[-1]]) # pass opponent's previous two moves
            return COOPERATE

    def update(self, action1, action2, opponent):
        """Updates the state based on the actions and if is opponent."""
        if opponent:
            self.payoffHist.append(self.M2[action1,action2])
            self.playedHist.append(action2)
            #COOP = 0 DEFECT = 1
            self.bestGivenOther.append(1 if action1 else 5)
        else:
            self.payoffHist.append(self.M1[action1,action2])
            self.playedHist.append(action1)
            self.bestGivenOther.append(1 if action2 else 5)

    def get_strategy(self, k):
        """Gets the strategy object given the id."""
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
        self.payoffHist = []
        self.playedHist = []
        self.bestGivenOther = []

class MultiPlayer(Player):
    """Class to describe multiple players with strategy and history."""

    def __init__(self, k, changing=False):
        Player.__init__(self, k, changing=changing)

        # save results for multiple rounds played by user
        # this way we can save all the results from the tournament
        self.prevPlayedHist = []
        self.prevOpponent = []
        self.results = []
        self.changing = changing

    # TODO:  Un parametro del nostro grado di cooperazione potrebbe essere la percentuale sul
    # totale di volte che una strategia ha cooperato durante il torneo precedente.
    @staticmethod
    def change_strategy(players, fixed):
        """Change the players' strategy randomly."""
        c_b = 0
        c_g = 0
        k_strategies = Strategy.generatePlayers(len(players)*3, replace=(len(players)*3>Strategy.TOT_STRAT), fixed = fixed)
        for i in range(len(players)):
            if i < len(players)/2:
                ##TODO TUNE THIS, maybe refer to the position
                print("Strategy that gives me good results - reinforce my type")
                print("BEFORE s {}, c {}".format(players[i].s, players[i].c))
                if players[i].s.id > IND:
                    players[i].c = (players[i].c + players[i].c**2)/2
                else:
                    players[i].c = (players[i].c + players[i].c**0.5)/2
                print("AFTER s {}, c {}".format(players[i].s, players[i].c))
            elif i > len(players)/2:
                print("Strategy that gives me bad results - try to change my type in the opposite direction")
                print("BEFORE s {}, c {}".format(players[i].s, players[i].c))
                if players[i].s.id > IND:
                    players[i].c = (players[i].c + players[i].c**0.5)/2
                else:
                    players[i].c = (players[i].c + players[i].c**2)/2
                print("AFTER s {}, c {}".format(players[i].s, players[i].c))
            else:
                print("In the middle, not changing my type s {}, c {}".format(players[i].s, players[i].c))

            #MUTATION PROBABILITY RELATED TO RESULTS
            if np.random.uniform(0,1) < i/len(players):
                #If lower I am tempted to cooperate
                if np.random.uniform(0,1) > players[i].c:
                    print("I am going to a less cooperative behaviour")
                    if players[i].s.id < BAD:
                        s_next = players[i].random_strategy(k_strategies)
                        c_b += 1
                        while str(s_next) == str(players[i].s) or (s_next.id < players[i].s.id or s_next.id < IND):
                            s_next = players[i].random_strategy(k_strategies)
                        players[i].s = s_next
                    print("After change of type I am {}\n\n".format(players[i].s))
                else:
                    print("I am going to a more cooperative behaviour")
                    if players[i].s.id > GRT:
                        s_next = players[i].random_strategy(k_strategies)
                        c_g += 1
                        while str(s_next) == str(players[i].s) or (s_next.id > players[i].s.id or s_next.id > IND):
                            s_next = players[i].random_strategy(k_strategies)
                        players[i].s = s_next
                    print("After change of type I am {}\n\n".format(players[i].s))
            print("\n\n")
        return players, c_b, c_g

    def random_strategy(self, k_list):
        """Generate random strategy object."""
        return self.get_strategy(np.random.choice(k_list))

    def play_iter(self, opponent, num_iter):
        """Plays the game against an opponent num_iter times."""
        Player.play_iter(self, opponent, num_iter)

        # save history for both players
        self.prevPlayedHist.append(self.playedHist)
        if self.s != opponent.s:
            opponent.prevPlayedHist.append(opponent.playedHist)

        self.prevOpponent.append(opponent)
        if self.s != opponent.s:
            opponent.prevOpponent.append(self)

        # check the sum of rewards to detect the winner
        self.winner(opponent)

    def winner(self, opponent):
        """Saves the total payoff of the player."""
        self.results.append(np.sum(self.payoffHist))
        if opponent.s != self.s:
            opponent.results.append(np.sum(opponent.payoffHist))

    def get_points(self):
        """Current gained points."""
        return np.cumsum(self.results)

    def get_coop_def_count(self):
        """Number of times the user cooperated and defected."""
        cooperate_count = defect_count = 0
        for hist in self.prevPlayedHist:
            cooperate_count += hist.count(COOPERATE)
            defect_count += hist.count(DEFECT)
        return cooperate_count, defect_count

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
            return 
        # first time
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
