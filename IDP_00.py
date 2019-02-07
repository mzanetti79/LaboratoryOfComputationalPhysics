import numpy as np
from random import choices

#Definition of the players

class player:
    
    k = 0
    r = 0
    move = np.array([0, 0]).reshape((2,1))
    
    def __init__(self, strategies):
        self.strategies = strategies
        
    def get_k(self):
        return self.k
    
    def get_strategies(self):
        return self.strategies
    
    def get_move(self):
        return self.move
    
    def get_r(self):
        return self.r
    
    def set_move(self, next_move):
        self.move = np.append(self.move, next_move, axis = 1)
    
    def set_k(self, p):
        self.k = p
        
# Have I to add every time the rewards? or only store the final rewards?
    def set_r(self, h):
        self.r = self.r + h


# Functions

def matrix(R, S, T, P):
    M = np.zeros((2,2))
    M[0,0] = R
    M[0,1] = S
    M[1,0] = T
    M[1,1] = P
    return M

def IPD(player1, player2, M, iter_count):
    
    if iter_count == 0:
        return 

    elif iter_count > 0:
        
        # Computing the u1 and u2 vectors and calculating the rewards for each player
        u1 = chose_strategies(player1, player2)
        u2 = chose_strategies(player2, player1)
        r1 = np.dot(np.dot(u1.T, M), u2)
        r2 = np.dot(np.dot(u2.T, M), u1)
        
        # Storing the rewards
        player1.set_r(int(r1))
        player2.set_r(int(r2))
        
        # Storing the choice
        player1.set_move(u1)
        player2.set_move(u2)
        
        return IPD(player1, player2, M, iter_count-1)

    
# Select the strategies of the player

def chose_strategies(player, opponent):
    
    if player.get_strategies() == "Nice guy":
        return nice_guy()
 
    elif player.get_strategies() == "Bad guy":
        return bad_guy()
        
    elif player.get_strategies() == "Mainly nice":
        return mainly_nice(player.get_k())
    
    elif player.get_strategies() == "Mainly bad":
        return mainly_bad(player.get_k())
        
    elif player.get_strategies() == "Tit-for-tat":
        return tit_for_tat(opponent.get_move())
    else:
        print("Wrong name strategies")
    
# Strategies definitions
        
def nice_guy():
    
    uc = np.array([1,0]).reshape((2,1))
    return uc


def bad_guy():
    
    ud = np.array([0,1]).reshape((2,1))
    return ud


def mainly_nice(k):
    
    uc = np.array([1,0]).reshape((2,1))
    ud = np.array([0,1]).reshape((2,1))
    move = [1, -1]
    prob = [1-k, k]
    value = choices(move, prob) #choices returns a list, find a better way
    if value == [1]:
        return uc
    
    elif value == [-1]:
        return ud

    
def mainly_bad(k):
    
    uc = np.array([1,0]).reshape((2,1))
    ud = np.array([0,1]).reshape((2,1))
    move = [1, -1]
    prob = [1-k, k]
    value = choices(move, prob)
    if value == [1]:
        return uc
    
    elif value == [-1]:
        return ud

    
def tit_for_tat(move):
    
    uc = np.array([1,0]).reshape((2,1))
    ud = np.array([0,1]).reshape((2,1))
    
    if move.shape[1] == 1:
        return uc
    
    last_move = move[:,-1].reshape((2,1))
    if last_move[0] == 1:
        return uc
    
    elif last_move[1] == 1:
        return ud
        

# MAIN

#"Tit-for-tat"
# "Mainly bad"
# "Bad guy"
# K is the probability of being randomly DEFECT for each case, mainly bad and mainly nice

uc = np.array([1,0]).reshape((2,1))
ud = np.array([0,1]).reshape((2,1))

M = matrix(2,0,3,1)
max_iter = 50
player1 = player("Mainly nice")
player1.set_k(0)
player2 = player("Mainly bad") # you have to set k if you adopt mainly..
player2.set_k(1)

a = IPD(player1, player2, M, max_iter)
print("player1 reward: ", player1.get_r())
print("player2 reward: ", player2.get_r())
