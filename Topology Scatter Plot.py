import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os

colors = ['red', 'blue', 'yellow', 'limegreen', 'mediumorchid', 'lightskyblue', 'orange', 'deeppink', 'purple',
              'darkturquoise', 'greenyellow', 'gold', 'dodgerblue', 'coral', 'green', 'pink', 'blueviolet']

def topology_scatter(wins_to_tops, topologies, destination_directory):
    """
    Creates a scatter plot showing the topology as the
    y-axis and the window as the x-axis

    Input:
    num -- number of windows

    Returns:
    A scatter plot with topologies as the x-axis and
    windows as the y-axis.
    """
    # initialize x and y
    x = []
    y = []

    # area of plotted circles
    area = math.pi * (5)**2

    # sizes plot appropriately
    plt.xticks(np.arange(0, len(wins_to_tops) + 1, 1.0))
    plt.yticks(np.arange(0, len(wins_to_tops.values()) + 1, 1.0))

    # x-axis is window number
    xkeys = wins_to_tops.keys()

    for i in range(len(xkeys)):
        x.append(int(xkeys[i]))

    for i in range(len(topologies)):
        for top in wins_to_tops:
            if topologies[i] == wins_to_tops[top]:
                # y-axis is number of times a topology occurs
                y.append(i)

    t = y

    # makes plot
    plt.scatter(x=x, y=y, s=area, label=topologies, c=t, alpha=1, linewidths=0.1)
    print x, y
    # legend
    plt.legend(y, loc='lower left', scatterpoints=1, ncol=2, columnspacing=0.1)

    # labels axes
    plt.xlabel('Windows', fontsize=10)
    plt.ylabel('Newick Strings', fontsize=10)

    plt.show()
    # saves plot image
    plot = os.path.join(destination_directory,"topologyPlot.png")
    plt.savefig(plot)

    return plot


topology_scatter({'1': '(seq4,((seq1,seq3),seq2),seq0);',
                   '0': '(seq4,(seq1,(seq2,seq3)),seq0);',
                   '3': '(seq1,(seq4,(seq3,seq2)),seq0);',
                   '2': '(seq1,((seq2,seq4),seq3),seq0);',
                   '4': '((seq1,seq2),(seq3,seq4),seq0);'},
                  ['(seq4,((seq1,seq3),seq2),seq0);',
                   '(seq1,(seq4,(seq3,seq2)),seq0);',
                   '((seq1,seq2),(seq3,seq4),seq0);',
                   '(seq4,(seq1,(seq2,seq3)),seq0);',
                   '(seq1,((seq2,seq4),seq3),seq0);',
                   'Other'],
                 'C:\Users\chaba\GitProjects\PhyloVis')