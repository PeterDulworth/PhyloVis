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
colors = ['#ff0000', '#0000ff', '#ffff00', '#32cd32', '#ba55d3', '#87cefa', '#ffa500', '#ff1493', '#a020f0',
          '#00ced1', '#adff2f', '#ffd700', '#1e90ff', '#ff7f50', '#008000', '#ffc0cb', '#8a2be2']

def topology_counter():
    """
    Counts the number of times that each topology appears as outputted by RAxML
    Output:
    topologies --- a dictionary mapping topologies to the number of times they appear
    """

    # Get the topology files from the "Topologies" folder
    input_directory = "Topologies"

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

def top_freqs(num, topologies):
    """
    Makes three lists containing the top 'num' topology
    frequencies and the labels and sizes for the
    donut plot inputs.

    Input:
    num        -- number of topologies to be viewed
    topologies -- topologies mapping outputted by
    topology_counter()

    Returns:
    Three lists top, labels, and sizes
    """
    # initialize lists for plot inputs
    sizes = []
    labels = []

    # initialize list of top 'num' topologies
    top = []

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
        sizes.append((float(count) / total) * 100)

    # gets topologies less than 'num' most frequent
    if sum(freqs) != 0:
        labels.append('Other Topologies '+str(len(freqs)))
        sizes.append(sum(freqs) / float(total) * 100)

    return top, labels, sizes

def top_topologies(num, topologies):
    """
    Maps the top 'num' topologies to the number of
    times they occur.

    Inputs:
    num        -- number of topologies to analyze
    topologies -- mapping outputted by topology_counter()

    Returns:
    top_topologies --- a mapping of the top 'num' topologies
    to the number of times they occur.
    """
    # initialize mapping
    top_topologies = {}

    # gets and sorts tuples of (topology, frequency)
    tops = topologies.items()
    tops = sorted(tops, key=lambda tup: tup[1], reverse=True)

    # maps top 'num' topologies to frequencies
    for i in range(num):
        top_topologies[tops[i][0]] = tops[i][1]

    return top_topologies

# print top_topologies(5, topology_counter())

def windows_to_newick(top_topologies):
    """
    Creates a dictionary of window numbers to the topology of that window if
    the newick string contained in the window is a top topology; otherwise the
    window number is mapped to "Other".

    Input:
    top_topologies -- a mapping outputted by top_topologies()

    Returns:
    wins_to_tops --- a dictionary as described above
    """

    ###May be possible to optimize this so it doesn't have to iterate over files that aren't Topology_bestTree
    tops_list = top_topologies.keys()

    wins_to_tops = {}

    # Iterate over each folder in the given directory
    for filename in os.listdir("Topologies"):

        # If file is the file with the topology of the best tree newick string
        if os.path.splitext(filename)[0] == "Topology_bestTree":

            filename = os.path.join("Topologies", filename)

            # Open file and read newick string
            with open(filename) as f:
                # Read newick string from file
                newick = f.readline()

            window_number = int((os.path.splitext(filename)[1]).replace(".",""))

            # Only map windows to newick strings that are in the top topologies
            if newick in tops_list:

                wins_to_tops[window_number] = newick

            else:

                wins_to_tops[window_number] = "Other"
    tops_list.append("Other")

    return wins_to_tops, tops_list

# Example run
# print windows_to_newick(top_topologies(tls[0], topology_counter()))

def topology_colors(wins_to_tops, tops_list):
    """
    Maps topologies to colors and makes two lists
    containing the colors for the scatter plot and
    the y-axis values.

    Input:
    wins_to_tops -- mapping outputted by windows_to_newick()[0]
    tops_list    -- list outputted by windows_to_newick()[1]

    Returns:
    A mapping tops_to_colors and two lists scatter_colors and
    ylist.
    """
    # initialize dictionaries and ylist
    scatter_colors = []
    tops_to_colors = {}
    ylist = []

    # y-axis is topology number
    for i in range(len(wins_to_tops)):
        for j in range(len(tops_list)):
            if tops_list[j] == wins_to_tops[i]:
                ylist.append(j)

    # create list of colors of same length as number of windows
    top_colors = colors[:len(ylist)]

    # map colors to topologies so they are the same in the plot
    for win in wins_to_tops:
        if wins_to_tops[win] in tops_to_colors.keys():
            scatter_colors.append(tops_to_colors[wins_to_tops[win]])
        else:
            tops_to_colors[wins_to_tops[win]] = top_colors[0]
            scatter_colors.append(tops_to_colors[wins_to_tops[win]])
            top_colors.pop(0)

    return tops_to_colors, scatter_colors, ylist

