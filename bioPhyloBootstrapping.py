from Bio import Phylo
from matplotlib import pyplot as plt



def contraction_threshold(tree_file, confidence_threshold):
    """
    Contract the inner nodes of a tree if the confidence values of the 
    inner nodes are less than a specified threshold value
    
    Inputs:
    tree_file --- a string containing the file name of a bootstrapped tree newick string
    confidence_threshold --- an integer value for the lowest confidence value allowed for 
    an internal node; nodes with confidence values less than this will be contracted
    """

    # Create a plot for the figure
    fig = plt.figure()
    axes = fig.add_subplot(1, 1, 1)

    tree = Phylo.read(tree_file, "newick")

    # Outgroup is meant just for "phylip.txt" testing
    tree.root_with_outgroup("seq5")

    # Creates a list of all internal nodes
    internal_nodes = tree.get_nonterminals()

    # Get the number of internal nodes initially
    num_internal_nodes_i = len(internal_nodes)

    for clade in internal_nodes:

        # If the clade has a confidence value less than the threshold contract it
        if clade.confidence < confidence_threshold and clade.confidence:

            # Print clad information for debugging
            # print clade.__repr__()

            tree.collapse(target=clade)

    # Get the final number of internal nodes
    num_internal_nodes_f = len(tree.get_nonterminals())

    plt.title('Confidence Threshold: ' + str(confidence_threshold))
    Phylo.draw(tree, "Test Tree", axes=axes, do_show=False)
    plt.show()

    return num_internal_nodes_i, num_internal_nodes_f

tree_file = 'RAxML_Files\\RAxML_bipartitions.0'
confidence_threshold = 100

print contraction_threshold(tree_file, confidence_threshold)