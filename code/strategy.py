import numpy as np

class Player(object):
    """Class to describe a player with strategy and history."""

    M1 = np.array([[2,0],[3,1]])
    # M1 = np.array([[3,0],[5,2]]) # another good choice
    # or use M = generatePayoffMatrix()
    M2 = M1.T
    
    def __str__(self):
        return "Player with strategy: {}".format(self.s)
    
    def __init__(self, k=0):
        # todo payoff matrix M should be an external parameter
        # todo if strategy may change, methods need to be added
        if k >= 0:
            self.s = ProbStrategy(k)
        elif k == -1:
            self.s = TitForTat()
        self.clear_hist()
    
    def play_iter(self, opponent, num_iter):
        """Plays the game against an opponent num_iter times."""
        for _ in range(num_iter):
            self.play(opponent)

    def play(self, opponent): 
        """Plays the game against an opponent."""
        if type(self.s) != TitForTat:
            action1 = self.s.get()
        else:
            action1 = 0 # cooperate
            if len(opponent.playedHist) > 0:
                action1 = self.s.get(opponent.playedHist[-1]) # pass opponent's move
            
        if type(opponent) != TitForTat:
            action2 = opponent.s.get()
        else:
            action2 = 0
            if len(self.playedHist) > 0:
                action2 = opponent.s.get(self.playedHist[-1]) # todo check if opponent or self
        self.update(action1, action2, False)
        opponent.update(action1, action2, True)
        
    def update(self, action1, action2, opponent):
        """Updates the state based on the actions."""
        self.stratHist.append(str(self.s)) #todo check if better this or k
        if opponent:
            self.payoffHist.append(self.M2[action1,action2])
            self.playedHist.append(action2)
            self.bestPossibleHist.append(max(self.M2[:,action2]))
        else:
            self.payoffHist.append(self.M1[action1,action2])
            self.playedHist.append(action1)
            self.bestPossibleHist.append(max(self.M1[action1,:]))

    def clear_hist(self):
        """Clears all history of the player."""
        self.stratHist = []
        self.payoffHist = []
        self.playedHist = []
        self.bestPossibleHist = []

class MultiPlayer(Player):
    """Class to describe multiple players with strategy and history."""

    def __init__(self, k):
        Player.__init__(self, k)
        
        # save results for multiple rounds played by user
        # this way we can save all the results from the tournament
        self.prevStratHist = []
        self.prevPayoffHist = []
        self.prevPlayedHist = []
        self.prevOpponent = []
        self.results = [] # 'w' = win, 'l' = loss, d' = draw

    def play_iter(self, opponent, num_iter):
        Player.play_iter(self, opponent, num_iter)

        self.prevStratHist.append(self.stratHist)
        self.prevPayoffHist.append(self.payoffHist)
        self.prevPlayedHist.append(self.playedHist)

        opponent.prevStratHist.append(opponent.stratHist)
        opponent.prevPayoffHist.append(opponent.payoffHist)
        opponent.prevPlayedHist.append(opponent.playedHist)

        self.prevOpponent.append(opponent)
        opponent.prevOpponent.append(self)

        # who won? check the sum of rewards
        if np.sum(self.payoffHist) == np.sum(opponent.payoffHist):
            self.results.append('d')
            opponent.results.append('d')
        elif np.sum(self.payoffHist) > np.sum(opponent.payoffHist):
            self.results.append('w')
            opponent.results.append('l')
        else:
            self.results.append('l')
            opponent.results.append('w')

        # set actual history to zero
        self.clear_hist()
        opponent.clear_hist()

    def rounds_played(self):
        """Number of rounds each user played."""
        return len(self.prevStratHist)

    def count_wins(self):
        """Counts the number of rounds won by player."""
        return self.results.count('w')

    def count_losses(self):
        """Counts the number of rounds loss by player."""
        return self.results.count('l')

    def count_draws(self):
        """Counts the number of rounds drawn by player."""
        return self.results.count('d')

class Strategy:
    """Abstract Strategy class to derive other."""

    def __str__(self):
        return "Base"

    def get(self):
        pass

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
