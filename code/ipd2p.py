import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from mgen import generatePayoffMatrix
from strategy import *

def main():
    # compare results with other version
    np.random.seed(1234)

    # number of iterations
    NUM_ITER = 50

    print("Testing {} iterations of 2-people IPD".format(NUM_ITER))

    # define k for strategy probabilities
    # use k=-1 for TfT
    kH = np.random.randint(51,100)
    kL = np.random.randint(0,50)
    k_strategies = np.array([0, 100, kL, kH, 50, -1])

    for k1 in k_strategies:
        for k2 in k_strategies:
            # todo this does A-B but also B-A, maybe change
            p1 = Player(k1)
            p2 = Player(k2)
            p1.play_iter(p2, NUM_ITER)
            print("Evaluating {} - {}...".format(p1.s,p2.s))
            #print(p1.playedHist)
            #print(p2.playedHist)

            # plot cumulative rewards
            plt.figure(figsize=(15,5))
            rew1 = np.cumsum(p1.payoffHist)
            rew2 = np.cumsum(p2.payoffHist)
            plt.plot(rew1)
            plt.plot(rew2)
            # https://predictablynoisy.com/matplotlib/_images/sphx_glr_colormaps_004.png
            # different dot colors based on action (easiest way to plot points)
            for i in range(0,rew1.size):
                if p1.playedHist[i] == 0:
                    plt.plot(i, rew1[i], 'bx', markersize=8)
                else:
                    plt.plot(i, rew1[i], 'rx', markersize=8)
                    
                if p2.playedHist[i] == 0:
                    plt.plot(i, rew2[i], 'bo', markersize=5)
                else:
                    plt.plot(i, rew2[i], 'ro', markersize=5)

            plt.title("2 pl. game: {} - {}".format(p1.s,p2.s))
            plt.xlabel('Iteration')
            plt.ylabel('Cum. reward')
            # plt.legend(['Player1','Player2'])
            # 0 = cooperate = blue
            plt.legend(handles=[
               # Line2D([0], [0], color='w', marker='_', label='Player 1',
              #            markeredgecolor='b'),
             #   Line2D([0], [0], color='w', marker='_', label='Player 2',
            #              markeredgecolor='r'),
                Line2D([0], [0], color='w', marker='x', label='P.1 Defect',
                          markeredgecolor='r'), 
                Line2D([0], [0], color='w', marker='x', label='P.1 Cooperate',
                          markeredgecolor='b'),      
                Line2D([0], [0], color='w', marker='o', label='P.2 Defect',
                          markerfacecolor='r'), 
                Line2D([0], [0], color='w', marker='o', label='P.2 Cooperate',
                          markerfacecolor='b')
                ])

            # plt.show()
            plt.savefig('../img_v1/idp2p-rewards-{}-{}.png'.format(p1.s,p2.s))
            plt.close()

if __name__ == "__main__":
    main()