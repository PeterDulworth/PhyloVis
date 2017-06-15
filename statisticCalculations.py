import subprocess
import os
from natsort import natsorted
import re
import dendropy
from dendropy import Tree
import math
from dendropy.calculate import treecompare
import matplotlib.pyplot as plt
import numpy as np

def newick_reformat(newick):
    """
    Reformat the inputted newick string to work with the PhyloNet jar file
    "(a:2.5,(b:1.0,c:1.0):1.5)" This format works
    "(a:2.0,(b:1.0,c:1.0):1.0);" This format works
    "(a:2.0,(b:1.0,c:1.0)):1.0;" THIS FORMAT DOES NOT WORK --- trees from RAxML are in this format
    Inputs:
    newick --- an incorrectly formatted newick string
    Output:
    newick --- a correctly formatted newick string
    """

    # Find root length and remove it
    pattern = "(?!.*\))(.*?)(?=\;)"

    newick = re.sub(pattern, '', newick)

    return newick


def calculate_p_of_gt_given_st(species_tree, gene_tree):
    """
    Computes the probability that a gene tree occurs given a species tree. If the taxon names between the two trees are not the
    same then the probability returned is 0.0. If trees are the exact same then probability is 1.0
    Inputs:
    species_tree --- a newick string containing a species tree with branch lengths as outputted by RAxML or inputted by user
    gene_tree --- a newick string containing a gene tree with branch lengths as outputted by RAxML run on windows
    Output:
    p_of_gt_given_st --- the probability that a gene tree occurs given a species tree
    """

    # If species_tree input is a file read in the newick string
    if os.path.isfile(species_tree):
        with open(species_tree) as f:
            species_tree = f.readline()

    # Check if the species tree is formatted correctly for PhyloNet if not reformat it
    if species_tree[-2] != ")" or species_tree[-1] != ")":
        species_tree = newick_reformat(species_tree).replace("\n","")

    # If gene_tree input is a file read in the newick string
    if os.path.isfile(gene_tree):
        with open(gene_tree) as f:
            gene_tree = f.readline()

    # Check if the gene tree is formatted correctly for PhyloNet if not reformat it
    if gene_tree[-2] != ")" or gene_tree[-1] != ")":
        gene_tree = newick_reformat(gene_tree).replace("\n","")

    # print "gt", gene_tree
    # print "st", species_tree

    # Run PhyloNet jar file
    p = subprocess.Popen("java -jar ./pstgt.jar {0} {1}".format(species_tree, gene_tree), stdout=subprocess.PIPE, shell=True)

    # Read output and convert to float
    p_of_gt_given_st = float(p.stdout.readline())

    return p_of_gt_given_st


def calculate_windows_to_p_gtst(species_tree):
    """
    Calculate p(gt|st) for each window and create a mapping of window numbers to probabilities
    Inputs:
    species_tree --- a newick string containing a species tree with branch lengths as outputted by RAxML or inputted by user
    Output:
    windows_to_p_gtst --- a mapping of window numbers to their p(gt|st)
    """

    # Initialize a mapping
    windows_to_p_gtst = {}

    # Iterate over each folder in the given directory
    for filename in natsorted(os.listdir("RAx_Files")):

        # If file is the file with the best tree newick string
        if os.path.splitext(filename)[0] == "RAxML_bestTree":

            window_num = (os.path.splitext(filename)[1]).replace(".","")

            gene_tree_filename = os.path.join("RAx_Files", filename)

            p_gtst = calculate_p_of_gt_given_st(species_tree, gene_tree_filename)

            windows_to_p_gtst[window_num] = p_gtst

    return windows_to_p_gtst


def calculate_robinson_foulds(species_tree, gene_tree, weighted):
    """
    Calculates the Robinson Foulds distances for weighted and unweighted
    trees.

    Input:
    species_tree -- newick file containing the species tree
                      * this should not change *
    gene_tree   -- newick file or newick string containing the tree to
                      be compared to the species tree
    weighted       -- boolean parameter for whether the files have weights

    Returns:
    The weighted and/or unweighted Robinson Foulds distance of the species
    tree and input tree.
    """

    # taxon names
    tns = dendropy.TaxonNamespace()

    # Create dendropy tree from species tree input file
    if os.path.isfile(species_tree):
        species_tree = Tree.get_from_path(species_tree, 'newick', taxon_namespace=tns)

    # Create dendropy tree from species tree input newick string
    else:
        species_tree = Tree.get_from_string(species_tree, 'newick', taxon_namespace=tns)

    # Create dendropy tree from gene tree input file
    if os.path.isfile(gene_tree):
        gene_tree = Tree.get_from_path(gene_tree, 'newick', taxon_namespace=tns)

    # Create dendropy tree from gene tree input newick string
    else:
        gene_tree = Tree.get_from_string(gene_tree, 'newick', taxon_namespace=tns)

    # both weighted and unweighted foulds distance
    if weighted:
        return treecompare.weighted_robinson_foulds_distance(species_tree, gene_tree), \
               treecompare.unweighted_robinson_foulds_distance(species_tree, gene_tree)

    # only unweighted foulds distance
    else:
        return treecompare.unweighted_robinson_foulds_distance(species_tree, gene_tree)


