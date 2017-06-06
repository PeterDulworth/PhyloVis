import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os

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
    # initialize set and mapping
    seq = set()
    color_map = {}

    # area of plotted circles
    area = math.pi * (5)**2

    colors = ['red', 'blue', 'yellow', 'limegreen', 'mediumorchid', 'lightskyblue', 'orange', 'deeppink', 'purple',
              'darkturquoise', 'greenyellow', 'gold', 'dodgerblue', 'coral', 'green', 'pink', 'blueviolet']

    for i in range(len(top_topologies)):
        # x-axis is window number
        x = i

        # sorts window numbers for legend
        seq.add(i)
        seqs = sorted(seq)

        # sizes plot appropriately
        plt.xticks(np.arange(0, len(top_topologies) + 1, 1.0))
        plt.yticks(np.arange(0, max(top_topologies.values()) + 1, 1.0))

        for top in top_topologies:
            # y-axis is number of times a topology occurs
            y = top_topologies[top]

            # map colors to topologies
            color_map[top] = colors[i]

        # makes plot
        plt.scatter(x=x, y=y[i], s=area, c=color_map[top], alpha=1, linewidths=0.1)

    # legend
    plt.legend(seqs, loc='lower left', scatterpoints=1, ncol=2, columnspacing=0.1)

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