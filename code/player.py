from strategy import *

class Player(object):
    """Class to describe a player with strategy and history."""

    def __str__(self):
        return "Player with strategy: {}".format(self.s)

    def __lt__(self, other):
        # compare by player's strategy
        return self.s.id < other.s.id

    # optional: use M = generatePayoffMatrix()
    def __init__(self, k=0, M=np.array([[3,0],[5,1]]), changing=False):
        self.M1 = M
        self.M2 = M.T
        if changing:
            self.c = (1-k/100 if k>=0 else 0.5) # probability to change strategy at the end of the round
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
        if opponent.s != self.s: #they are not the same player
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
            self.bestGivenOther.append(self.M2[action1,:].max())
            self.bestAch.append(self.M2[:,action2].max())
        else:
            self.payoffHist.append(self.M1[action1,action2])
            self.playedHist.append(action1)
            self.bestGivenOther.append(self.M1[:,action2].max())
            self.bestAch.append(self.M1[action1,:].max())

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
        self.bestAch = []
        if self.s.id == GRT: # reset GrT trigger
            self.s.triggered = False

    def metrics(self):
        """Gives the metrics of the player."""
        rew_p = np.cumsum(self.payoffHist)
        yield_p = np.cumsum(self.bestGivenOther)
        best_p = np.cumsum(self.bestAch)
        return rew_p, yield_p, best_p

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

    @staticmethod
    def change_strategy(players, fixed, alternative):
        """Changes the players' strategy randomly."""
        # c in [0,1] where 0 means not cooperative, 1 means cooperative

        count_bad = count_good = 0

        for i in range(len(players)):
            # save old c, generate new c, replace c
            old_c = players[i].c

            if alternative == 1:
                new_c = np.random.uniform(0,1)

            elif alternative == 2:
                if players[i].s.id > IND: # BAD player
                    # if high in the chart go less coop (0.1+0)/2 = 0.05
                    #     low in the chart go more coop (0.1+1)/2 = 0.55
                    new_c = (players[i].c + (i/len(players))**2)/2
                else:
                    # if high in the chart go more coop (0.1+(1-0))/2 = 0.55
                    #     low in the chart go less coop (0.5+(1-1))/2 = 0.25
                    new_c = (players[i].c + (1-i/len(players))**2)/2

            players[i].c = new_c
            
            # get a set of new strategy candidates
            k_strategies = MultiPlayer.change_strategy_check(players[i].s, old_c, new_c)

            if k_strategies is not None:
                # change is possible, there are candidates

                # update counters
                if new_c > old_c:
                    count_good += 1
                else:
                    count_bad += 1

                # select randomly one strategy from the set
                players[i].s = players[i].get_strategy(np.random.choice(k_strategies))
                if players[i].s.id < 0:
                    players[i].c = 0.5 # reset c for TfT,Tf2T,GrT

        return players, count_bad, count_good

    @staticmethod
    def change_strategy_check(strategy, old_c, new_c):
        """Generates a set of random strategies for a player based on its strategy its c and optionally using bounds."""
        THRESHOLD = 0.1

        k_strategies = None
        c_diff = old_c - new_c
        if np.abs(c_diff) > THRESHOLD:
            if new_c < 0.5:
                # new c is lower go to less coop
                if strategy.id < BAD:
                    k_strategies = MultiPlayer.get_random_strategies_list(strategy.id, new_c, to_more_coop=False)
            else:
                # new c is greater go to more coop
                if strategy.id != NICE and strategy.id != GRT:
                    k_strategies = MultiPlayer.get_random_strategies_list(strategy.id, new_c, to_more_coop=True)
        return k_strategies

    @staticmethod
    def get_random_strategies_list(id, c, to_more_coop):
        """Generates a set of random strategies for a player based on its ID and optionally its c and bounds."""
        stat_choices = [TFT, TF2T, GRT]
        MAX_GEN = 6

        if to_more_coop:
            boundL = (1-c)*100
            boundH = min(id, 50) if id >= 0 else 50
        else:
            boundL = max(50, id) if id >= 0 else 50
            boundH = (1-c)*100

        if boundL > boundH: # swap if needed
            boundL, boundH = boundH, boundL

        return np.append(stat_choices, np.random.randint(boundL, boundH+1, size=MAX_GEN))

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
