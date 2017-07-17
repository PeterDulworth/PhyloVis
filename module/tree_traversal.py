import ete3
import copy

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

        inverted_pattern = []

        # Iterate over each site in the pattern
        for site in pattern:

            if site == "A":
                inverted_pattern.append("B")

            elif site == "B":
                inverted_pattern.append("A")

        # Change the last site to an "A"
        inverted_pattern[-1] = "A"
        inverted.append(inverted_pattern)

    return inverted


def site_pattern_generator(taxa_order, newick):
    """
    Generate the appropriate AB list patterns
    Inputs:
    taxa_order --- the desired order of the taxa
    newick --- the newick string to generate site patterns for
    Output:
    finished_patterns --- the list of site patterns generated for the newick string
    """

    # Create a tree object
    tree = ete3.Tree(newick, format=1)

    # Determine the outgroup of the tree
    outgroup = taxa_order[-1]

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
    for node in tree.traverse("postorder"):
        # Add node name to list of nodes
        nodes.append(node.name)

    # Keep track of visited leaves
    seen_leaves = []

    nodes = list(reversed(nodes))
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
        for node_idx in range(end_idx+1,len(nodes)):

            # If the last clade is reached break
            if node_idx == len(nodes) -3:
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
    for pattern_idx in range(len(final_site_patterns)-idx_offset):
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
        pattern_str = ""
        pattern = finished_patterns.pop()
        for site in pattern:
            pattern_str += site
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

    newicks_to_patterns = {}

    # Iterate over the newick strings
    for newick in newicks:

        newicks_to_patterns[newick] = site_pattern_generator(taxa_order,newicks)

    return newicks_to_patterns



# taxa = ["P1", "P2", "P3", "P4","P5","P6", "O"]
# newick = "((((P1,P2),(P3,P4)),(P5,P6)),O);"
# newick = "((((((P1,P2),P3),P4),P5),P6),O);"
# taxa = ["P1", "P2", "P3", "P4", "O"]
# newick = "(((P1,P2),(P3,P4)),O);"
# # newick = "((((P1,P2),P3),P4),O);"
# # taxa = ["P1", "P2", "P3", "O"]
# # newick = "(((P1,P2),P3),O);"

print newicks_to_patterns_generator(taxa, newicks)















# # taxa = ["P1","P2","P3","P4","O"]
# taxa = ["P1","P2","P3","P4","O"]
# # taxa = ["O","B","C","G","H"]
# outgroup = "O"
# newick = "(((P1,P2),(P3,P4)),O);"
# # # newick = "(((P2,P3),(P1,P4)),O);" # BAABA,ABBAA
# # # newick = "(((P2,P3),P1),O);"
# # newick = '(O,(B,(C,(G,H))));'
# # # newick = "((((G,H),C),B),O);"
# # # newick = "((O,(P1,P2)),(P3,P4));"
# # # newicks = ["(((P1,P2),P3),O);","(((P2,P3),P1),O);","(((P1,P3),P2),O);"]
# newicks = [newick]
# print site_pattern_generator(taxa, outgroup, newicks)




# taxa = ["1","2","3","4","5","O"]
# outgroup = "O"
# newick = "((((1,2),(3,4)),5),O);"
# newicks = [newick]
# print site_pattern_generator(taxa, outgroup, newicks)






# pattern_dict = {}
#     for newick in newicks:
#
#         nodes = []
#         site_pattern = []
#
#         # Create a tree object
#         t = ete3.Tree(newick, format=1)
#
#         for node in t.traverse("postorder"):
#             # Do some analysis on node
#             nodes.append(node.name)
#         print nodes
#         p = ""
#         for i in range(len(taxa)):
#             p += "A"
#
#         pattern = "B"
#
#         for node_idx in range((len(nodes)-2),-1,-1):
#
#             if nodes[node_idx] != "" and nodes[node_idx+1] != "":
#                 node1 = nodes[node_idx + 1]
#                 node2 = nodes[node_idx]
#
#                 pat_idx1 = taxa.index(node1)
#                 pat_idx2 = taxa.index(node2)
#
#                 p = p[:pat_idx1] + pattern + p[pat_idx1+1:]
#                 p = p[:pat_idx2] + pattern + p[pat_idx2+1:]
#
#                 pattern = "A"
#
#         pattern_dict[newick] = p
#
#     return pattern_dict

