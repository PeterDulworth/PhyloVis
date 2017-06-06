""" Functions for creating circle chart depicting topology frequencies."""

import random
import math
import matplotlib.pyplot as plt
from collections import defaultdict
import os

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

#dir = ('C:\Users\chaba\GitProjects\PhyloVis\RAx_Files', '')
#print topology_count(dir)

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
