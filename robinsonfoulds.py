import Bio
import BioSQL
import math
import os
from dendropy import Tree
from dendropy.calculate import treecompare


s1 = "C:\Users\chaba\GitProjects\PhyloVis\RAx_Files\RAxML_bestTree.1"
s2 = "C:\Users\chaba\GitProjects\PhyloVis\RAx_Files\RAxML_bestTree.2"

#
# def phylo_to_dendro(ref_newick, input_newick):
#     """
#
#     :param ref_newick:
#     :param input_newick:
#     :return:
#     """
#     ref = Phylo.write(bptree, ref_newick, "newick")
#     ref_tree = Tree.get(ref, "newick")
#
#     tree = Phylo.write(bptree, input_newick, "newick")
#     input_tree = Tree.write(tree)
#
#     return ref_tree, input_tree
#
#
# def foulds(ref_tree, input_tree, Weighted):
#     """
#
#     :param newick1:
#     :param newick2:
#     :param Weighted:
#     :return:
#     """
#     if Weighted == True:
#         return "W", treecompare.robinson_foulds_distance(ref_tree, input_tree,
#                                                     edge_weight_attr="length"),\
#                "U", treecompare.symmetric_difference(ref_tree, input_tree,
#                                                 is_bipartitions_updated=False)
#     else:
#         return treecompare.symmetric_difference(ref_tree, input_tree,
#                                                 is_bipartitions_updated=False)
#
# # print foulds(phylo_to_dendro(s1, s2)[0], phylo_to_dendro(s1, s2)[0], False)
#

def robinson_foulds(ref_newick, input_newick, Weighted):
    """

    :param ref_newick:
    :param input_newick:
    :param Weighted:
    :return:
    """
