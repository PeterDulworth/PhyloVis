import re
import os
from dendropy import Tree
import itertools
import math
import ete3
from ete3 import Tree
import copy
import subprocess

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
            network = re.sub(taxon[j], '(' + taxon[j] + ')#H1:0::0.5', network)

        # add 'end' node to network
        elif taxon[j] in network_map.values():
            network = re.sub(taxon[j], '(#H1:0::0.5,' + taxon[j] + ')', network)

    # regular expression for labels in network tree
    labels = ', n\d- '

    # remove node labels at beginning of node
    network = re.sub(labels, ',', network)

    return network


##### Generate all unique trees functions

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
    """
    Generate the set of unique trees over a set of taxa with an outgroup
    Inputs:
    taxa --- a list of taxa to be used as the leaves of trees
    outgroup --- the outgroup to root at
    Output:
    unique_newicks --- a set of all unique topologies over the given taxa
    """

    # Regular expression for identifying floats
    float_pattern = "([+-]?\\d*\\.\\d+)(?![-+0-9\\.])"
    # Regular expressions for removing branch lengths and confidence values
    pattern2 = "([\:][\\d])"
    pattern3 = "([\)][\\d])"


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

            # Compute robinson-foulds distance
            rf_distance = tree.robinson_foulds(unique_tree)[0]

            # If rf distance is 0 the tree is not unique
            if rf_distance == 0:
                is_unique = False

        if is_unique:
            unique_trees.add(tree)

    # Iterate over the trees
    for tree in unique_trees:

        # Get newick strings from the tree objects
        tree = tree.write()

        # Get rid of branch lengths in the newick strings
        tree = (re.sub(float_pattern, '', tree))
        tree = (re.sub(pattern2, '', tree)).replace(":", "")
        tree = (re.sub(pattern3, ')', tree))

        tree = outgroup_reformat(tree, outgroup)

        # Add the newick strings to the set of unique newick strings
        unique_newicks.add(tree)

    return unique_newicks


###### Statistics Calculations Functions

def calculate_newicks_to_stats(species_tree, species_network, unique_trees):
    """
    Compute p(g|S) and p(g|N) for each g in unique_trees and 
    map the tree newick string to those values
    Inputs:
    species_tree --- the species tree newick string for the taxa
    species_network --- the network newick string derived from adding a branch to the species tree between the interested taxa
    unique_trees --- the set of all unique topologies over n taxa
    Output:
    trees_to_pgS--- a mapping of tree newick strings to their p(g|S) values 
    trees_to_pgN--- a mapping of tree newick strings to their p(g|N) values
    """

    trees_to_pgS = {}
    trees_to_pgN = {}

    # Iterate over the trees
    for tree in unique_trees:

        # Run PhyloNet p(g|S) jar file
        p = subprocess.Popen("java -jar ../unstable.jar {0} {1}".format(species_tree, tree), stdout=subprocess.PIPE,
                             shell=True)

        # Read output and convert to float
        p_of_g_given_s = p.stdout.readline()

        # Run PhyloNet p(g|N) jar file
        p = subprocess.Popen("java -jar ../unstable.jar {0} {1}".format(species_network, tree), stdout=subprocess.PIPE,
                             shell=True)

        # Read output and convert to float
        p_of_g_given_n = p.stdout.readline()

        trees_to_pgS[tree] = p_of_g_given_s
        trees_to_pgN[tree] = p_of_g_given_n

    return trees_to_pgS, trees_to_pgN


def determine_interesting_trees(trees_to_pgS, trees_to_pgN):
    """
    Get the subset of trees whose position changes when ordering based on p(g|S) and p(g|N)
    Input:
    trees_to_pgS--- a mapping of tree newick strings to their p(g|S) values 
    trees_to_pgN--- a mapping of tree newick strings to their p(g|N) values
    Output:
    interesting_trees --- the subset of tree topologies to look at for determining introgression
    """

    interesting_trees = set({})

    # Create lists of tuples with newicks strings and their probability values
    # Sort the lists by their probability values
    pgS_list = sorted(trees_to_pgS.items(), key=lambda x: x[1])
    pgN_list = sorted(trees_to_pgN.items(), key=lambda x: x[1])

    # Iterate over indices in the lists
    for i in range(len(pgN_list)):

        # If the newick strings are not the same at each index add them to a set
        if pgS_list[i][0] != pgN_list[i][0]:
            interesting_trees.add(pgS_list[i][0])
            interesting_trees.add(pgN_list[i][0])


    return interesting_trees


##### Site Pattern Functions

