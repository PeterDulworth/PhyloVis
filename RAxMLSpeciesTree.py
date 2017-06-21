from natsort import natsorted
from sys import platform
import subprocess
import shutil
import os
import re


def raxml_species_tree(phylip):
    """
    Runs RAxML on input PHYLIP file to create a species
    tree.

    Inputs:
    phylip -- a file inputted by the user.

    Returns:
    A species tree folder.
    """
    # Create output directory
    output_directory = "RAxML_SpeciesTree"

    # Delete the folder and remake it if it already exists
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    os.makedirs(output_directory)

    # Run RAxML
    p = subprocess.Popen(
        "raxmlHPC -f a -x12345 -p 12345 -# 2 -m GTRGAMMA -s {0} -n txt".format(phylip),
        shell=True)
    # Wait until command line is finished running
    p.wait()

    # Regular expression for identifying floats
    float_pattern = "([+-]?\\d*\\.\\d+)(?![-+0-9\\.])"

    # Create a separate file with the topology of the best tree
    with open("RAxML_bestTree.txt") as f:
        # Read newick string from file
        topology = f.readline()

        # Delete float branch lengths, ":" and "\n" from newick string
        topology = ((re.sub(float_pattern, '', topology)).replace(":", "")).replace("\n", "")
        file = open("Topology_bestTree.txt", "w")
        file.write(topology)
        file.close()

    if platform == "win32":
        # Move RAxML output files into their own destination folder - Windows
        os.rename("RAxML_bestTree.txt", output_directory + "\RAxML_ST_bestTree.txt")
        os.rename("RAxML_bipartitions.txt", output_directory + "\RAxML_ST_bipartitions.txt")
        os.rename("RAxML_bipartitionsBranchLabels.txt",
                  output_directory + "\RAxML_ST_bipartitionsBranchLabels.txt")
        os.rename("RAxML_bootstrap.txt", output_directory + "\RAxML_ST_bootstrap.txt")
        os.rename("RAxML_info.txt", output_directory + "\RAxML_ST_info.txt")
        os.rename("topology_bestTree.txt", output_directory + "\Topology_ST_bestTree.txt")

    elif platform == "darwin":
        # Move RAxML output files into their own destination folder - Mac
        os.rename("RAxML_bestTree.txt", output_directory + "/RAxML_ST_bestTree.txt")
        os.rename("RAxML_bipartitions.txt", output_directory + "/RAxML_ST_bipartitions.txt")
        os.rename("RAxML_bipartitionsBranchLabels.txt",
                  output_directory + "/RAxML_ST_bipartitionsBranchLabels.txt")
        os.rename("RAxML_bootstrap.txt", output_directory + "/RAxML_ST_bootstrap.txt")
        os.rename("RAxML_info.txt", output_directory + "/RAxML_ST_info.txt")
        os.rename("topology_bestTree.txt", output_directory + "/Topology_ST_bestTree.txt")

phy = "C:\Users\chaba\GitProjects\PhyloVis\phylip.txt"
raxml_species_tree(phy)