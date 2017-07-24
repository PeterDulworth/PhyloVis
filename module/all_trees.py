import re
import os
import itertools
import math
import ete3
from ete3 import Tree
import copy
import subprocess
from collections import defaultdict

"""
Functions:
    
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

def generate_network_tree(inheritance, species_tree, network_map):
    """
    Creates a network tree based on the species tree
    and the two leaves to be connected.

    Inputs:
    inheritance  -- inputted tuple containing inheritance
                    probability ex. (0.7, 0.3)
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

    # get taxa for the edge in the network
    start = network_map.keys()[0]
    end = network_map[start]

    # add nodes into tree in proper format
    network = s_tree.replace(start, '((' + start + ')#H1:0::' + str(inheritance[0]) + ')')
    network = network.replace(end, '(#H1:0::' + str(inheritance[1]) + ',' + end + ')')

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


def outgroup_removal(newick, outgroup):
    """
    Move the location of the outgroup in a newick string to be at the end of the string
    Inputs:
    newick --- a newick string to be reformatted
    outgroup --- the outgroup
    """

    # Replace the outgroup and comma with an empty string
    newick = newick.replace("," + outgroup, "")

    newick = newick[1:-2] + ";"

    return newick


def calculate_newicks_to_stats(species_tree, species_network, unique_trees, outgroup):
    """
    Compute p(g|S) and p(g|N) for each g in unique_trees and 
    map the tree newick string to those values
    Inputs:
    species_tree --- the species tree newick string for the taxa
    species_network --- the network newick string derived from adding a branch to the species tree between the interested taxa
    unique_trees --- the set of all unique topologies over n taxa
    outgroup --- the outgroup
    Output:
    trees_to_pgS--- a mapping of tree newick strings to their p(g|S) values 
    trees_to_pgN--- a mapping of tree newick strings to their p(g|N) values
    """

    trees_to_pgS = {}
    trees_to_pgN = {}
    trees_to_pgS_noO = {}
    trees_to_pgN_noO = {}

    species_tree_noO = outgroup_removal(species_tree, outgroup)
    species_network_noO = outgroup_removal(species_network, outgroup)

    # Iterate over the trees
    for tree in unique_trees:

        # Run PhyloNet p(g|S) jar file
        p = subprocess.Popen("java -jar ../unstable.jar {0} {1}".format(species_tree, tree), stdout=subprocess.PIPE,
                             shell=True)

        # Read output and convert to float
        p_of_g_given_s = float(p.stdout.readline())

        # Run PhyloNet p(g|N) jar file
        p = subprocess.Popen("java -jar ../unstable.jar {0} {1}".format(species_network, tree), stdout=subprocess.PIPE,
                             shell=True)

        # Read output and convert to float
        p_of_g_given_n = float(p.stdout.readline())

        # Calculate for trees without outgroup
        tree_noO = outgroup_removal(tree, outgroup)

        # Run PhyloNet p(g|S) jar file
        p = subprocess.Popen("java -jar ../unstable.jar {0} {1}".format(species_tree_noO, tree_noO), stdout=subprocess.PIPE,
                             shell=True)

        # Read output and convert to float
        p_of_g_given_s_noO = float(p.stdout.readline())

        # Run PhyloNet p(g|N) jar file
        p = subprocess.Popen("java -jar ../unstable.jar {0} {1}".format(species_network_noO, tree_noO), stdout=subprocess.PIPE,
                             shell=True)

        # Read output and convert to float
        p_of_g_given_n_noO = float(p.stdout.readline())

        trees_to_pgS[tree] = p_of_g_given_s
        trees_to_pgN[tree] = p_of_g_given_n
        trees_to_pgS_noO[tree] = p_of_g_given_s_noO
        trees_to_pgN_noO[tree] = p_of_g_given_n_noO

    return trees_to_pgS, trees_to_pgN, trees_to_pgS_noO, trees_to_pgN_noO