def pattern_inverter(patterns):
    """
    Switches "A"s to "B"s and "B"s to "A" in a site pattern excluding the outgroup
    Inputs:
    patterns --- a list of site patterns
    Output:
    inverted --- a list of the inverted patterns
    """

    inverted = []

    # Iterate over the patterns
    for pattern in patterns:

        a_count = 0
        b_count = 0

        inverted_pattern = []

        # Iterate over each site in the pattern
        for site in pattern:

            if site == "A":
                inverted_pattern.append("B")
                b_count += 1

            elif site == "B":
                inverted_pattern.append("A")
                a_count += 1

        if inverted_pattern[-1] != "A":
            # Change the last site to an "A"
            inverted_pattern[-1] = "A"
            b_count -= 1
            a_count += 1

        if a_count > 1 and b_count > 1:
            inverted.append(inverted_pattern)

    return inverted


def site_pattern_generator(taxa_order, newick, outgroup):
    """
    Generate the appropriate AB list patterns
    Inputs:
    taxa_order --- the desired order of the taxa
    newick --- the newick string to generate site patterns for
    outgroup --- the outgroup of the tree
    Output:
    finished_patterns --- the list of site patterns generated for the newick string
    """
    # Create a tree object
    tree = ete3.Tree(newick, format=1)

    # Initialize containers for the final patterns and patterns being altered
    final_site_patterns = []

    # Keep a count of clades in the tree that contain 2 leaves
    clade_count = 0

    # Number of possible patterns is number of taxa - 3
    num_patterns = len(taxa_order) - 3

    # Initialize pattern to be a list of strings
    pattern = ["B" for x in range(len(taxa_order))]

    # Create list of nodes in order of appearance
    nodes = []
    for node in tree.traverse("preorder"):
        # Add node name to list of nodes
        nodes.append(node.name)

    nodes = list(reversed(nodes))
    # Keep track of visited leaves
    seen_leaves = []

    # Iterate over the order that the nodes occur beginning at the root
    for node_idx in range(len(nodes)):

        node = nodes[node_idx]

        # If the node is the outgroup add A to the end of the pattern
        if node == outgroup:
            pattern[-1] = "A"
            # Add outgroup to the seen leaves
            seen_leaves.append(node)

        # Else if the node is a leaf and is adjacent to the outgroup
        elif node != "" and seen_leaves[-1] == outgroup and outgroup in seen_leaves:

            # If the next node is a leaf a clade has been found
            if nodes[node_idx + 1] != "":
                node2 = nodes[node_idx + 1]

                # Get the indices of the leaves in the pattern
                pat_idx1 = taxa_order.index(node)
                pat_idx2 = taxa_order.index(node2)

                # Set those pattern indices to "A"
                pattern[pat_idx1] = "A"
                pattern[pat_idx2] = "A"

                clade_count += 1

                # If there is a clade besides the first one then duplicate it in the list
                final_site_patterns.append(pattern)

                seen_leaves.append(node)
                seen_leaves.append(node2)

                # Get the index that final clade occurs at
                end_idx = node_idx + 1
                break

            # Otherwise there is no clade
            else:
                # Get the index of the leaf in the pattern
                pat_idx = taxa.index(node)

                # Set those pattern indices to "A"
                pattern[pat_idx] = "A"

                seen_leaves.append(node)

                # Get the index that final leaf occurs at
                end_idx = node_idx
                break

    # All patterns can be derived from the pattern with the most B's
    working_patterns = [pattern for x in range(num_patterns)]

    # Pop a pattern off of working patterns and add it to the final site patterns
    final_site_patterns.append(working_patterns.pop())

    # Iterate over each pattern in working patterns and change them
    while working_patterns:

        # Get a pattern and copy it
        pattern = copy.deepcopy(working_patterns.pop())

        # Iterate over the order that the nodes occur beginning at the last clade or leaf
        for node_idx in range(end_idx + 1, len(nodes)):

            # If the last clade is reached break
            if node_idx == len(nodes) - 3:
                break

            node = nodes[node_idx]

            # If the next node is a leaf a clade has been found
            if node != "" and nodes[node_idx + 1] != "":
                node2 = nodes[node_idx + 1]

                # Get the indices of the leaves in the pattern
                pat_idx1 = taxa_order.index(node)
                pat_idx2 = taxa_order.index(node2)

                # Set those pattern indices to "A"
                pattern[pat_idx1] = "A"
                pattern[pat_idx2] = "A"

                clade_count += 1

                # If there is a clade besides the first one then duplicate it in the list
                final_site_patterns.append(pattern)

                # Get the index that final clade occurs at
                end_idx = node_idx + 1
                break

            # Else if the node is a leaf
            elif node != "":
                # Get the index of the leaf in the pattern
                pat_idx1 = taxa_order.index(node)

                # Set those pattern indices to "A"
                pattern[pat_idx1] = "A"

                # Get the index that final leaf occurs at
                end_idx = node_idx
                break

        # Add the altered pattern to the final site patterns
        final_site_patterns.append(pattern)

        # Update the working patterns to be the same as the most recent pattern
        working_patterns = [pattern for x in range(num_patterns - len(final_site_patterns))]

    idx_offset = 0
    # Create a list of patterns without duplicates
    finished_patterns = []
    # Create a list of patterns that are duplicates
    duplicates = []

    # Iterate over each pattern and determine which ones are duplicates
    for pattern_idx in range(len(final_site_patterns) - idx_offset):
        pattern = final_site_patterns[pattern_idx]

        if pattern not in finished_patterns:
            finished_patterns.append(pattern)

        else:
            duplicates.append(pattern)

    # Invert all duplicate patterns
    inverted_patterns = pattern_inverter(duplicates)

    # Iterate over the inverted patterns and add them to finished patterns
    for pattern in inverted_patterns:

        if pattern not in finished_patterns:
            finished_patterns.append(pattern)

    # Convert the site pattern lists to strings
    pattern_strings = []
    while finished_patterns:

        a_count = 0
        b_count = 0
        pattern_str = ""
        pattern = finished_patterns.pop()

        for site in pattern:

            if site == "A":
                b_count += 1

            elif site == "B":
                a_count += 1

            pattern_str += site

        if a_count > 1 and b_count > 1:
            pattern_strings.append(pattern_str)

    return pattern_strings


