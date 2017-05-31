import os
import subprocess
from ete3 import Tree, TreeStyle


"""
Function for splitting PHYLIP files into smaller files based on sliding windows across the sequences
"""

def splittr(filename, window_size, step_size, destination_directory):
    """
    Creates smaller PHYLIP files based on a given window size
    Inputs:
    filename --- name of the PHYLIP file to be used
    window_size --- the number of nucleotides to include in each window
    step_size --- the number of nucleotides between the beginning of each window
    destination_directory --- the desired folder for the window files to be stored
    Output:
    Smaller "window" files showing sections of the genome in PHYLIP format
    """

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Create a list for the output files
    output_files = []

    with open(filename) as f:
        # First two line contains the number and length of the sequences respectively
        number_of_sequences = int(f.readline())
        length_of_sequences = int(f.readline())

        # Initialize a pointer for the beginning of each window
        i = 0
        # Initialize a count for the total number of windows
        BENEDICTRs_CONST = 0

        # Determine the total number of windows needed
        while(i + window_size - 1 < length_of_sequences):
            i += step_size
            BENEDICTRs_CONST += 1

        # Create a file for each window and add it to the list
        # Write the number and length of the sequences to each file
        for i in range(BENEDICTRs_CONST):
            output_files.append(open(destination_directory + "/window" + str(i + 1) + ".phylip", "w"))
            output_files[i].close()

        for i in range(BENEDICTRs_CONST):
            file = open(output_files[i].name,"a")
            file.write(str(number_of_sequences) + "\n")
            file.write(str(window_size) + "\n")
            file.close()

        # initialize l
        l = 0

        # Subsequent lines contain taxon and sequence separated by a space
        for i in range(number_of_sequences):
            line = f.readline()
            line = line.split()

            taxon = line[0]
            sequence = line[1]

            for j in range(BENEDICTRs_CONST):
                l = j * step_size
                file = open(output_files[j].name, "a")
                file.write(taxon + " ")
                window = ""
                for k in range(window_size):
                    window += sequence[l+k]


                file.write(window + "\n")
                file.close()

    return destination_directory


def RAxML_windows(window_directory):
    """
    Runs RAxML on the "windows" folder
    Inputs:
    window_directory --- name of directory that holds window files
    """

    destination_directory = "RAx_Files"

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Initialize a count to 0 to be used for file naming
    count = 0

    # Iterate over each folder in the given directory
    for filename in os.listdir(window_directory):

        count += 1

        # If file is a phylip file run RAxML on it
        if filename.endswith(".phylip"):

            input_file = os.path.join(window_directory, filename)

            # Run RAxML
            p = subprocess.Popen("raxmlHPC -f a -x12345 -p 12345 -# 2 -m GTRGAMMA -s {0} -n {1}".format(input_file, count))
            # Wait until command line is finished running
            p.wait()

            # Move RAxML output files into their own destination folder
            os.rename("RAxML_bestTree." + str(count), "RAx_Files\RAxML_bestTree." + str(count))
            os.rename("RAxML_bipartitions." + str(count), "RAx_Files\RAxML_bipartitions." + str(count))
            os.rename("RAxML_bipartitionsBranchLabels." + str(count), "RAx_Files\RAxML_bipartitionsBranchLabels." + str(count))
            os.rename("RAxML_bootstrap." + str(count), "RAx_Files\RAxML_bootstrap." + str(count))
            os.rename("RAxML_info." + str(count), "RAx_Files\RAxML_info." + str(count))

    return destination_directory


def tree_display(input_directory, destination_directory):
    """
    Creates phylogenetic tree image files for each newick string file outputted by RAxML
    Inputs:
    input_directory --- name of folder containing RAxML files
    output_directory --- name of folder to save tree images to
    """

    count = 0

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Iterate over each folder in the given directory
    for filename in os.listdir(input_directory):

        input_file = os.path.join(input_directory, filename)

        count += 1

        # If file is the file with the newick string create an image for it
        if os.path.splitext(filename)[0] == "RAxML_bestTree":

            output_name = "Tree" + os.path.splitext(filename)[1] + ".png"

            t = Tree(input_file)
            ts = TreeStyle()
            ts.rotation = 90
            ts.show_branch_length = False
            ts.show_branch_support = False
            t.render("Tree"+os.path.splitext(filename)[1]+".png", tree_style=ts)
            os.rename(output_name, os.path.join(destination_directory, output_name))

tree_display(RAxML_windows(splittr("phylip.txt", 10, 10, "windows")), "Trees")



