import os
from ete3 import Tree, TreeStyle
from PIL import Image

def windows_to_topologies(destination_directory):
    """
    Maps the name of each window to the newick string representing the topology of the RAxML best tree
    Inputs:
    destination_directory --- the folder containing all other outputted folders
    Output:
    window_topologies --- a dictionary mapping windows to newick strings
    """

    topologies = set([])

    windows_topologies = {}

    rax_dir = os.path.join(destination_directory, "RAx_Files")

    # Iterate over each folder in the given directory
    for filename in os.listdir(rax_dir):

        # If file is the file with the best tree newick string create an image for it
        if os.path.splitext(filename)[0] == "Topology_bestTree":
            input_file = os.path.join(rax_dir, filename)

            with open(input_file) as f:
                # Read newick string from file
                topology = f.readline()
                f.close()

                topologies.add(topology)

    topologies = list(topologies)

    for each
    return windows_topologies