def newicks_to_patterns_generator(taxa_order, newicks):
    """
    Generate the site patterns for each newick string and map the strings to their patterns
    Inputs:
    taxa_order --- the desired order of the taxa
    newicks --- a list of newick strings
    Output:
    newicks_to_patterns --- a mapping of newick strings to their site patterns
    """

    # Determine the outgroup of the tree
    outgroup = taxa_order[-1]

    newicks_to_patterns = {}

    # Iterate over the newick strings
    for newick in newicks:

        newicks_to_patterns[newick] = site_pattern_generator(taxa_order, newick, outgroup)

    return newicks_to_patterns


def outgroup_reformat(newick, outgroup):
    """
    Move the location of the outgroup in a newick string to be at the end of the string
    Inputs:
    newick --- a newick string to be reformatted
    outgroup --- the outgroup
    """

    # Replace the outgroup and comma with an empty string
    newick = newick.replace(outgroup + ",", "")

    newick = newick[:-2] + "," + outgroup + ");"

    return newick

# print outgroup_reformat('(O,(((P1,P2),(P3,P4)),P5));', "O")

# taxa = ["A", "B", "C", "D", "O"]
# taxa = ["P1", "P2", "P3","O"]
# taxa = ["P1", "P2", "P3", "P4", "O"]
taxa = ["P1", "P2", "P3", "P4", "P5", "O"]
outgroup = "O"
unique = generate_unique_trees(taxa, outgroup)
# print unique
newick_patterns = newicks_to_patterns_generator(taxa, unique)
# print newick_patterns

# newicks = ['(O,(P5,((P1,P2),(P3,P4))));']
# newick_patterns = newicks_to_patterns_generator(taxa, newicks)
# print newick_patterns

# species_tree = "(((P1:0.8,P2:0.8):0.8,P3:0.8),O);"
# species_tree = "(((P1:0.8,P2:0.8):0.8,(P3:0.8,P4:0.8):0.8):0.8,O);"
species_tree = "((((P1:0.8,P2:0.8):0.8,(P3:0.8,P4:0.8):0.8):0.8,P5),O);"
network_map = {"P3":"P1"}
network_tree = network_tree(species_tree, network_map)
trees_to_pgS, trees_to_pgN = calculate_newicks_to_stats(species_tree, network_tree, unique)
# print trees_to_pgS
#
# Create a mapping of newicks to their probability and site pattern
newick_to_pat_n_stat = {}
for newick in newick_patterns:
    for tree in trees_to_pgS:
        if newick == tree:
            newick_to_pat_n_stat[newick] = (newick_patterns[newick],trees_to_pgS[newick])

# print newick_to_pat_n_stat
for i in newick_to_pat_n_stat.items():
    print i







# species_tree = "((((H:0.8,C:0.8):0.8,G:0.8):0.8,B):0.8,O);"
species_tree = ""
network_map = {"G":"H"}

# network_tree = network_tree(species_tree, network_map)
# print network_tree

# trees_to_pgS, trees_to_pgN = calculate_newicks_to_stats(species_tree, network_tree, unique)
# print trees_to_pgS
# print trees_to_pgN
# print determine_interesting_trees(trees_to_pgS, trees_to_pgN)


# n = len(taxa)
# print calculate_num_trees(n), "Actual"
# # print gendistinct(n)
# all = generate_all_trees(taxa)
# # print all
# print len(all), "All"
# unique = generate_unique_trees(taxa, outgroup)
# print len(unique), "Unique"
# all = generate_all_trees(taxa)


