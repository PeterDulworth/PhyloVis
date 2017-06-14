import subprocess
import os

def calculate_p_of_gt_given_st(species_tree, gene_tree):
    """
    Computes the probability that a gene tree occurs given a species tree. If the taxon names between the two trees are not the
    same then the probability returned is 0.0. If trees are the exact same then probability is 1.0
    Inputs:
    species_tree --- a newick string containing a species tree with branch lengths as outputted by RAxML or inputted by user
    gene_tree --- a newick string containing a gene tree with branch lengths as outputted by RAxML run on windows
    Output:
    p_of_gt_given_st --- the probability that a gene tree occurs given a species tree
    """

    # If species_tree input is a file read in the newick string
    if os.path.isfile(species_tree):
        with open(species_tree) as f:
            species_tree = f.readline()
        print "st", species_tree

        # Check if the species tree is formatted correctly for PhyloNet if not reformat it
        if species_tree[-2] != ")" or species_tree[-1] != ")":
            species_tree = newick_reformat(species_tree)

    # If gene_tree input is a file read in the newick string
    if os.path.isfile(gene_tree):
        with open(gene_tree) as f:
            gene_tree = f.readline()
        print "gt", gene_tree
        print

        # Check if the gene tree is formatted correctly for PhyloNet if not reformat it
        if gene_tree[-2] != ")" or gene_tree[-1] != ")":
            gene_tree = newick_reformat(gene_tree)

    print "st", species_tree
    print "gt", gene_tree

    # Run PhyloNet jar file
    p = subprocess.Popen("java -jar ./pstgt.jar {0} {1}".format(species_tree, gene_tree), stdout=subprocess.PIPE, shell=True)

    # Read output and convert to float
    p_of_gt_given_st = float(p.stdout.readline())

    return p_of_gt_given_st

def newick_reformat(newick):
    """
    Reformat the inputted newick string to work with the PhyloNet jar file
    "(a:2.5,(b:1.0,c:1.0):1.5)" This format works
    "(a:2.0,(b:1.0,c:1.0):1.0);" This format works
    "(a:2.0,(b:1.0,c:1.0)):1.0;" THIS FORMAT DOES NOT WORK --- trees from RAxML are in this format
    Inputs:
    newick --- an incorrectly formatted newick string
    Output:
    newick --- a correctly formatted newick string
    """

    # Find the last occurrence of ")"
    last_idx = newick.rfind(")")

    # If newick string ends in ";" like in the RAxMl output files move ")" to before ";"
    if newick.rfind(";") == len(newick)-1:
        newick = newick[:last_idx] + newick[last_idx + 1:]
        newick = newick[:-1] + ")" + newick[-1:]

    # Else move ")" to before end of string
    else:
        newick = newick[:last_idx] + newick[last_idx + 1:]
        newick = newick + ")"

    return newick


# Original command
# "java -jar ./pstgt.jar (a:2.0,(b:1.0,c:1.0):1.0) (a:2.5,(b:1.0,c:1.0):1.5)"

# "(a:2.5,(b:1.0,c:1.0):1.5)" This format works
# "(a:2.0,(b:1.0,c:1.0):1.0);" This format works
# "(a:2.0,(b:1.0,c:1.0)):1.0;" THIS FORMAT DOES NOT WORK --- trees from RAxML are in this format