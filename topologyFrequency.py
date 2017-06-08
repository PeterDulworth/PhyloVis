""" Functions for creating circle chart depicting topology frequencies."""
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from Bio import Phylo
from cStringIO import StringIO
from PIL import Image


# list of colors for plots
colors = ['red', 'blue', 'yellow', 'limegreen', 'mediumorchid', 'lightskyblue', 'orange', 'deeppink', 'purple',
              'darkturquoise', 'greenyellow', 'gold', 'dodgerblue', 'coral', 'green', 'pink', 'blueviolet']


def topology_counter():
    """
    Counts the number of times that each topology appears as outputted by RAxML
    Output:
    topologies --- a dictionary mapping topologies to the number of times they appear
    """

    # Get the topology files from the "RAx_Files" folder
    input_directory = "RAx_Files"

    topology_count = defaultdict(int)

    # Iterate over each folder in the given directory
    for filename in os.listdir(input_directory):

        # If file is the file with the best tree newick string
        if os.path.splitext(filename)[0] == "Topology_bestTree":

            input_file = os.path.join(input_directory,filename)

            with open(input_file) as f:

                # Read newick string from file
                topology = f.readline()

                # Add to the count for that newick string
                topology_count[topology] += 1

    return topology_count


def topology_donut(num):
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
    topologies = topology_counter()

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
    plt.savefig("topologyDonut.png")

    return top

print topology_donut(5)

# def windows_to_topologies():
#     """
#     Maps the name of each window to the newick string representing the topology of the RAxML best tree
#     Output:
#     window_topologies --- a dictionary mapping windows to newick strings
#     """
#
#     window_topologies = {}
#
#     rax_dir = ("RAx_Files")
#
#     # Iterate over each folder in the given directory
#     for filename in os.listdir(rax_dir):
#
#         # If file is the file with the best tree newick string create an image for it
#         if os.path.splitext(filename)[0] == "Topology_bestTree":
#             input_file = os.path.join(rax_dir, filename)
#
#             with open(input_file) as f:
#                 # Read newick string from file
#                 topology = f.readline()
#                 f.close()
#
#                 # Map the number of each window to the corresponding newick string
#                 window_num = (os.path.splitext(filename)[1]).replace(".","")
#                 window_topologies[window_num] = topology
#
#     return window_topologies

# Sample run command
# print windows_to_topologies()

def top_topologies(top, topologies):
    """
    Maps the top 'num' topologies to the number of
    times they occur.

    Inputs:
    top        -- list of top 'num' topology counts
    topologies -- mapping of topologies to the number
    of times they occur.

    Returns:
    top_topologies --- a mapping of the top num topologies 
    to the number of times they occur
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
    window number is mapped to "Other"
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

def topology_scatter(wins_to_tops, topologies):
    """
    Creates a scatter plot showing the topology as the
    y-axis and the window as the x-axis

    Input:
    wins_to_tops          -- window to topology mapping outputted by windows_to_newick()
    topologies            -- top topology list outputted by windows_to_newick()

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

    # Save plot image
    plot = "topologyPlot.png"
    plt.savefig(plot)

    return tops_to_colors

# Example run
# topology_scatter({0: '(a, (b, c));', 1: '((a, b), c);',
#                   2: '(a, (b, c));', 3: 'Other'},
#                  ['(a, (b, c));', '((a, c), b);',
#                   '((a, b), c);', 'Other'],
#                  'C:\Users\chaba\GitProjects\PhyloVis')

def topology_colorizer(color_scheme):
    """
    Create colored tree topology images based on a color scheme where
    the color of a tree is determined by the frequency that it occurs
    Inputs:
    color scheme --- a dictionary mapping newick strings to colors
    """

    # Create a count for the number of the topologies
    count = 0
    # Iterate over each newick string in color_scheme
    for newick in color_scheme:

        if newick != "Other":
            # Create a unique output file for each topology image
            output_file = "Topology" + str(count) + ".png"

            # Create the tree object and assign it to the appropriate color
            tree = Phylo.read(StringIO(newick), "newick")
            tree.rooted = True
            tree.root.color = color_scheme[newick]

            # Create the figure
            fig = plt.figure()
            axes = fig.add_subplot(1, 1, 1)

            # Create the tree image
            Phylo.draw(tree, output_file, axes=axes, do_show=False)

            # Rotate the image and save it
            im = Image.open(output_file)
            im.rotate(-90).save(output_file)

            count += 1

    return

# Example run
# color_scheme = {"((A,B),C);":'red',"((B,C),A);":'blue',"((C,A),B);":'yellow'}
# topology_colorizer(color_scheme)


# Trying to run all of these together

topologies_to_count = topology_counter()

list_of_top_topology_frequencies = topology_donut(num)

# windows_to_all_topologies = windows_to_topologies()

num_of_topologies_to_frequencies = top_topologies(topology_frequency, topologies)

windows_to_top_topologies = windows_to_newick(top_topologies)

# Create scatter plot of the topologies and generate the color scheme
color_scheme = topology_scatter(wins_to_tops, topologies)

# Create the colored topology images
topology_colorizer(color_scheme)






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

