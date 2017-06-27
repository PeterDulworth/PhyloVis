from Bio.Graphics.GenomeDiagram import GraphSet
from Bio.Graphics import GenomeDiagram
from collections import defaultdict
from reportlab.lib import colors
import matplotlib
matplotlib.use('Qt4Agg') # necessary for mac pls don't remove -- needs to be before pyplot is imported but after matplotlib is imported
from matplotlib import pyplot as plt
from cStringIO import StringIO
from natsort import natsorted
from sys import platform
from Bio import Phylo
from PIL import Image
import numpy as np
import math
import os
from dendropy.calculate import treecompare
from dendropy import Tree
import dendropy

"""
Functions for creating plots based on the topologies.
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

# list of colors for plots
COLORS = ['#ff0000', '#0000ff', '#ffff00', '#32cd32', '#ba55d3', '#87cefa', '#ffa500', '#ff1493', '#a020f0',
          '#00ced1', '#adff2f', '#ffd700', '#1e90ff', '#ff7f50', '#008000', '#ffc0cb', '#8a2be2']

def topology_counter(rooted=False, outgroup=None):
    """
    Counts the number of times that each topology appears as outputted by
    running RAxML.

    Output:
    topologies_to_counts --- a dictionary mapping topologies to the number of times they appear
    """

    # Initialize a dictionary mapping newick strings to unique topologies
    unique_topologies_to_newicks = {}

    # taxon names
    tns = dendropy.TaxonNamespace()

    # Create a set of unique topologies
    unique_topologies = set([])

    # Get the topology files from the "Topologies" folder
    input_directory = "Topologies"

    # Initialize topology_count to a defaultdict
    topologies_to_counts = defaultdict(int)

    # Iterate over each file in the given directory
    for filename in os.listdir(input_directory):

        # Create a boolean flag for determining the uniqueness of tree
        new_tree_is_unique = True

        # If file is the file with the best tree newick string
        if os.path.splitext(filename)[0] == "Topology_bestTree":
            input_file = os.path.join(input_directory, filename)

            new_tree = Tree.get_from_path(input_file, 'newick', taxon_namespace=tns)

            if rooted:
                outgroup_node = new_tree.find_node_with_taxon_label(outgroup)
                new_tree.to_outgroup_position(outgroup_node, update_bipartitions=False)

            # Iterate over each topology in unique_topologies
            for unique_topology in unique_topologies:

                # Create a tree for each of the unique topologies calculate RF distance compared to new_tree
                unique_tree = Tree.get_from_string(unique_topology, 'newick', taxon_namespace=tns)
                rf_distance = treecompare.unweighted_robinson_foulds_distance(unique_tree, new_tree)

                # If the RF distance is 0 then the new tree is the same as one of the unique topologies
                if rf_distance == 0:
                    topologies_to_counts[unique_topology] += 1
                    new_tree_is_unique = False
                    new_tree = new_tree.as_string("newick").replace("\n", "")
                    unique_topologies_to_newicks[unique_topology].add(new_tree)
                    break

            # If the new tree is a unique tree add it to the set of unique topologies
            if new_tree_is_unique:
                new_tree = new_tree.as_string("newick").replace("\n","")
                unique_topologies.add(new_tree)
                topologies_to_counts[new_tree] += 1
                unique_topologies_to_newicks[new_tree] = set([new_tree])

    return topologies_to_counts, unique_topologies_to_newicks


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


def windows_to_newick(top_topologies_to_counts, unique_topologies_to_newicks, rooted=False, outgroup=None):
    """
    Creates a dictionary of window numbers to the topology of that window if
    the newick string contained in the window is a top topology; otherwise the
    window number is mapped to "Other".
    Input:
    unique_topologies_to_newicks -- a mapping outputted by topology_counter()
    Returns:
    wins_to_tops --- a dictionary as described above
    tops_list --- a list of the top topologies
    """

    # Initialize dictionary
    tops_list = top_topologies_to_counts.keys()
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

            if rooted:
                # taxon names
                tns = dendropy.TaxonNamespace()

                # Create tree root it and return newick string
                new_tree = Tree.get_from_path(filename, 'newick', taxon_namespace=tns)
                outgroup_node = new_tree.find_node_with_taxon_label(outgroup)
                new_tree.to_outgroup_position(outgroup_node, update_bipartitions=False)
                newick = new_tree.as_string("newick").replace("\n","")

            window_number = int((os.path.splitext(filename)[1]).replace(".", ""))

            for unique_topology in unique_topologies_to_newicks:

                # If the newick string is in the set of newick strings corresponding to the unique topology
                if newick in unique_topologies_to_newicks[unique_topology]:

                    # If the unique topology is a top topology map to it
                    if unique_topology in tops_list:
                        wins_to_tops[window_number] = unique_topology

                    # Otherwise map to "Other"
                    else:
                        wins_to_tops[window_number] = "Other"

                        if "Other" not in tops_list:
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
    A mapping tops_to_colors and two lists scatter_colors andylist.
    """

    # initialize dictionaries and ylist
    scatter_colors = []
    tops_to_colors = {}
    ylist = []
    count = 0

    # y-axis is topology number
    for i in range(len(wins_to_tops)):
        for j in range(len(tops_list)):
            if tops_list[j] == wins_to_tops[i]:
                ylist.append(j)
                count += 1
                break

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


