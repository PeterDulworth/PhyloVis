from Bio import Phylo

tree = Phylo.read("str.txt", "newick")
# Phylo.draw_ascii(tree)
tree.rooted = True
Phylo.draw(tree)