def determine_interesting_trees(trees_to_pgS, trees_to_pgN):
    """
    Get the subset of trees who are initially equal based on p(g|S) but unequal based on p(g|N)
    Input:
    trees_to_pgS--- a mapping of tree newick strings to their p(g|S) values 
    trees_to_pgN--- a mapping of tree newick strings to their p(g|N) values
    Output:
    interesting_trees --- the subset of tree topologies to look at for determining introgression
    """

    # Initialize a set to contain all tree that are equal based on p(g|S)
    possible_trees = []

    # Compare the probability of each tree to the probability of every other tree
    for tree1 in trees_to_pgS:

        equal_trees = set([])

        for tree2 in trees_to_pgS:

            if trees_to_pgS[tree1] == trees_to_pgS[tree2]:
                equal_trees.add(tree2)

        if len(equal_trees) > 1:
            # Add the equal trees to the set of possible trees
            possible_trees.append(equal_trees)

    valuable_trees = []

    # Iterate over each set of equal trees
    for equal_trees in possible_trees:

        unequal_trees = set([])

        # Compare the p(g|N) values
        for tree1 in equal_trees:

            for tree2 in equal_trees:

                if trees_to_pgN[tree1] != trees_to_pgN[tree2]:
                    unequal_trees.add(tree1)
                    unequal_trees.add(tree2)

        if len(unequal_trees) > 0:
            valuable_trees.append(unequal_trees)

    minimal_size = float("inf")

    # Get the minimal subset of interesting trees
    for trees in valuable_trees:
        if len(trees) < minimal_size:
            minimal_size = len(trees)
            interesting_trees = trees

    return interesting_trees


##### Site Pattern Functions


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

        if a_count > 1 and b_count > 0:
            inverted.append(inverted_pattern)

    return inverted


def pattern_string_generator(patterns):
    """
    Creates a list of viable pattern strings that are easier to read
    Input:
    patterns --- a list of lists of individual characters e.g. [["A","B","B","A"],["B","A","B","A"]]
    Output:
    pattern_strings --- a list of lists of strings e.g. [["ABBA"],["BABA"]]
    """

    # Convert the site pattern lists to strings
    pattern_strings = []
    while patterns:

        a_count = 0
        b_count = 0
        pattern_str = ""
        pattern = patterns.pop()

        for site in pattern:

            if site == "A":
                b_count += 1

            elif site == "B":
                a_count += 1

            pattern_str += site

        if a_count > 0 and b_count > 0:
            pattern_strings.append(pattern_str)

    return pattern_strings


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

    # Number of possible patterns is number of taxa - 2 + the number of clades
    num_patterns = len(taxa_order) - 2

    # Initialize pattern to be a list of strings
    pattern = ["B" for x in range(len(taxa_order))]

    # Create list of nodes in order of appearance
    nodes = []
    for node in tree.traverse("postorder"):
        # Add node name to list of nodes
        nodes.append(node.name)


    nodes = list(reversed(nodes))

    if nodes[2] == "" and nodes[3] == "":
        nodes = []
        for node in tree.traverse("preorder"):
            # Add node name to list of nodes
            nodes.append(node.name)

        nodes = list(reversed(nodes))

    # Keep track of visited leaves
    seen_leaves = []

    # Create a list of patterns that are duplicates
    duplicates = []

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
                duplicates.append(pattern)

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

    num_patterns = num_patterns + clade_count
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
            if node_idx == len(nodes)-1:

                if node != "":
                    # Get the index of the leaf in the pattern
                    pat_idx1 = taxa_order.index(node)

                    # Set those pattern indices to "A"
                    pattern[pat_idx1] = "A"

                    # Get the index that final leaf occurs at
                    end_idx = node_idx
                    break

                else:
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
                duplicates.append(pattern)

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
        duplicates.append(pattern)

        # Update the working patterns to be the same as the most recent pattern
        working_patterns = [pattern for x in range(num_patterns - len(final_site_patterns))]

    # Create a list of patterns without duplicates
    finished_patterns = []

    # Iterate over each pattern and determine which ones are duplicates
    for pattern in final_site_patterns:

        if pattern not in finished_patterns:
            finished_patterns.append(pattern)

        else:
            duplicates.append(pattern)

    # This may need to change double check with Chill Leo on this
    # if clade_count > 1:

    duplicates = finished_patterns

    # Invert all duplicate patterns
    inverted_patterns = pattern_inverter(duplicates)

    # Iterate over the inverted patterns and add them to finished patterns
    for pattern in inverted_patterns:

        if pattern not in finished_patterns:
            finished_patterns.append(pattern)

    finished_patterns = pattern_string_generator(finished_patterns)

    return finished_patterns


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


