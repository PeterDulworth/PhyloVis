from Bio import Phylo
from Bio.Phylo.Consensus import *
from Bio.Phylo.Consensus import _BitString

from matplotlib import pyplot as plt


# Create the figure
fig = plt.figure()
axes = fig.add_subplot(1, 1, 1)

target_tree = Phylo.read('RAxML_Files\\RAxML_bipartitions.1', "newick")
trees = list(Phylo.parse('RAxML_Files\\RAxML_bootstrap.1', 'newick'))

# support_tree = get_support(target_tree, trees)
#
# Phylo.draw(support_tree, "Test Tree", axes=axes, do_show=False)
# # Phylo.draw(target_tree, "Test Tree", axes=axes, do_show=False)
#
# plt.show()

# get clade from tree
clade = target_tree.get_nonterminals()[0]

# suppose we are provided with a tree list, the first thing
# to do is to get all the terminal names in the first tree
term_names = [term.name for term in trees[0].get_terminals()]

# for a specific clade in any of the tree, also get its terminal names
clade_term_names = [term.name for term in clade.get_terminals()]

# then create a boolean list
boolvals = [name in clade_term_names for name in term_names]

# create the string version and pass it to _BitString
bitstr = _BitString(''.join(map(str, map(int, boolvals))))






from Bio.Phylo.BaseTree import TreeMixin

target_tree = Phylo.read('RAxML_Files\\RAxML_bipartitions.0', "newick")

target_tree.root_with_outgroup("seq5")

# print target_tree.get_terminals()
# print

# Creates a list of all internal nodes
inner_nodes = target_tree.get_nonterminals()
print "loooook " + str(len(inner_nodes))
# ._repr_() displays clade information

print inner_nodes[1].__repr__()
print
print target_tree.find_any(confidence=50).__repr__()
print

print "Find elements"
interested_clades = target_tree.find_elements(confidence=0)

for clade in interested_clades:
    print clade.__repr__()
    target_tree.collapse(target=clade)

inner_nodes = target_tree.get_nonterminals()
print "loooook" + str(len(inner_nodes))

Phylo.draw(target_tree, "Test Tree", axes=axes, do_show=False)
plt.show()


# print inner_nodes



# print target_tree._filter_search(confidence>20)