def topology_donut(labels, sizes, donut_colors):
    """
    Creates a donut chart showing the breakdown of the top 'num'
    topologies.
    Inputs:
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
    plt.rcParams['patch.edgecolor'] = '#000000'
    plt.pie(sizes, explode=None, labels=labels,
            colors=donut_colors, autopct=None, shadow=False)

    # create circle behind pie chart to outline it
    outer_circle = plt.Circle((0, 0), 1, color='#000000', fill=False,
                              linewidth=1.25)


    # impose circle over pie chart to make a donut chart
    inner_circle = plt.Circle((0, 0), 0.65, color='#000000', fc='#ffffff',
                        linewidth=1.25)
    fig = plt.gcf()
    fig.gca().add_artist(inner_circle)
    fig.gca().add_artist(outer_circle)

    # set axes equal
    plt.axis('equal')

    # plt.tight_layout()
    # save plot
    plt.savefig("topologyDonut.png", dpi=250)
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
        plt.scatter(xc, yc, s=area, c=cols, label=cla, alpha=1, edgecolors='#000000')
        plt.grid = True
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, scatterpoints=1)

    # labels axes
    plt.xlabel('Windows', fontsize=10)
    plt.ylabel('Top Newick Strings', fontsize=10)


    # save plot
    plot = "topologyScatter.png"
    plt.savefig(plot)
    plt.clf()


def topology_colorizer(color_scheme, rooted=False, outgroup=False):
    """
    Create colored tree topology images based on a color scheme where
    the color of a tree is determined by the frequency that it occurs.
    Inputs:
    color scheme --- a dictionary mapping newick strings to colors
    rooted --- a boolean parameter corresponding to the tree being rooted
    outgroup --- a string of the desired taxon to root at
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
            tree.rooted = rooted

            if outgroup:
                tree.root_with_outgroup(outgroup)

            tree.root.color = color_scheme[newick]

            # Create the figure
            fig = plt.figure()
            axes = fig.add_subplot(1, 1, 1)

            # Create the tree image
            Phylo.draw(tree, output_file, axes=axes, do_show=False)
            plt.tight_layout()

            # Rotate the image and save it
            im = Image.open(output_file)
            im.rotate(-90).save(output_file)

            plt.clf()

            count += 1