##### Interesting sites functions


def calculate_pattern_probabilities(newicks_to_patterns, newicks_to_pgS, newicks_to_pgN):
    """
    Creates a mapping of site patterns to their total p(g|S) values across all gene trees and 
    a mapping of site patterns to their total p(g|N) values across all gene trees
    Inputs:
    newicks_to_patterns --- a mapping of tree newick strings to their site patterns
    newicks_to_pgS--- a mapping of tree newick strings to their p(g|S) values 
    newicks_to_pgN--- a mapping of tree newick strings to their p(g|N) values
    Outputs:
    patterns_to_pgS --- a mapping of site patterns to their total p(g|S) value
    patterns_to_pgN --- a mapping of site patterns to their total p(g|N) value
    """

    patterns_to_pgS = {}
    patterns_to_pgN = {}

    # Iterate over each newick string
    for newick in newicks_to_patterns:
        # Iterate over each site pattern of a tree
        for pattern in newicks_to_patterns[newick]:


            # Initialize a probability for each pattern if it does not have one
            if pattern not in patterns_to_pgS:
                patterns_to_pgS[pattern] = newicks_to_pgS[newick]
                patterns_to_pgN[pattern] = newicks_to_pgN[newick]

            # Otherwise add to the existing probability
            else:
                patterns_to_pgS[pattern] += newicks_to_pgS[newick]
                patterns_to_pgN[pattern] += newicks_to_pgN[newick]

    return patterns_to_pgS, patterns_to_pgN


def determine_patterns(patterns_to_pgS, patterns_to_pgN1, patterns_to_pgN2):
    """
    Determine which patterns are useful in determining introgression
    Inputs:
    patterns_to_pgS --- a mapping of site patterns to their total p(g|S) value
    patterns_to_pgN1 --- a mapping of site patterns to their total p(g|N) value for a network
    patterns_to_pgN2 --- a mapping of site patterns to their total p(g|N) value for a different network
    Outputs:
    terms1 --- a set of patterns to count and add to each other to determine introgression
    terms2 --- a set of other patterns to count and add to each other to determine introgression
    """

    # Initialize sets for the patterns of interest
    interesting_patterns = set([])
    terms1 = set([])
    terms2 = set([])

    # Iterate over each pattern to determine the patterns of interest
    for pattern in patterns_to_pgS:

        tree_probability = patterns_to_pgS[pattern]

        # If either network probability is not equal to the tree probability and the network probabilities are not equal the pattern is of interest
        if (patterns_to_pgN1[pattern] != tree_probability or patterns_to_pgN2[pattern] != tree_probability) and patterns_to_pgN1[pattern] != patterns_to_pgN2[pattern]:

            interesting_patterns.add(pattern)

    # Iterate over each interesting pattern and determine which set of terms to add the pattern to
    for pattern in interesting_patterns:

        if patterns_to_pgN1[pattern] > patterns_to_pgN2[pattern]:
            terms1.add(pattern)

        elif patterns_to_pgN2[pattern] > patterns_to_pgN1[pattern]:
            terms2.add(pattern)

    return (terms1, terms2)


def generate_statistic_string(patterns_of_interest):
    """
    Create a string representing the statistic for determining introgression like "(ABBA - BABA)/(ABBA + BABA)"
    Input:
    patterns_of_interest --- a tuple containing the sets of patterns used for determining a statistic
    Output:
    L_statistic --- a string representation of the statistic
    """

    calculation = []

    # Iterate over each set of patterns
    for pattern_set in patterns_of_interest:
        term = "("

        # Combine each term with a "+"
        for pattern in pattern_set:
            term = term + pattern + " + "
        term = term[:-3] + ")"
        calculation.append(term)

    L_statistic = "({0} - {1}) / ({0} + {1})".format(calculation[0], calculation[1])

    return L_statistic


##### Function for calculating statistic


