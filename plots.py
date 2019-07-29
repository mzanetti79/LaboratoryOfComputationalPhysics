import random
import numpy as np
import matplotlib.pyplot as plt
import statistics
    
def barPlot(players, scores):
    bins = []
    playersNames = []
    counts = []
    avg_scores = []
    for i in range(len(players)):
        avg_scores.append(statistics.mean(scores[i]))
        playersNames.append(players[i].getName())
    bins = list(dict.fromkeys(playersNames))

    for x in range(len(bins)):
        counts.append(playersNames.count(bins[x]))
    
    startigies_avg = [0] * len(bins)
    for i in range(len(playersNames)):
        for x in range(len(bins)):
            if(bins[x] == playersNames[i]):
                startigies_avg[x]+=avg_scores[i]
    
    for x in range(len(startigies_avg)):
        startigies_avg[x] = startigies_avg[x]/counts[x]
    
    
    fig=plt.figure(figsize=(14, 4), dpi= 80, facecolor='w', edgecolor='k')
    plt.figure(1)
    y_pos = np.arange(len(startigies_avg))
    plt.bar(y_pos, startigies_avg, align='center', alpha=0.5, width=0.5)
    plt.xticks(y_pos, bins)
    plt.xlabel('Name')
    plt.ylabel('Average score')
    plt.title('Players with average scores')
    plt.show()

def plot_cunsum(players_score_matrix, players,ax1):
    players_len= len(players_score_matrix)
    turns=len(players_score_matrix[0])
    x = range(1,turns+1)
    total=sum(sum(np.asarray(players_score_matrix)))
    for i in range(players_len):
        r = lambda: random.randint(20,200)
        g = lambda: random.randint(20,200)
        b = lambda: random.randint(20,200)
        color = '#{:02x}{:02x}{:02x}'.format(r(), g(), b())
        linestyles = ['-', '--', '-.', ':']
        marker = ['.', 'o', '>', 'D', '+']
        y = np.asarray(players_score_matrix[i])
        y = y.cumsum()
        y=y/total
        label= players[i].getName()
        ax1.plot(x, y, marker=random.choice(marker), linestyle=random.choice(linestyles), linewidth=1.5, label=label, color=color)
    # tidy up the figure
    ax1.grid(True)
    ax1.legend(loc='right')
    ax1.set_title('Player Score over turns')
    ax1.set_xlabel('Turns')
    ax1.set_ylabel('Score Fraction')

def plot_box_multiple(scores,players, NUM_REPETITIONS,ax2):
    playersNames=[]
    finalScore=[]
    for i in range(0,len(players)):
        playersNames.append(players[i].getName())
        finalScore.append(scores[i])
    ax2.boxplot(finalScore,showmeans=True)
    plt.xticks(range(1,len(players)+1), playersNames)
    plt.ylabel('Reward')
    plt.title("Means Scores for {} iterations".format(NUM_REPETITIONS))


def plot_two_functions(scores,players, NUM_REPETITIONS):
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(10, 4))
    plot_cunsum(scores,players,ax1)
    plot_box_multiple(scores,players,10,ax2)
    plt.tight_layout() 
    plt.show()

# iterPlayers is a matrix of Player objects
# iterPlayers.shape = (number_of_iterations, number_of_players)
def plot_iterPlayers(iterPlayers, ax):
    iterPlayers = np.array(iterPlayers)
    strats = {}
    iterations = iterPlayers.shape[0]
    # count the number of players for each strategy in each iteration
    # result => strats = {startegyName:[num_of_players_in_iteration_1, ...iteration_2, _3,...,.._15]}
    for i,iP in enumerate(iterPlayers):
        for player in iP:
            strategyName = player.getName()
            if(strategyName not in strats):
                strats[strategyName] = np.zeros(iterations)
            strats[strategyName][i] += 1
    for strat in strats:
        r = lambda: random.randint(20,200)
        g = lambda: random.randint(20,200)
        b = lambda: random.randint(20,200)
        color = '#{:02x}{:02x}{:02x}'.format(r(), g(), b())
        y = np.asarray(strats[strat])
        x = range(1,iterations+1)
        ax.plot(x, y, 'k--', linewidth=1.5, label=strat, color=color)
    # tidy up the figure
    ax.grid(True)
    ax.legend(loc='right')
    ax.set_title('Number of players for each strategy over generations')
    ax.set_xlabel('iterations')
    ax.set_ylabel('number of players')

# Plot totals
def plot_totals(totals, ax):
    ax.plot(totals)
    ax.set_title('Total score for all players in each generation')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Total score')

def plot_totals_iterPlayers(totals,iterPlayers):
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(14, 4))
    plot_totals(totals, ax2)
    plot_iterPlayers(iterPlayers, ax1)
    plt.tight_layout() 
    plt.show()