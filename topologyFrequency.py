""" Functions for creating circle chart depicting topology frequencies."""
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


# list of colors for plots
colors = ['red', 'blue', 'yellow', 'limegreen', 'mediumorchid', 'lightskyblue', 'orange', 'deeppink', 'purple',
              'darkturquoise', 'greenyellow', 'gold', 'dodgerblue', 'coral', 'green', 'pink', 'blueviolet']


def topology_count(directories):
    """
    Creates phylogenetic tree image files for each newick string file outputted by RAxML
    Inputs:
    directories --- a tuple containing the RAxML Files directory and the destination directory
    Output:
    topologies --- a dictionary mapping topologies to the number of times they appear
    """

    input_directory = directories[0]

    topologies = defaultdict(int)

    # Iterate over each folder in the given directory
    for filename in os.listdir(input_directory):

        # If file is the file with the best tree newick string create an image for it
        if os.path.splitext(filename)[0] == "Topology_bestTree":

            input_file = os.path.join(input_directory,filename)

            with open(input_file) as f:

                # Read newick string from file
                topology = f.readline()

                topologies[topology] += 1

    return topologies


def topology_donut(num, directories):
    """
    Creates a donut chart showing the breakdown of the top 'num'
    topologies.

    Inputs:
    num -- the number of topologies to be shown

    Returns:
    A donut chart with the number of times a topology occurs and
    'Other Topologies' for topologies that occur less than the
    most frequent 'num' topologies as the labels.
    """
    # initialize lists for plot inputs
    sizes = []
    labels = []

    # initialize list of top 'num' topologies
    top = []

    # get topology counts
    topologies = topology_count(directories)

    # add counts to frequency list
    freqs = []
    for n in topologies:
        freqs.append(topologies[n])

    # get sum of all counts
    total = sum(topologies.values())

    # get top 'num' topologies
    for i in range(num):
        count = max(freqs)
        top.append(count)
        freqs.remove(count)
        # label and size parameters
        labels.append(str(count))
        sizes.append((float(count)/ total) * 100)

    # gets topologies less than 'num' most frequent
    if sum(freqs) != 0:
        labels.append('Other Topologies')
        sizes.append(sum(freqs) / float(total) * 100)

    # plots pie chart
    plt.pie(sizes, explode=None, labels=labels,
            colors=colors, autopct=None, shadow=False)

    # impose circle over pie chart to make a donut chart
    circle = plt.Circle((0, 0), 0.65, color='black', fc='white',
                        linewidth=1.25)
    fig = plt.gcf()
    fig.gca().add_artist(circle)

    # set axes equal
    plt.axis('equal')
    plt.show()

    return top

# dir = ('C:\Users\chaba\GitProjects\PhyloVis\RAx_Files', '')
# print topology_donut(5, dir)

def windows_to_topologies(destination_directory):
    """
    Maps the name of each window to the newick string representing the topology of the RAxML best tree
    Inputs:
    destination_directory --- the folder containing all other outputted folders
    Output:
    window_topologies --- a dictionary mapping windows to newick strings
    """

    window_topologies = {}

    rax_dir = os.path.join(destination_directory, "RAx_Files")

    # Iterate over each folder in the given directory
    for filename in os.listdir(rax_dir):

        # If file is the file with the best tree newick string create an image for it
        if os.path.splitext(filename)[0] == "Topology_bestTree":
            input_file = os.path.join(rax_dir, filename)

            with open(input_file) as f:
                # Read newick string from file
                topology = f.readline()
                f.close()

                # Map the number of each window to the corresponding newick string
                window_num = (os.path.splitext(filename)[1]).replace(".","")
                window_topologies[window_num] = topology

    return window_topologies

# Sample run command
# print windows_to_topologies("C:\\Users\\travi\\Documents\\Evolutionary-Diversity-Visualization-Python")
#print windows_to_topologies('C:\Users\chaba\GitProjects\PhyloVis')

def top_topologies(top, topologies):
    """
    Maps the top 'num' topologies to the number of
    times they occur.

    Inputs:
    top        -- list of top 'num' topology counts
    topologies -- mapping of topologies to the number
    of times they occur.

    Returns:
    A mapping top_topologies.
    """
    # initialize mapping
    top_topologies = {}

    # separate most frequent topologies
    for i in range(len(top)):
        for topology in topologies:
            if top[i] == topologies[topology]:
                top_topologies[topology] = top[i]

    return top_topologies

#print top_topologies([1, 1, 1, 1, 1], topology_count(dir))

def windows_to_newick(top_topologies):
    """
    Creates a dictionary of window numbers to the topology of that window if
    the newick string contained in the window is a top topology otherwise the
    window number is mapped to "other"
    Inputs
    topologies --- a list containing the top topologies of the phylogenetic trees
    Output
    wins_to_tops --- a dictionary as described above
    """

    ###May be possible to optimize this so it doesn't have to iterate over files that aren't Topology_bestTree
    topologies = top_topologies.keys()

    wins_to_tops = {}

    # Iterate over each folder in the given directory
    for filename in os.listdir("Rax_Files"):

        # If file is the file with the topology of the best tree newick string
        if os.path.splitext(filename)[0] == "Topology_bestTree":

            filename = os.path.join("Rax_Files", filename)

            # Open file and read newick string
            with open(filename) as f:
                # Read newick string from file
                newick = f.readline()

            window_number = int((os.path.splitext(filename)[1]).replace(".",""))

            # Only map windows to newick strings that are in the top topologies
            if newick in topologies:

                wins_to_tops[window_number] = newick

            else:

                wins_to_tops[window_number] = "Other"
    topologies.append("Other")

    return wins_to_tops, topologies

# Example run
# print windows_to_newick(top_topologies(topology_donut(5, dir), topology_count(dir)))

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