def calculate_L(alignment, taxa_order, patterns_of_interest):
    """
    Calculates the L statistic for the given alignment
    Input:
    alignment --- a sequence alignment in phylip format
    taxa_order --- the desired order of the taxa
    patterns_of_interest --- a tuple containing the sets of patterns used for determining a statistic
    Output:
    l_stat --- the L statistic value
    """

    # Separate the patterns of interest into their two terms
    terms1 = patterns_of_interest[0]
    terms2 = patterns_of_interest[1]

    terms1_counts = defaultdict(int)
    terms2_counts = defaultdict(int)

    sequence_list = []
    taxon_list =[]

    with open(alignment) as f:

        # Create a list of each line in the file
        lines = f.readlines()

        # First line contains the number and length of the sequences
        first_line = lines[0].split()
        length_of_sequences = int(first_line[1])

    for line in lines[1:]:
        # Add each sequence to a list
        sequence = line.split()[1]
        sequence_list.append(sequence)

        # Add each taxon to a list
        taxon = line.split()[0]
        taxon_list.append(taxon)

    # The outgroup is the last taxa in taxa order
    outgroup = taxa_order[-1]

    # Iterate over the site indices
    for site_idx in range(length_of_sequences):

        # Map each taxa to the base at a given site
        taxa_to_site = {}

        # Create a set of the bases at a given site to determine if the site is biallelic
        bases = set([])

        # Iterate over each sequence in the alignment
        for sequence, taxon in zip(sequence_list, taxon_list):
            # Map each taxon to the corresponding base at the site
            base = sequence[site_idx]
            taxa_to_site[taxon] = base
            bases.add(base)

        if len(bases) == 2:

            # Create the pattern that each site has
            site_pattern = []

            # The ancestral gene is always the same as the outgroup
            ancestral = taxa_to_site[outgroup]

            # Iterate over each taxon
            for taxon in taxa_order:
                nucleotide = taxa_to_site[taxon]

                # Determine if the correct derived/ancestral status of each nucleotide
                if nucleotide == ancestral:
                    site_pattern.append("A")
                else:
                    site_pattern.append("B")

            # Convert the site pattern to a string
            site_string = pattern_string_generator([site_pattern])[0]

            # If the site string is a pattern of interest add to its count for one of the terms
            if site_string in terms1:
                terms1_counts[site_string] += 1

            elif site_string in terms2:
                terms2_counts[site_string] += 1

    terms1_total = sum(terms1_counts.values())
    terms2_total = sum(terms2_counts.values())

    numerator = terms1_total - terms2_total
    denominator = terms1_total + terms2_total

    l_stat = numerator/float(denominator)

    return l_stat


def L_statistic(alignment, taxa, species_tree, reticulations):
    """
    Calculates the L statistic for the given alignment
    Input:
    alignment --- a sequence alignment in phylip format
    taxa --- a list of the taxa in the desired order
    species_tree --- the inputted species tree over the given taxa
    reticulations a tuple containing two dictionaries mapping the start leaves to end leaves
    Output:
    l_stat --- the L statistic value
    """

    # The outgroup is the last taxon in the list of taxa
    outgroup = taxa[-1]

    # Generate all unique trees over the given topology
    unique = generate_unique_trees(taxa, outgroup)

    # Map the tree newick strings to their site patterns
    newick_patterns = newicks_to_patterns_generator(taxa, unique)

    # Create species networks
    network_map1, network_map2 = reticulations[0], reticulations[1]
    network1 = generate_network_tree((0.3, 0.7), species_tree, network_map1)
    network2 = generate_network_tree((0.3, 0.7), species_tree, network_map2)


    trees_to_pgS, trees_to_pgN, trees_to_pgS_noO, trees_to_pgN_noO = calculate_newicks_to_stats(species_tree, network1, unique, outgroup)
    patterns_pgS, patterns_pgN1 = calculate_pattern_probabilities(newick_patterns, trees_to_pgS, trees_to_pgN)

    trees_to_pgS, trees_to_pgN, trees_to_pgS_noO, trees_to_pgN_noO = calculate_newicks_to_stats(species_tree, network2, unique, outgroup)
    patterns_pgS, patterns_pgN2 = calculate_pattern_probabilities(newick_patterns, trees_to_pgS, trees_to_pgN)

    patterns_of_interest = determine_patterns(patterns_pgS, patterns_pgN1, patterns_pgN2)

    l_stat = calculate_L(alignment, taxa, patterns_of_interest)

    return l_stat


alignment = "C:\\Users\\travi\\Documents\\PhyloVis\\testFiles\\ChillLeo-Copy.phylip"
taxa = ["P1", "P2", "P3", "O"]
species_tree = "(((P1:0.8,P2:0.8):0.8,P3:0.8),O);"
reticulations = ({"P3":"P2"},{"P3":"P1"})

