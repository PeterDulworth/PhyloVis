import os
import math
import random
import numpy as np
import matplotlib.pyplot as plt



colors = ['red', 'blue', 'yellow', 'limegreen', 'mediumorchid', 'lightskyblue', 'orange', 'deeppink', 'purple',
              'darkturquoise', 'greenyellow', 'gold', 'dodgerblue', 'coral', 'green', 'pink', 'blueviolet']

def topology_scatter(wins_to_tops, topologies, destination_directory):
    """
    Creates a scatter plot showing the topology as the
    y-axis and the window as the x-axis

    Input:
    wins_to_tops          -- window to topology mapping outputted by windows_to_newick()
    topologies            -- top topology list outputted by windows_to_newick()
    destination_directory -- folder to save outputted image in

    Returns:
    A scatter plot with topologies as the x-axis and
    windows as the y-axis.
    """
    # initialize lists and dictionaries
    y = []
    scatter_colors = []
    tops_to_colors = {}

    # area of plotted circles
    area = math.pi * (5)**2

    # sizes plot appropriately
    plt.xticks(np.arange(0, len(wins_to_tops) + 1, 1.0))
    plt.yticks(np.arange(0, len(wins_to_tops.values()) + 1, 1.0))

    # x-axis is window numbers
    x = wins_to_tops.keys()

    # y-axis is topology number
    for i in range(len(wins_to_tops)):
        for j in range(len(topologies)):
            if topologies[j] == wins_to_tops[i]:
                y.append(j)

    x = np.array(x)
    y = np.array(y)

    # create list of colors of same length as y
    top_colors = colors[:len(y)]

    # map colors to topologies so they are the same in the plot
    for win in wins_to_tops:
        if wins_to_tops[win] in tops_to_colors.keys():
            scatter_colors.append(tops_to_colors[wins_to_tops[win]])
        else:
            tops_to_colors[wins_to_tops[win]] = top_colors[0]
            scatter_colors.append(tops_to_colors[wins_to_tops[win]])
            top_colors.pop(0)

    # create legend
    for (i, cla) in enumerate(set(wins_to_tops.values())):
        xc = [p for (j, p) in enumerate(x) if wins_to_tops.values()[j] == cla]
        yc = [p for (j, p) in enumerate(y) if wins_to_tops.values()[j] == cla]
        cols = [c for (j, c) in enumerate(scatter_colors) if wins_to_tops.values()[j] == cla]
        plt.scatter(xc, yc, s=area, c=cols, label=cla)
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, scatterpoints=1)

    # labels axes
    plt.xlabel('Windows', fontsize=10)
    plt.ylabel('Top Newick Strings', fontsize=10)

    plt.show()

    # saves plot image
    plot = os.path.join(destination_directory,"topologyPlot.png")
    plt.savefig(plot)

    return plot

# topology_scatter({0: '(a, (b, c));', 1: '((a, b), c);',
#                   2: '(a, (b, c));', 3: 'Other'},
#                  ['(a, (b, c));', '((a, c), b);',
#                   '((a, b), c);', 'Other'],
#                  'C:\Users\chaba\GitProjects\PhyloVis')

# topology_scatter({1: '(seq4,((seq1,seq3),seq2),seq0);',
#                    0: '(seq4,(seq1,(seq2,seq3)),seq0);',
#                    3: '(seq1,(seq4,(seq3,seq2)),seq0);',
#                    2: '(seq1,((seq2,seq4),seq3),seq0);',
#                    4: '(seq4,(seq1,(seq2,seq3)),seq0);',
#                    5: 'Other'},
#                  ['(seq4,((seq1,seq3),seq2),seq0);',
#                    '(seq1,(seq4,(seq3,seq2)),seq0);',
#                    '((seq1,seq2),(seq3,seq4),seq0);',
#                    '(seq4,(seq1,(seq2,seq3)),seq0);',
#                    '(seq1,((seq2,seq4),seq3),seq0);',
#                    'Other'],
#                  'C:\Users\chaba\GitProjects\PhyloVis')