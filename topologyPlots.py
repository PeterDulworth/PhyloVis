from Bio.Graphics.GenomeDiagram import GraphSet
from Bio.Graphics import GenomeDiagram
from collections import defaultdict
from reportlab.lib import colors
import matplotlib.pyplot as plt
from cStringIO import StringIO
from natsort import natsorted
from sys import platform
from Bio import Phylo
from PIL import Image
import numpy as np
import math
import os

"""
Functions for creating plots based on the topologies.
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

# list of colors for plots
COLORS = ['#ff0000', '#0000ff', '#ffff00', '#32cd32', '#ba55d3', '#87cefa', '#ffa500', '#ff1493', '#a020f0',
          '#00ced1', '#adff2f', '#ffd700', '#1e90ff', '#ff7f50', '#008000', '#ffc0cb', '#8a2be2']


def topology_counter():
    """
    Counts the number of times that each topology appears as outputted by
    running RAxML.

    Output:
    topologies_to_counts --- a dictionary mapping topologies to the number of times they appear
    """

    # Get the topology files from the "Topologies" folder
    input_directory = "Topologies"

    # Initialize topology_count to a defaultdict
    topologies_to_counts = defaultdict(int)

    # Iterate over each file in the given directory
    for filename in os.listdir(input_directory):

        # If file is the file with the best tree newick string
        if os.path.splitext(filename)[0] == "Topology_bestTree":
            input_file = os.path.join(input_directory, filename)

            with open(input_file) as f:
                # Read newick string from file
                topology = f.readline()

                # Add to the count for that newick string
                topologies_to_counts[topology] += 1

    return topologies_to_counts


def top_freqs(num, topologies_to_counts):
    """
    Makes three lists containing the top 'num' topology
    frequencies and the labels and sizes for the
    donut plot inputs.
    Inputs:
    num --- number of topologies to be viewed
    topologies_to_counts --- topologies to counts mapping outputted by topology_counter
    Outputs:
    list_of_top_counts --- labels, and sizes
    """
    # initialize lists for plot inputs
    sizes = []
    labels = []

    # initialize list of top 'num' topologies
    list_of_top_counts = []

    # add counts to frequency list
    freqs = []
    for topology in topologies_to_counts:
        freqs.append(topologies_to_counts[topology])

    # get sum of all counts
    total = sum(topologies_to_counts.values())

    # get top 'num' topologies
    for i in range(num):
        count = max(freqs)
        list_of_top_counts.append(count)
        freqs.remove(count)
        # label and size parameters
        labels.append(str(count))
        sizes.append((float(count) / total) * 100)

    # gets topologies less than 'num' most frequent
    if sum(freqs) != 0:
        labels.append('Other Topologies ' + str(len(freqs)))
        sizes.append(sum(freqs) / float(total) * 100)

    return list_of_top_counts, labels, sizes


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


def windows_to_newick(top_topologies):
    """
    Creates a dictionary of window numbers to the topology of that window if
    the newick string contained in the window is a top topology; otherwise the
    window number is mapped to "Other".
    Input:
    top_topologies -- a mapping outputted by top_topologies()
    Returns:
    wins_to_tops --- a dictionary as described above
    tops_list --- a list of the top topologies
    """
    # Get top topologies and initialize dictionary
    tops_list = top_topologies.keys()
    wins_to_tops = {}

    # Iterate over each folder in the given directory
    for filename in natsorted(os.listdir("Topologies")):

        # If file is the file with the topology of the best tree newick string
        if os.path.splitext(filename)[0] == "Topology_bestTree":

            filename = os.path.join("Topologies", filename)

            # Open file and read newick string
            with open(filename) as f:
                # Read newick string from file
                newick = f.readline()

            window_number = int((os.path.splitext(filename)[1]).replace(".", ""))

            # Only map windows to newick strings that are in the top topologies
            if newick in tops_list:

                wins_to_tops[window_number] = newick

            else:

                wins_to_tops[window_number] = "Other"
    # Adds "Other" so all topologies are included with top ones
    tops_list.append("Other")

    return wins_to_tops, tops_list


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
    top_colors = COLORS[:len(ylist)]

    # map colors to topologies so they are the same in scatter plot
    for win in wins_to_tops:
        if wins_to_tops[win] in tops_to_colors.keys():
            scatter_colors.append(tops_to_colors[wins_to_tops[win]])
        else:
            tops_to_colors[wins_to_tops[win]] = top_colors[0]
            scatter_colors.append(tops_to_colors[wins_to_tops[win]])
            top_colors.pop(0)

    return tops_to_colors, scatter_colors, ylist


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
    donut_colors = []

    # sort topologies based on number of occurrences (high to low)
    tops = top_topologies.items()
    topologies = sorted(tops, key=lambda tup: tup[1], reverse=True)

    for i in range(len(topologies)):
        for top2 in tops_to_colors:
            # add color to list if topologies are the same
            if topologies[i][0] == top2:
                donut_colors.append(tops_to_colors[top2])

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
    area = math.pi * (3) ** 2

    # size y-axis on plot
    plt.yticks(np.arange(len(wins_to_tops) + 1, 0))

    # x-axis is window numbers
    x = wins_to_tops.keys()

    x = np.array(x)
    y = np.array(ylist)

    # create legend
    for (i, cla) in enumerate(set(wins_to_tops.values())):
        xc = [p for (j, p) in enumerate(x) if wins_to_tops.values()[j] == cla]
        yc = [p for (j, p) in enumerate(y) if wins_to_tops.values()[j] == cla]
        cols = [c for (j, c) in enumerate(scatter_colors) if wins_to_tops.values()[j] == cla]
        plt.scatter(xc, yc, s=area, c=cols, label=cla, alpha=1)
        plt.grid = True
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, scatterpoints=1)

    # labels axes
    plt.xlabel('Windows', fontsize=10)
    plt.ylabel('Top Newick Strings', fontsize=10)

    # save plot
    plot = "topologyScatter.png"
    plt.savefig(plot)
    plt.clf()


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

            plt.clf()

            count += 1


def generateCircleGraph(file, windows_to_top_topologies, topologies_to_colors, window_size, window_offset):
    """
    Creates genetic circle graph showing the windows and the areas where each topology appears
    Inputs:
    file --- phylip file inputted in GUI
    windows_to_top_topologies --- mapping outputted by windows_to_newick()[0]
    topologies_to_colors --- mapping outputted by topology_colors()[0]
    window_size --- size inputted in GUI
    window_offset --- size inputted in GUI
    Returns:
    A genetic circle graph GenomeAltase.
    """

    ############################# Format Data #############################

    # -1 because top_topologies_to_colors includes 'Other'
    number_of_top_topologies = len(topologies_to_colors) - 1

    # get the length of the sequence
    with open(file) as f:
        length_of_sequences = int(f.readline().split()[1])
    f.close()

    # accounts for offset
    windows_to_top_topologies2 = {}
    for window in windows_to_top_topologies:
        windows_to_top_topologies2[window * window_offset] = windows_to_top_topologies[window]
    windows_to_top_topologies = windows_to_top_topologies2.items()

    # gets windows
    windows = []
    for window_topology in windows_to_top_topologies:
        windows.append(window_topology[0])

    for i in range(length_of_sequences):
        if i not in windows:
            windows_to_top_topologies.append((i, 0))

    # maps data to topologies
    topologies_to_data = {}
    for topology in topologies_to_colors:
        topologies_to_data[topology] = []

    for topology in topologies_to_colors:
        for window in windows_to_top_topologies:
            if topology == window[1]:
                topologies_to_data[topology].append(tuple([window[0], 1]))
            else:
                topologies_to_data[topology].append(tuple([window[0], -0.1]))

    # maps data to colors
    data_to_colors = {}
    for topology in topologies_to_data:
        data_to_colors[str(topologies_to_data[topology])] = topologies_to_colors[topology]

    # removes 'Other' from mapping
    minor_topology_data = topologies_to_data['Other']
    del topologies_to_data['Other']
    data = topologies_to_data.values()

    # separates data into windowed and unwindowed
    windowed_data = []
    nonwindowed_data = []
    for i in range(length_of_sequences):
        if i not in windows:
            nonwindowed_data.append(tuple([i, 1]))
            windowed_data.append(tuple([i, 0]))
        else:
            for j in range(i, i + window_size):
                windowed_data.append((j, 1))
            nonwindowed_data.append(tuple([i, 0]))

    ############################# Build Graph #############################

    # name of the figure
    name = "GenomeAltase"
    graphStyle = 'bar'

    # create the diagram -- highest level container for everything
    diagram = GenomeDiagram.Diagram(name)

    diagram.new_track(
        1,
        greytrack=0,
        name="Track",
        height=2,
        hide=0,
        scale=1,
        scale_color=colors.black,
        scale_font='Helvetica',
        scale_fontsize=6,
        scale_fontangle=45,
        scale_ticks=1,
        scale_largeticks=0.3,
        scale_smallticks=0.1,
        scale_largetick_interval=(length_of_sequences / 6),
        scale_smalltick_interval=(length_of_sequences / 12),
        scale_largetick_labels=1,
        scale_smalltick_labels=0
    )

    diagram \
        .new_track(2, name="Minor Topologies", height=1.0, hide=0, greytrack=0, greytrack_labels=2,
                   greytrack_font_size=8, grey_track_font_color=colors.black, scale=1, scale_ticks=0,
                   axis_labels=0) \
        .new_set('graph') \
        .new_graph(minor_topology_data, style=graphStyle,
                   colour=colors.HexColor(data_to_colors[str(minor_topology_data)]),
                   altcolour=colors.transparent, linewidth=1)

    for i in range(number_of_top_topologies):
        # create tracks -- and add them to the diagram
        if i == 0:
            diagram \
                .new_track(i + 3, name="Track" + str(i + 1), height=1.0, hide=0, greytrack=0,
                           greytrack_labels=2, greytrack_font_size=8, grey_track_font_color=colors.black,
                           scale=1, scale_ticks=0, axis_labels=0) \
                .new_set('graph') \
                .new_graph(data[i], style=graphStyle, colour=colors.HexColor(data_to_colors[str(data[i])]),
                           altcolour=colors.transparent, linewidth=1)
        else:
            diagram \
                .new_track(i + 3, name="Track" + str(i + 1), height=1.0, hide=0, greytrack=0,
                           greytrack_labels=2, greytrack_font_size=8, grey_track_font_color=colors.black,
                           scale=0) \
                .new_set('graph') \
                .new_graph(data[i], style=graphStyle, colour=colors.HexColor(data_to_colors[str(data[i])]),
                           altcolour=colors.transparent, linewidth=1)

    # outer ring shit
    graph_set = GraphSet('graph')
    graph_set.new_graph(nonwindowed_data, style=graphStyle, color=colors.HexColor('#cccccc'),
                        altcolour=colors.transparent)
    graph_set.new_graph(windowed_data, style=graphStyle, color=colors.HexColor('#2f377c'),
                        altcolour=colors.transparent)

    diagram \
        .new_track(i + 4, name="Track" + str(i + 1), height=2, hide=0, greytrack=0, greytrack_labels=2,
                   greytrack_font_size=8, grey_track_font_color=colors.black, scale=0) \
        .add_set(graph_set)

    diagram.draw(format="circular", pagesize='A5', orientation='landscape', x=0.0, y=0.0, track_size=1.88,
                 tracklines=0, circular=0, circle_core=0.3, start=0, end=length_of_sequences - 1)

    # # save the file(s)
    diagram.write(name + ".pdf", "PDF")
    # diagram.write(name + ".eps", "EPS")
    # diagram.write(name + ".svg", "SVG")
    diagram.write(name + ".png", "PNG")


# Run commands below

if __name__ == '__main__':
    # User inputs:
    num = 3
    file = 'phylip.txt'
    windowSize = 10
    windowOffset = 10

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

    generateCircleGraph(file, windows_to_top_topologies, topologies_to_colors, windowSize, windowOffset)

    if platform == "win32":
        os.startfile("GenomeAltase" + ".pdf")

    elif platform == "darwin":
        os.system("open " + "GenomeAltase" + ".pdf")