def calculate_windows_to_rf(species_tree, weighted):
    """
    Calculate Robinson-Foulds distance for each window and create a mapping of window numbers to RF distance
    Inputs:
    species_tree --- a newick string containing a species tree with branch lengths as outputted by RAxML or inputted by user
    weighted --- a boolean corresponding to calculating the weighted or unweighted RF distance
    Output:
    windows_to_rf --- a mapping of window numbers to their RF distance
    """

    # Initialize a mapping for the weighted and unweighted RF distance
    windows_to_w_rf = {}
    windows_to_uw_rf = {}

    # Iterate over each folder in the given directory
    for filename in natsorted(os.listdir("RAx_Files")):

        # If file is the file with the best tree newick string
        if os.path.splitext(filename)[0] == "RAxML_bestTree":
            window_num = (os.path.splitext(filename)[1]).replace(".", "")

            gene_tree_filename = os.path.join("RAx_Files", filename)

            rf_distance = calculate_robinson_foulds(species_tree, gene_tree_filename, weighted)

            if weighted:

                # Weighted RF
                windows_to_w_rf[window_num] = rf_distance[0]
                # Unweighted RF
                windows_to_uw_rf[window_num] = rf_distance[1]

            else:

                # Unweighted RF
                windows_to_uw_rf[window_num] = rf_distance

    if weighted:
        return windows_to_w_rf, windows_to_uw_rf

    else:
        return windows_to_uw_rf


def stat_scatter(stat_map, name):
    """
    Creates a scatter plot with the x-axis being the
    windows and the y-axis being the statistic to
    be graphed.

    Input:
    stat_map -- a mapping outputted by either
                calculate_windows_to_p_gtst or
                calculate_windows_to_rf ([0] or [1])
    name -- the name of the mapping so the y-axis and
            file names are labeled correctly

    Returns:
    A scatter plot with windows as the x-axis and
    a statistic as the y-axis.
    """
    # sizes plot circles
    area = math.pi * (3) ** 2

    x_list = []

    # makes x values integers
    xlist = stat_map.keys()
    for j in range(len(xlist)):
        x_list.append(int(xlist[j]))

    x = np.array(x_list)

    # gets y values from dictionary
    ylist = stat_map.values()
    y = np.array(ylist)

    plt.scatter(x, y, s=area, c='#000000', alpha=1)

    # labels x-axis
    plt.xlabel('Windows', fontsize=10)

    # labels y-axis
    if name == 'weightedRF':
        plt.ylabel('Weighted Robinson Foulds Distance', fontsize=10)

        # saves and names plot
        plot = "WeightedFouldsPlot.png"
        plt.savefig(plot)

    elif name == 'unweightedRF':
        plt.ylabel('Unweighted Robinson Foulds Distance', fontsize=10)

        # saves and names plot
        plot = "UnweightedFouldsPlot.png"
        plt.savefig(plot)

    elif name == 'PGTST':
        plt.ylabel('P(gt|st)', fontsize=10)

        # saves and names plot
        plot = "PGTSTPlot.png"
        plt.savefig(plot)

    plt.clf()


# f1 = "C:\Users\chaba\GitProjects\PhyloVis\RAx_Files\RAxML_bestTree.1"
# f2 = "C:\Users\chaba\GitProjects\PhyloVis\RAx_Files\RAxML_bestTree.2"
# stat_scatter(calculate_windows_to_p_gtst(f1), 'PGTST')
# rf = calculate_windows_to_rf(f1, True)

# stat_scatter(rf[0], 'weightedRF')
# stat_scatter(rf[1], 'unweightedRF')

# Run commands below

if __name__ == '__main__':
    # Inputs
    species_tree = "RAx_Files\RAxML_bestTree.0"
    weighted = True

    # Run commands
    windows_to_p_gtst = calculate_windows_to_p_gtst(species_tree)
    stat_scatter(windows_to_p_gtst, "PGTST")

    # Unweighted Robinson-Foulds
    if not weighted:
        windows_to_uw_rf = calculate_windows_to_rf(species_tree, weighted)
        stat_scatter(windows_to_uw_rf, "unweightedRF")

    # Weighted Robinson-Foulds
    if weighted:
        windows_to_w_rf, windows_to_uw_rf = calculate_windows_to_rf(species_tree, weighted)
        stat_scatter(windows_to_w_rf, "weightedRF")
        stat_scatter(windows_to_uw_rf, "unweightedRF")