def generateCircleGraph(file, windows_to_top_topologies, topologies_to_colors, window_size, window_offset, sites_to_informative):
    """
    Creates genetic circle graph showing the windows and the areas where each topology appears
    Inputs:
    file --- phylip file inputted in GUI
    windows_to_top_topologies --- mapping outputted by windows_to_newick()[0]
    topologies_to_colors --- mapping outputted by topology_colors()[0]
    window_size --- size inputted in GUI
    window_offset --- size inputted in GUI
    Returns:
    A genetic circle graph GenomeAtlas.
    """

    ############################# Format Data #############################

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

    includeOther = False
    if 'Other' in topologies_to_data:
        includeOther = True
        # -1 because top_topologies_to_colors includes 'Other'
        number_of_top_topologies = len(topologies_to_colors) - 1
    else:
        number_of_top_topologies = len(topologies_to_colors)

    # removes 'Other' from mapping
    if includeOther:
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
    name = "GenomeAtlas"
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

    if includeOther:
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
        .new_track(i + 5, name="Track" + str(i + 2), height=2, hide=0, greytrack=0, greytrack_labels=2,
                   greytrack_font_size=8, grey_track_font_color=colors.black, scale=0) \
        .add_set(graph_set)

    ############################################

    diagram \
        .new_track(i + 4, name="Track" + str(i + 1), height=1.0, hide=0, greytrack=0,
                   greytrack_labels=2, greytrack_font_size=8, grey_track_font_color=colors.black,
                   scale=0) \
        .new_set('graph') \
        .new_graph(sites_to_informative.items(), style='line', colour=colors.coral,
                   altcolour=colors.transparent, linewidth=0.01)

    ###########################################################

    diagram.draw(format="circular", pagesize='A5', orientation='landscape', x=0.0, y=0.0, track_size=1.88,
                 tracklines=0, circular=0, circle_core=0.3, start=0, end=length_of_sequences - 1)

    # save the file
    diagram.write(name + ".pdf", "PDF")
    # diagram.write(name + ".eps", "EPS")
    # diagram.write(name + ".svg", "SVG")
    diagram.write(name + ".png", "PNG")

# Run commands below

if __name__ == '__main__':

    # sites_to_informative = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1, 38: 1, 39: 1, 40: 1, 41: 1, 42: 1, 43: 1, 44: 1, 45: 1, 46: 1, 47: 1, 48: 1, 49: 1, 50: 1, 51: 1, 52: 1, 53: 1, 54: 1, 55: 1, 56: 1, 57: 1, 58: 1, 59: 1, 60: 1, 61: 1, 62: 1, 63: 1, 64: 1, 65: 1, 66: 1, 67: 1, 68: 1, 69: 1, 70: 1, 71: 1, 72: 1, 73: 1, 74: 1, 75: 1, 76: 1, 77: 1, 78: 1, 79: 1, 80: 1, 81: 1, 82: 1, 83: 1, 84: 1, 85: 1, 86: 1, 87: 1, 88: 1, 89: 1, 90: 1, 91: 1, 92: 1, 93: 1, 94: 1, 95: 0, 96: 1, 97: 1, 98: 1, 99: 1}

    # User inputs:
    num = 5
    # file = 'phylip.txt'
    file = "testFiles/ChillLeo.phylip"
    windowSize = 10000
    windowOffset = 10000
    rooted = False
    outgroup = "seq5"

    # Function calls for plotting inputs:
    # topologies_to_counts, unique_topologies_to_newicks = topology_counter()
    topologies_to_counts, unique_topologies_to_newicks = topology_counter(rooted, outgroup)

    if num > len(topologies_to_counts):
        num = len(topologies_to_counts)

    list_of_top_counts, labels, sizes = top_freqs(num, topologies_to_counts)

    top_topologies_to_counts = top_topologies(num, topologies_to_counts)


    windows_to_top_topologies, top_topologies_list = windows_to_newick(top_topologies_to_counts, unique_topologies_to_newicks, rooted, outgroup)

    topologies_to_colors, scatter_colors, ylist = topology_colors(windows_to_top_topologies, top_topologies_list)

    donut_colors = donut_colors(top_topologies_to_counts, topologies_to_colors)

    # Functions for creating plots
    topology_scatter(windows_to_top_topologies, scatter_colors, ylist)
    topology_donut(labels, sizes, donut_colors)
    topology_colorizer(topologies_to_colors, rooted, outgroup)

    # generateCircleGraph(file, windows_to_top_topologies, topologies_to_colors, windowSize, windowOffset)
    #
    # if platform == "win32":
    #     os.startfile("GenomeAtlas" + ".png")
    #
    # elif platform == "darwin":
    #     os.system("open " + "GenomeAtlas" + ".png")