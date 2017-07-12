import dendropy
from dendropy import Tree
import random
from dendropy.calculate import treecompare

# (2n)!/(n+1)!*n!
# tree = "(((B:6.0,(A:5.0,C:3.0)),E:4.0):5.0,D:11.0);"
# tree = "((A,B,C),(D,E,F));"
new_topology = True

tree = "(A,B,D,E);"
tns = dendropy.TaxonNamespace()
r = random.Random()

tree = Tree.get_from_string(tree, 'newick', taxon_namespace=tns)
tree.resolve_polytomies(rng=r)
tree = tree.as_string(schema="newick").replace("\n","")
resolved = set([tree])


for i in range(10000):
    # print i
    tree = "(A,B,C,D,E);"

    # Create dendropy tree from species tree input file
    tree = Tree.get_from_string(tree, 'newick', taxon_namespace=tns)
    tree.resolve_polytomies(rng=r)

    # Iterate over the previously seen trees to determine if there is a new topology
    for seen_tree in resolved:
        seen_tree = Tree.get_from_string(seen_tree, 'newick', taxon_namespace=tns)
        rf_distance = treecompare.unweighted_robinson_foulds_distance(tree, seen_tree)
        # If the RF distance is 0 then the new tree is the same as one of the unique topologies
        if rf_distance == 0:
            new_topology = False
            break

    if new_topology:
        tree = tree.as_string(schema="newick").replace("\n","").replace("[&U] ","")
        resolved.add(tree)
        # print tree

print resolved
print len(resolved)


