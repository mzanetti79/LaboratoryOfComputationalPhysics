import numpy as np

class Player(object):
    """Class to describe a player with strategy and history."""
    
    def __str__(self):
        return "Player with strategy: {}".format(self.s)
    
    # M1 = np.array([[3,0],[5,2]]) # another good choice
    # or use M = generatePayoffMatrix()
    def __init__(self, k=0, M1=np.array([[3,0],[5,1]])):
        self.M1 = M1
        self.M2 = M1.T

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
        action1 = self.act(opponent)
        action2 = opponent.act(self)
                
        self.update(action1, action2, False)
        opponent.update(action1, action2, True)

    def act(self, opponent):
        if type(self.s) != TitForTat:
            return self.s.get()
        else:
            if len(opponent.playedHist) > 0:
                # print(opponent.playedHist[-1])
                return self.s.get(opponent.playedHist[-1]) # pass opponent's move
            return 0 # cooperate
        
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

    def change(self):
        """Change the strategy randomly"""
        # watch out: each player has a different kH, kL
        kH = np.random.randint(51,100)
        kL = np.random.randint(0,50)
        k_strategies = np.array([0, 100, kL, kH, 50, -1])
        
        proposed = self.propose_change(k_strategies)
            
        while proposed == self.s:
            proposed = self.propose_change(k_strategies)

        self.s = proposed

    def propose_change(self, k_strategies):
        k =  np.random.choice(k_strategies) # gene
        if k >= 0:
            return ProbStrategy(k)
        elif k == -1:
            return TitForTat()
        
    def clear_hist(self):
        """Clears all history of the player."""
        self.stratHist = []
        self.payoffHist = []
        self.playedHist = []
        self.bestPossibleHist = []

class MultiPlayer(Player):
    """Class to describe multiple players with strategy and history."""

    def __init__(self, k, changing = False):
        Player.__init__(self, k)
        
        # save results for multiple rounds played by user
        # this way we can save all the results from the tournament
        self.prevStratHist = []
        self.prevPayoffHist = []
        self.prevPlayedHist = []
        self.prevBestPossibleHist = []
        self.prevOpponent = []
        self.results = [] # 'w' = win, 'l' = loss, d' = draw
        self.changing = changing
        
    # def winner(self,opponent):
    #     if np.sum(self.payoffHist) == np.sum(opponent.payoffHist):
    #         self.results.append('d')
    #         opponent.results.append('d')
    #         if self.changing:
    #             self.change()
    #         if opponent.changing:
    #             opponent.change()
    #     elif np.sum(self.payoffHist) > np.sum(opponent.payoffHist):
    #         self.results.append('w')
    #         opponent.results.append('l')
    #         if opponent.changing:
    #             opponent.change()
    #     else:
    #         self.results.append('l')
    #         opponent.results.append('w')
    #         if self.changing:
    #             self.change()
    
    def winner_alt(self,opponent):
        self.results.append(np.sum(self.payoffHist))
        opponent.results.append(np.sum(opponent.payoffHist))
        
    def play_iter(self, opponent, num_iter):
        Player.play_iter(self, opponent, num_iter)

        self.prevStratHist.append(self.stratHist)
        self.prevPayoffHist.append(self.payoffHist)
        self.prevPlayedHist.append(self.playedHist)
        self.prevBestPossibleHist.append(self.bestPossibleHist)
        
        opponent.prevStratHist.append(opponent.stratHist)
        opponent.prevPayoffHist.append(opponent.payoffHist)
        opponent.prevPlayedHist.append(opponent.playedHist)
        opponent.prevBestPossibleHist.append(opponent.bestPossibleHist)
        
        self.prevOpponent.append(opponent)
        opponent.prevOpponent.append(self)

        # who won? check the sum of rewards
        self.winner_alt(opponent)
                
        # set actual history to zero
        self.clear_hist()
        opponent.clear_hist()
    

    def rounds_played(self):
        """Number of rounds each user played."""
        return len(self.prevStratHist)

    # def count_wins(self):
    #     """Counts the number of rounds won by player."""
    #     return self.results.count('w')

    # def count_losses(self):
    #     """Counts the number of rounds loss by player."""
    #     return self.results.count('l')

    # def count_draws(self):
    #     """Counts the number of rounds drawn by player."""
    #     return self.results.count('d')

    # def get_points(self):
    #     """Counts the points at each match of the player w=3, d=1, l=0."""
    #     points = np.zeros(len(self.results))
    #     points[np.array(self.results) == 'd'] = 1
    #     points[np.array(self.results) == 'w'] = 3
    #     points[np.array(self.results) == 'l'] = 0
    #     return np.cumsum(points)

    def get_points_alt(self):
        # points = np.zeros(len(self.results)) #todo check if useless
        points = self.results
        return np.cumsum(points)

class Strategy:
    """Abstract Strategy class to derive other."""

    def __str__(self):
        return "Base"

    def get(self):
        pass

class ProbStrategy(Strategy):
    """Strategy class when probability is used."""

    def __init__(self, k):
        # default value 0 is to cooperate in case of wrong k
        # todo: check if throwing exception is better
        self.k = k if k>=0 and k<=100 else 0

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
