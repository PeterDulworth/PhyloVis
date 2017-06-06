import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os

colors = ['red', 'blue', 'yellow', 'limegreen', 'mediumorchid', 'lightskyblue', 'orange', 'deeppink', 'purple',
              'darkturquoise', 'greenyellow', 'gold', 'dodgerblue', 'coral', 'green', 'pink', 'blueviolet']

def topology_scatter(top_topologies, destination_directory):
    """
    Creates a scatter plot showing the topology as the
    y-axis and the window as the x-axis

    Input:
    num -- number of windows

    Returns:
    A scatter plot with topologies as the x-axis and
    windows as the y-axis.
    """
    # initialize set, count, xlist, and ylist
    i = 0
    seq = []
    x = []
    y = []

    # area of plotted circles
    area = math.pi * (5)**2

    # sizes plot appropriately
    plt.xticks(np.arange(0, len(top_topologies) + 1, 1.0))
    plt.yticks(np.arange(0, max(top_topologies.values()) + 1, 1.0))

    for top in top_topologies:
        # x-axis is window number
        x.append(i)

        # y-axis is number of times a topology occurs
        y.append(top_topologies[top])

        # sorts window numbers for legend
        seq.append(i)

        # increments i for windows
        i += 1

    # makes plot
    plt.scatter(x=x, y=y, s=area, c=colors[:15], alpha=1, linewidths=0.1)

    # legend
    plt.legend(seq, loc='lower left', scatterpoints=1, ncol=2, columnspacing=0.1)

    # labels axes
    plt.xlabel('Windows', fontsize=10)
    plt.ylabel('# of Occurrences', fontsize=10)

    plt.show()
    # saves plot image
    plot = os.path.join(destination_directory,"topologyPlot.png")
    plt.savefig(plot)

    return plot


topology_scatter({'(seq4,((seq1,seq3),seq2),seq0);': 15,
                  '(seq1,(seq4,(seq3,seq2)),seq0);': 7,
                  '((seq1,seq2),(seq3,seq4),seq0);': 5,
                  '(seq4,(seq1,(seq2,seq3)),seq0);': 4,
                  '(seq1,((seq2,seq4),seq3),seq0);': 2},
                 'C:\Users\chaba\GitProjects\PhyloVis')