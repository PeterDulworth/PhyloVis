from ete3 import Tree

taxa = "[P1,P2,P3,P4,O]"
newick = "(((P1,P2),(P3,P4)),O);"

# we load a tree
t = Tree(newick, format=1)

for node in t.traverse("postorder"):
  # Do some analysis on node
  print node.name