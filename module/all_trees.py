import re
import dendropy
from dendropy import Tree
import copy
from dendropy.calculate import treecompare
import itertools
import math
from collections import defaultdict
from Bio import Phylo
from cStringIO import StringIO
from ete3 import Tree


def calculate_num_trees(n):
    """
    Calculate the number of unique topologies on n taxa
    Input:
    n --- the number of taxa
    Output:
    num_trees --- the number of trees
    """

    numerator = math.factorial((2 * n - 5))
    denominator = math.factorial((n - 3)) * 2 ** (n - 3)
    num_trees = numerator / denominator

    return num_trees


def gendistinct(n):
    """
    Generate all full binary trees with n leaves
    Input:
    n --- the number of leaves
    Output:
    dp[-1] --- the set of all full binary trees with n nodes
    """

    leafnode = '(.)'
    dp = []
    newset = set()
    newset.add(leafnode)
    dp.append(newset)

    for i in range(1, n):
        newset = set()
        for j in range(i):
            for leftchild in dp[j]:
                for rightchild in dp[i - j - 1]:
                    newset.add('(' + '.' + leftchild + rightchild + ')')
        dp.append(newset)

    # newdpbish = []
    #
    # for i in dp[-1]:
    #     i = i.replace(')(', '),(')
    #     i = i.replace('(.)','*')
    #     i = i.replace('.','')
    #     newdpbish.append(i)
    #
    # return newdpbish
    #
    return dp[-1]

print gendistinct(4)
print len(gendistinct(4))


def generate_all_trees(taxa):
    """
    Create all trees given a set of taxa
    Inputs:
    taxa --- a set of the taxa to be used for leaf names
    Output:
    trees --- the set of all trees over the taxa
    """

    # Regex pattern for identifying leaves next to a clade in newick string
    pattern = "([\)][a-zA-Z0-9_.-])"

    # Generate all distinct binary trees
    trees = gendistinct(len(taxa))

    # Get all possible permutations of the taxa
    taxa_orders = itertools.permutations(taxa)
    taxa_orders = list(taxa_orders)


    all_trees = []

    # Iterate over each tree in the set
    for tree in trees:
        # print 'tree', tree
        # Reformat the tree
        tree = tree.replace('.', '')

        # Iterate over each permutation of taxa
        for taxa_perm in taxa_orders:
            # print 'perm', taxa_perm

            # Create a copy of the tree
            bi_tree = tree

            # replace the leaves with taxons and reformat string
            for i in range(len(taxa_perm)):
                taxon = taxa_perm[i] + ","
                bi_tree = bi_tree.replace("()", taxon, 1)

            bi_tree = bi_tree.replace(",)", ")")

            # Find all instances of a ")" followed by a taxon and add a "," between
            clades = re.findall(pattern, bi_tree)
            for clade in clades:
                taxon = clade[1]
                bi_tree = bi_tree.replace(clade, ")," + taxon)
            bi_tree = bi_tree.replace(")(", "),(")
            bi_tree = bi_tree + ";"
            all_trees.append(bi_tree)

            # print bi_tree

    return all_trees

# generate_all_trees(['A','B','C','O'])

def generate_unique_trees(taxa, outgroup):
    # Create a set for unique trees
    unique_trees = set([])

    unique_newicks = set([])

    all_trees = generate_all_trees(taxa)

    # t1 = Tree('(((a,b),c), ((e, f), g));')
    # t2 = Tree('(((a,b),c), ((e, f), g));')
    # # rf, max_rf, common_leaves, parts_t1, parts_t2 = \
    # print type(t1)
    # print t1.robinson_foulds(t2)[0]

    # Iterate over each tree in all_trees
    for tree in all_trees:

        tree = Tree(tree)
        tree.set_outgroup(outgroup)

        is_unique = True

        # Iterate the unique trees for comparison
        for unique_tree in unique_trees:

            # unique_tree = Tree(unique_tree)
            # unique_tree.set_outgroup(outgroup)

            # Compute robinson-foulds distance
            rf_distance = tree.robinson_foulds(unique_tree)[0]

            # If rf distance is 0 the tree is not unique
            if rf_distance == 0:
                is_unique = False

        if is_unique:
            unique_trees.add(tree)

    for tree in unique_trees:
        unique_newicks.add(tree.write())

    return unique_newicks


taxa = ["H", "C", "O", "P", "X","B",'D']
outgroup = "O"
n = len(taxa)
print calculate_num_trees(n), "Actual"
# print gendistinct(n)
all = generate_all_trees(taxa)
# print all
print len(all), "All"
unique = generate_unique_trees(taxa, outgroup)
print len(unique), "Unique"
print unique

