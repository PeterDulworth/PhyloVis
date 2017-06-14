import os
import dendropy
from dendropy import Tree
from dendropy.calculate import treecompare



def robinson_foulds(input_newick, species_newick, Weighted):
    """
    Calculates the Robinson Foulds distances for weighted and unweighted
    trees.

    Input:
    input_newick   -- newick file or newick string containing the tree to
                      be compared to the species tree
    species_newick -- newick file containing the species tree
                      * this should not change *
    Weighted       -- boolean parameter for whether the files have weights

    Returns:
    The weighted and/or unweighted Robinson Foulds distance of the species
    tree and input tree.
    """
    # taxon names
    tns = dendropy.TaxonNamespace()

    # dendropy tree from species file
    species_tree = Tree.get_from_path(species_newick, 'newick', taxon_namespace=tns)

    # dendropy tree from input file
    if os.path.isfile(input_newick):
        input_tree = Tree.get_from_path(input_newick, 'newick', taxon_namespace=tns)

    # dendropy tree from input newick
    else:
        input_tree = Tree.get_from_string(input_newick, 'newick', taxon_namespace=tns)

    # both weighted and unweighted foulds distance
    if Weighted:
        return treecompare.weighted_robinson_foulds_distance(species_tree, input_tree), \
               treecompare.unweighted_robinson_foulds_distance(species_tree, input_tree)

    # only unweighted foulds distance
    else:
        return treecompare.unweighted_robinson_foulds_distance(species_tree, input_tree)


# s1 = '(seq8:0.00000100000050002909, ((((seq3:0.65020833412901768433,((seq7:0.00000100000050002909, ' \
#      '(seq6:0.68152455233459297013,seq1:0.00000100000050002909):1.24521798063484312458):0.58859971808264277549, ' \
#      'seq5:0.00000100000050002909):0.42899887291206934004):1.25531743587387700778,' \
#      'seq2:0.22759388849035810942):34.53877639491068407551,' \
#      'seq9:0.31954588819430751467):0.00000100000050002909,seq4:1.43351615153153244542):0.85579630090819847066,seq0:1.65212366516800979177):0.0;'
# f1 = "C:\Users\chaba\GitProjects\PhyloVis\RAx_Files\RAxML_bestTree.1"
# f2 = "C:\Users\chaba\GitProjects\PhyloVis\RAx_Files\RAxML_bestTree.2"
#
# print robinson_foulds(s1, f2, True)
# print robinson_foulds(f1, f2, True)
