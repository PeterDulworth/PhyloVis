import re
import os
from dendropy import Tree
import itertools
import math
from ete3 import Tree

"""
Functions:
    
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

def network_tree(species_tree, network_map):
    """
    Creates a network tree based on the species tree
    and the two leaves to be connected.

    Inputs:
    species_tree -- generated or inputted file or newick
                    string
    network_map  -- inputted mapping of leaves where nodes
                    will be added

    Returns:
    A newick string network with the added nodes.
    """
    # check for a species tree file
    if os.path.isfile(species_tree):
        with open(species_tree) as f:
            s_tree = f.readline()

    # check for a species tree string
    else:
        s_tree = species_tree

    # regular expression for commas in species tree
    commas = '[,]'

    # split species tree into parts for labeling
    parts = re.split(commas, s_tree)

    # initialize network tree
    network = ''

    for i in range(len(parts) - 1):
        # label each node in tree
        part = parts[i] + ', n' + str(i) + '- '

        # add part to network
        network += part

    # add last part to network
    network += parts[len(parts) - 1]

    # regular expression for taxa
    taxa = '[A-Z]'

    # get list of taxa in network tree
    taxon = re.findall(taxa, network)

    for j in range(len(taxon)):
        # add 'start' node to network
        if taxon[j] in network_map.keys():
            network = re.sub(taxon[j], '(' + taxon[j] + ')#H1', network)

        # add 'end' node to network
        elif taxon[j] in network_map.values():
            network = re.sub(taxon[j], '(#H1,' + taxon[j] + ')', network)

    # regular expression for labels in network tree
    labels = ', n\d- '

    # remove node labels at beginning of node
    network = re.sub(labels, ',', network)

    return network


def calculate_num_trees(n):
    """
    Calculate the number of unique topologies on n taxa
    Input:
    n --- the number of taxa
    Output:
    num_trees --- the number of trees
    """

    numerator = math.factorial((2 * n - 5))
    denominator = math.factorial((n - 3)) * 2 ** (n - 3)
    num_trees = numerator / denominator

    return num_trees


def gendistinct(n):
    """
    Generate all full binary trees with n leaves
    Input:
    n --- the number of leaves
    Output:
    dp[-1] --- the set of all full binary trees with n nodes
    """

    leafnode = '(.)'
    dp = []
    newset = set()
    newset.add(leafnode)
    dp.append(newset)

    for i in range(1, n):
        newset = set()
        for j in range(i):
            for leftchild in dp[j]:
                for rightchild in dp[i - j - 1]:
                    newset.add('(' + '.' + leftchild + rightchild + ')')
        dp.append(newset)

    return dp[-1]


def generate_all_trees(taxa):
    """
    Create all trees given a set of taxa
    Inputs:
    taxa --- a set of the taxa to be used for leaf names
    Output:
    trees --- the set of all trees over the taxa
    """

    # Regex pattern for identifying leaves next to a clade in newick string
    pattern = "([\)][a-zA-Z0-9_.-])"

    # Generate all distinct binary trees
    trees = gendistinct(len(taxa))

    # Get all possible permutations of the taxa
    taxa_orders = itertools.permutations(taxa)
    taxa_orders = list(taxa_orders)


    all_trees = []

    # Iterate over each tree in the set
    for tree in trees:
        # print 'tree', tree
        # Reformat the tree
        tree = tree.replace('.', '')

        # Iterate over each permutation of taxa
        for taxa_perm in taxa_orders:
            # print 'perm', taxa_perm

            # Create a copy of the tree
            bi_tree = tree

            # replace the leaves with taxons and reformat string
            for i in range(len(taxa_perm)):
                taxon = taxa_perm[i] + ","
                bi_tree = bi_tree.replace("()", taxon, 1)

            bi_tree = bi_tree.replace(",)", ")")

            # Find all instances of a ")" followed by a taxon and add a "," between
            clades = re.findall(pattern, bi_tree)
            for clade in clades:
                taxon = clade[1]
                bi_tree = bi_tree.replace(clade, ")," + taxon)
            bi_tree = bi_tree.replace(")(", "),(")
            bi_tree = bi_tree + ";"
            all_trees.append(bi_tree)

            # print bi_tree

    return all_trees


def generate_unique_trees(taxa, outgroup):
    # Create a set for unique trees
    unique_trees = set([])

    unique_newicks = set([])

    all_trees = generate_all_trees(taxa)

    # Iterate over each tree in all_trees
    for tree in all_trees:

        tree = Tree(tree)
        tree.set_outgroup(outgroup)

        is_unique = True

        # Iterate the unique trees for comparison
        for unique_tree in unique_trees:

            # unique_tree = Tree(unique_tree)
            # unique_tree.set_outgroup(outgroup)

            # Compute robinson-foulds distance
            rf_distance = tree.robinson_foulds(unique_tree)[0]

            # If rf distance is 0 the tree is not unique
            if rf_distance == 0:
                is_unique = False

        if is_unique:
            unique_trees.add(tree)

    for tree in unique_trees:
        unique_newicks.add(tree.write())

    return unique_newicks


taxa = ["H", "C", "O", "P", "X"]
outgroup = "O"
n = len(taxa)
print calculate_num_trees(n), "Actual"
# print gendistinct(n)
all = generate_all_trees(taxa)
# print all
print len(all), "All"
unique = generate_unique_trees(taxa, outgroup)
print len(unique), "Unique"