# tscolors = topology_colors(windows_to_newick(top_topologies(5, topology_counter()))[0],
#                            windows_to_newick(top_topologies(5,topology_counter()))[1])

def donut_colors(top_topologies, tops_to_colors):
    """
    Makes a color list formatted for use in the donut chart
    so that it matches the scatter plot.

    Input:
    top_topologies -- mapping outputted by top_topologies()
    tops_to_colors -- mapping outputted by tops_to_colors()

    Returns:
    A list donut_colors.
    """
    # initialize color list
    cols = []

    for top1 in top_topologies:
        for top2 in tops_to_colors:
            # add color to list if topologies are the same
            if top1 == top2:
                cols.append(tops_to_colors[top2])

    # reverse color list for counterclockwise plotting
    donut_colors = list(reversed(cols))

    # add color mapped to 'Other' to end of list
    for color in tops_to_colors.values():
        if color not in donut_colors:
            donut_colors.append(color)

    return donut_colors


def topology_donut(num, top, labels, sizes, donut_colors):
    """
    Creates a donut chart showing the breakdown of the top 'num'
    topologies.

    Inputs:
    num    -- the number of topologies to be shown
    top    -- a list of the top frequencies outputted by
              top_freqs()[0]
    labels -- a list of labels outputted by top_freqs()[1]
    sizes  -- a list of sizes outputted by top_freqs()[2]
    donut_colors -- a list of colors outputted by
                    donut_colors()

    Returns:
    A donut chart with the number of times a topology occurs and
    'Other Topologies' for topologies that occur less than the
    most frequent 'num' topologies as the labels, and a list tops
    of the top 'num' scores.
    """
    # plots pie chart
    plt.pie(sizes, explode=None, labels=labels,
        colors=donut_colors, autopct=None, shadow=False)

    # impose circle over pie chart to make a donut chart
    circle = plt.Circle((0, 0), 0.65, color='black', fc='white',
                        linewidth=1.25)
    fig = plt.gcf()
    fig.gca().add_artist(circle)

    # set axes equal
    plt.axis('equal')

    # save plot
    plt.savefig("topologyDonut.png")
    plt.clf()

# topology_donut(5, tls[0], tls[1], tls[2])

# Sample run command
# print windows_to_topologies()

def topology_scatter(wins_to_tops, scatter_colors, ylist):
    """
    Creates a scatter plot showing the topology as the
    y-axis and the window as the x-axis.

    Input:
    wins_to_tops   -- window to topology mapping outputted by windows_to_newick()[0]
    scatter_colors -- list of colors outputted by topology_colors()[1]
    ylist          -- list of y-axis values outputted by topology_colors()[2]

    Returns:
    A scatter plot with topologies as the x-axis and
    windows as the y-axis.
    """
    # area of plotted circles
    area = math.pi * (5)**2

    # sizes plot appropriately
    plt.xticks(np.arange(0, len(wins_to_tops) + 1, 1.0))
    plt.yticks(np.arange(0, len(wins_to_tops) + 1, 1.0))

    # x-axis is window numbers
    x = wins_to_tops.keys()

    x = np.array(x)
    y = np.array(ylist)

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
    # Save plot
    plot = "topologyPlot.png"
    plt.savefig(plot)
    plt.clf()

# Example run
# topology_scatter(windows_to_newick(top_topologies(5, topology_counter()))[0], tscolors[1], tscolors[2])

def topology_colorizer(color_scheme):
    """
    Create colored tree topology images based on a color scheme where
    the color of a tree is determined by the frequency that it occurs.

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

# Example run
# color_scheme = {"((A,B),C);":'red',"((B,C),A);":'blue',"((C,A),B);":'yellow'}
# color_scheme2 = topology_colors(windows_to_newick(top_topologies(tls[0], topology_counter()))[0], topology_counter())[0]
# topology_colorizer(color_scheme2)


### Trying to run all of these together

# User inputs:
num = 3

# Function calls for plotting inputs:
topologies_to_counts = topology_counter()

list_of_top_counts, labels, sizes = top_freqs(num, topologies_to_counts)

top_topologies_to_counts = top_topologies(num, topologies_to_counts)

windows_to_top_topologies, top_topologies_list = windows_to_newick(top_topologies_to_counts)

topologies_to_colors, scatter_colors, ylist = topology_colors(windows_to_top_topologies, top_topologies_list)

donut_colors = donut_colors(top_topologies_to_counts, topologies_to_colors)

# Functions for creating plots
topology_scatter(windows_to_top_topologies, scatter_colors, ylist)
topology_donut(num, list_of_top_counts, labels, sizes, donut_colors)
topology_colorizer(topologies_to_colors)

print topologies_to_colors
print "Scatter", scatter_colors
print "Donut", donut_colors


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