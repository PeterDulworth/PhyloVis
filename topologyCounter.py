import re
from collections import defaultdict
import os


def topology_count(directories):
    """
    Creates phylogenetic tree image files for each newick string file outputted by RAxML
    Inputs:
    directories --- a tuple containing the RAxML Files directory and the destination directory
    Output:
    topologies --- a dictionary mapping topologies to the number of times they appear
    """

    input_directory = directories[0]

    topologies = defaultdict(int)

    # Regular expression for floats
    float_pattern = "([+-]?\\d*\\.\\d+)(?![-+0-9\\.])"

    # Iterate over each folder in the given directory
    for filename in os.listdir(input_directory):

        # If file is the file with the best tree newick string create an image for it
        if os.path.splitext(filename)[0] == "RAxML_bestTree":

            input_file = os.path.join(input_directory,filename)

            with open(input_file) as f:

                # Read newick string from file
                topology = f.readline()

                # Delete float branch lengths and ":" from newick string
                topology = ((re.sub(float_pattern, '', topology)).replace(":", "")).replace("\n", "")

                topologies[topology] += 1

    return topologies

# Run example
# directories = ("C:\\Users\\travi\\Documents\\Evolutionary-Diversity-Visualization-Python\\RAx_Files","")
# print topology_count(directories)


