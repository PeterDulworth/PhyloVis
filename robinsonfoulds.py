from Bio import Phylo
import BioSQL
import math
import os
from dendropy import Tree
from dendropy.calculate import treecompare


f1 = "C:\Users\chaba\GitProjects\PhyloVis\RAx_Files\RAxML_bestTree.1"
f2 = "C:\Users\chaba\GitProjects\PhyloVis\RAx_Files\RAxML_bestTree.2"
f3 = "C:\Users\chaba\GitProjects\PhyloVis\RAx_Files\RAxML_bestTree.3"

s1 = '(A, (B, C), (D, E))'
s2 = '((A, B), C, D), E)'
s3 = '(A, B, ((C, D), E))'


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

def robinson_foulds(input_newick, species_newick, Weighted):
    """

    :param input_newick:
    :param species_tree:
    :param gene_tree:
    :param Weighted:
    :return:
    """
    if os.path.isfile(input_newick):
        input_tree = Tree.get_from_path(input_newick, 'newick')

    else:
        input_tree = Tree.get_from_string

    species_tree = Tree.get_from_path(species_newick, 'newick')

    if Weighted:
        return "weighted: ", treecompare.weighted_robinson_foulds_distance(species_tree, input_tree), \
               "unweighted: ", treecompare.unweighted_robinson_foulds_distance(species_tree, input_tree)

    else:
        return "unweighted: ", treecompare.unweighted_robinson_foulds_distance(species_tree, input_tree)


print robinson_foulds(f1, f2, False)
print robinson_foulds(s1, f2, False)