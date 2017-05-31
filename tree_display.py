from Bio import Phylo

def displayr(newick_file):
    tree = Phylo.read(newick_file, "newick")
    Phylo.draw_ascii(tree)
    tree.rooted = True
    Phylo.draw(tree)

displayr("newick.txt")