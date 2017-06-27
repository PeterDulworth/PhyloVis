from Bio import Phylo
from matplotlib import pyplot as plt
from natsort import natsorted
import os
from PyQt4 import QtCore

"""
Functions for creating sequence windows and running RAxML.
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

class BootstrapContraction(QtCore.QThread):
    def __init__(self, parent=None):
        super(BootstrapContraction, self).__init__(parent)

    def contraction_threshold(self, tree_file, confidence_threshold):
        """
        Contract the inner nodes of a tree if the confidence values of the
        inner nodes are less than a specified threshold value

        Inputs:
        tree_file --- a string containing the file name of a bootstrapped tree newick string
        confidence_threshold --- an integer value for the lowest confidence value allowed for
        an internal node; nodes with confidence values less than this will be contracted
        Outputs:
        num_internal_nodes_i --- the number of internal nodes in the tree before contraction
        num_internal_nodes_f --- the number of internal nodes in the tree after contraction
        """

        # Create a plot for the figure
        fig = plt.figure()
        axes = fig.add_subplot(1, 1, 1)

        tree = Phylo.read(tree_file, "newick")

        # Outgroup is meant just for "phylip.txt" testing
        # tree.root_with_outgroup("seq5")

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

        # plt.title('Confidence Threshold: ' + str(confidence_threshold))
        Phylo.draw(tree, "TestTree", axes=axes, do_show=False)
        plt.clf()
        # plt.show()

        return num_internal_nodes_i, num_internal_nodes_f


    def internal_nodes_after_contraction(self, confidence_threshold):
        """
        Contract the inner nodes of each bootstrapped tree from RAxML and create
        lists for the number internal nodes before and after contraction

        Inputs:
        confidence_threshold --- an integer value for the lowest confidence value allowed for
        an internal node; nodes with confidence values less than this will be contracted
        Outputs:
        internal_nodes_i --- a list of the number of internal nodes in the tree before contraction
        internal_nodes_f --- a list of the number of internal nodes in the tree after contraction
        """

        internal_nodes_i = []
        internal_nodes_f = []

        # Iterate over each folder in the given directory
        for filename in natsorted(os.listdir("RAxML_Files")):

            # If file is the file with the topology of the best tree newick string
            if os.path.splitext(filename)[0] == "RAxML_bipartitions":
                filename = os.path.join("RAxML_Files", filename)

                # Get the number of internal nodes before and after contraction
                num_internal_nodes_i, num_internal_nodes_f = self.contraction_threshold(filename, confidence_threshold)

                internal_nodes_i.append(num_internal_nodes_i)
                internal_nodes_f.append(num_internal_nodes_f)

        return internal_nodes_i, internal_nodes_f


    def double_line_graph_generator(self, list1, list2, xlabel, ylabel, name, confidence_threshold):
        """
        Create a line graph based on the inputted dictionary
        Input:
        list1 --- a list of integers
        list2 --- a list of integers of equal length to list1
        xlabel --- a string for the labeling the x-axis
        ylabel --- a string for the labeling the y-axis
        name --- a string for the image name
        Output:
        """

        x = range(len(list1))

        plt.plot(x, list1, "-", )
        plt.plot(x, list2, "-", )
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title('Number of Internal Nodes Confidence Threshold: ' + str(confidence_threshold))
        plt.legend(["Before Contraction", "After Contraction"], loc=0)
        # plt.tight_layout()
        # plt.show()
        plt.savefig(name, dpi=250)
        plt.clf()


if __name__ == '__main__':  # if we're running file directly and not importing it

    bc = BootstrapContraction()

    # tree_file = 'RAxML_Files\\RAxML_bipartitions.0'
    confidence_threshold = 60
    # print contraction_threshold(tree_file, confidence_threshold)

    internal_nodes_i, internal_nodes_f = bc.internal_nodes_after_contraction(confidence_threshold)
    xlabel = "Window Indices"
    ylabel = "Number of Internal Nodes"
    name = "ContractedGraph.png"

    bc.double_line_graph_generator(internal_nodes_i, internal_nodes_f, xlabel, ylabel, name, confidence_threshold)