print L_statistic(alignment,taxa,species_tree,reticulations)



# taxa = ["P1", "P2", "P3","O"]
# # taxa = ["P1", "P2", "P3", "P4", "O"]
# # taxa = ["P1", "P2", "P3", "P4", "P5", "O"]
# # taxa = ["P1", "P2", "P3", "P4", "P5", "P6", "O"]
# outgroup = "O"
# unique = generate_unique_trees(taxa, outgroup)
# # print unique
# newick_patterns = newicks_to_patterns_generator(taxa, unique)
# # print newick_patterns
#
# # species_tree = "(((P1:0.6,P2:0.65):0.4,(P3:0.7,P4:0.75):0.8),O);"
#
# species_tree = "(((P1:0.8,P2:0.8):0.8,P3:0.8),O);"
# # species_tree = "(((P1:0.8,P2:0.8):0.8,(P3:0.8,P4:0.8):0.8),O);"
# # species_tree = "((((P1:0.8,P2:0.8):0.8,(P3:0.8,P4:0.8):0.8):0.8,P5),O);"
# # species_tree = "((((P1:0.8,P2:0.8):0.8,(P3:0.8,P4:0.8):0.8):0.8,(P5:0.8,P6:0.8):0.8),O);"
# network_map = {"P3":"P2"}
# print network_map
# network_tree = generate_network_tree((0.3, 0.7), species_tree, network_map)
#
# trees_to_pgS, trees_to_pgN, trees_to_pgS_noO, trees_to_pgN_noO = calculate_newicks_to_stats(species_tree, network_tree, unique, outgroup)
#
# patterns_pgS, patterns_pgN1 = calculate_pattern_probabilities(newick_patterns, trees_to_pgS, trees_to_pgN)
# # patterns_pgS, patterns_pgN = calculate_pattern_probabilities(newick_patterns, trees_to_pgS_noO, trees_to_pgN_noO)
#
# network_map = {"P3":"P1"}
# print network_map
# network_tree = generate_network_tree((0.3, 0.7), species_tree, network_map)
#
# trees_to_pgS, trees_to_pgN, trees_to_pgS_noO, trees_to_pgN_noO = calculate_newicks_to_stats(species_tree, network_tree, unique, outgroup)
#
# patterns_pgS, patterns_pgN2 = calculate_pattern_probabilities(newick_patterns, trees_to_pgS, trees_to_pgN)
#
# patterns_of_interest = determine_patterns(patterns_pgS, patterns_pgN1, patterns_pgN2)
#
#
# print species_tree
# print
# for pattern in patterns_pgS:
#     print pattern, ":", patterns_pgS[pattern], ":", patterns_pgN1[pattern], ":", patterns_pgN2[pattern]
# print
# print generate_statistic_string(patterns_of_interest)
#
# print
# alignment = "C:\\Users\\travi\\Documents\\PhyloVis\\testFiles\\ChillLeo-Copy.phylip"
# print "L statistic =", calculate_L(alignment, taxa, patterns_of_interest)


# print "Site Pattern probabilities before reticulation from P3 to P2"
# for pattern in patterns_pgS:
#     print pattern, ":", patterns_pgS[pattern]
#
# print
#
# print "Site Pattern probabilities after reticulation from P3 to P2"
# for pattern in patterns_pgN:
#     print pattern, ":", patterns_pgN1[pattern]

# print patterns_pgS
# print patterns_pgN


# Create a mapping of newicks to their probability and site pattern
# newick_to_pat_n_stat = {}
# for newick in newick_patterns:
#     for tree in trees_to_pgS:
#         if newick == tree:
#             newick_to_pat_n_stat[newick] = (newick_patterns[newick],trees_to_pgS[tree],trees_to_pgN[tree], trees_to_pgS_noO[tree], trees_to_pgN_noO[tree])
#
# results = sorted(newick_to_pat_n_stat.items(), key=lambda tup: tup[1][1], reverse=True)
# for i in results:
#     print i
#
# print
#
# trees = determine_interesting_trees(trees_to_pgS, trees_to_pgN)
# trees = list(trees)
# print trees
# print
# print newick_to_pat_n_stat[trees[1]][0] , "-" , newick_to_pat_n_stat[trees[0]][0]