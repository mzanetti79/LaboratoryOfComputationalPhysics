class Player(object):
    """A class for a player in the tournament.
    This is an abstract base class, not intended to be used directly.
    """ 
    
    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        self.score = 0
        self.memory = []
        self.name = 'Player'

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

class Nice_guy(Player):
    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        Player.__init__(self)
        self.name = 'Nice guy'
        
    def play(self):
        return 1


class Bad_guy(Player):
    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        Player.__init__(self)
        self.name = 'Bad guy'
    
    def play(self):
        return 0



class Tit_for_tat(Player):
    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        Player.__init__(self)
        self.name = 'Tit for tat'
    
    def play(self):
        if(len(self.memory) == 0):
            return 1
        else:
            return self.memory[-1]


class TitFor2Tats(Player):
    """A player starts by cooperating and then defects only after two defects by opponent."""

    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        Player.__init__(self)
        self.name = 'Tit for 2 tats'
    
    def play(self):
        if self.memory[-2:] == [0, 0]:
            return 0
        else:
            return 1

class SuspiciousTitForTat(Player):
    """A player that behaves opposite to Tit For Tat.
    Starts by defecting and then does the opposite of opponent's previous move.
    This the opposite of TIT FOR TAT, also sometimes called BULLY.
    """
    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        Player.__init__(self)
        self.name = 'Suspicious Tit For Tat'

    def play(self):
        if (len(self.memory) == 0):
            return 1
        else:
            return 0