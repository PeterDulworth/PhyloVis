from natsort import natsorted
from sys import platform
import subprocess
import shutil
import os
import re

"""
Functions for creating sequence windows and running RAxML
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""


def window_splitter(filename, window_size, step_size):
    """
    Creates smaller PHYLIP files based on a given window size
    
    Inputs:
    filename --- name of the PHYLIP file to be used
    window_size --- the number of nucleotides to include in each window
    step_size --- the number of nucleotides between the beginning of each window
    
    Output:
    Smaller "window" files showing sections of the genome in PHYLIP format
    """

    output_folder = "windows"

    # Delete the folder and remake it
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    os.makedirs(output_folder)

    # Create a list for the output files
    output_files = []

    with open(filename) as f:
        # First line contains the number and length of the sequences
        line = f.readline()
        line = line.split()

        number_of_sequences = int(line[0])
        length_of_sequences = int(line[1])

        # Initialize a pointer for the beginning of each window
        i = 0
        # Initialize a count for the total number of windows
        num_windows = 0

        # Determine the total number of windows needed
        while(i + window_size - 1 < length_of_sequences):
            i += step_size
            num_windows += 1

        # Create a file for each window and add it to the list
        for i in range(num_windows):
            output_files.append(open(output_folder + "/window" + str(i) + ".phylip", "w"))
            output_files[i].close()

        # Write the number and length of the sequences to each file
        for i in range(num_windows):
            file = open(output_files[i].name,"a")
            file.write(str(number_of_sequences) + "\n")
            file.write(str(window_size) + "\n")
            file.close()

        # Subsequent lines contain taxon and sequence separated by a space
        for i in range(number_of_sequences):
            line = f.readline()
            line = line.split()

            taxon = line[0]
            sequence = line[1]

            for j in range(num_windows):
                l = j * step_size
                file = open(output_files[j].name, "a")
                file.write(taxon + " ")
                window = ""
                for k in range(window_size):
                    window += sequence[l+k]


                file.write(window + "\n")
                file.close()

    return output_folder


def raxml_windows(window_directory):
    """
    Runs RAxML on files in the directory containing the windows
    
    Inputs:
    window_directory ---  the window directory location
    """

    output_directory = "RAxML_Files"

    topology_output_directory = "Topologies"

    # Delete the folder and remake it if it already exists
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    os.makedirs(output_directory)

    # Delete the folder and remake it if it already exists
    if os.path.exists(topology_output_directory):
        shutil.rmtree(topology_output_directory)

    os.makedirs(topology_output_directory)

    # Iterate over each folder in the given directory in numerical order
    for filename in natsorted(os.listdir(window_directory)):

        # If file is a phylip file run RAxML on it
        if filename.endswith(".phylip"):

            file_number = filename.replace("window","")
            file_number = file_number.replace(".phylip", "")

            input_file = os.path.join(window_directory, filename)

            # Run RAxML
            p = subprocess.Popen("raxmlHPC -f a -x12345 -p 12345 -# 2 -m GTRGAMMA -s {0} -n {1}".format(input_file, file_number), shell=True)
            # Wait until command line is finished running
            p.wait()

            # Regular expression for identifying floats
            float_pattern = "([+-]?\\d*\\.\\d+)(?![-+0-9\\.])"

            # Create a separate file with the topology of the best tree
            with open("RAxML_bestTree." + file_number) as f:
                # Read newick string from file
                topology = f.readline()

                # Delete float branch lengths, ":" and "\n" from newick string
                topology = ((re.sub(float_pattern, '', topology)).replace(":", "")).replace("\n", "")
                file = open("Topology_bestTree." + file_number, "w")
                file.write(topology)
                file.close()

            if platform == "win32":
                # Move RAxML output files into their own destination folder - Windows
                os.rename("RAxML_bestTree." + file_number, output_directory + "\RAxML_bestTree." + file_number)
                os.rename("RAxML_bipartitions." + file_number, output_directory + "\RAxML_bipartitions." + file_number)
                os.rename("RAxML_bipartitionsBranchLabels." + file_number, output_directory + "\RAxML_bipartitionsBranchLabels." + file_number)
                os.rename("RAxML_bootstrap." + file_number, output_directory + "\RAxML_bootstrap." + file_number)
                os.rename("RAxML_info." + file_number, output_directory + "\RAxML_info." + file_number)
                os.rename("topology_bestTree." + file_number, topology_output_directory + "\Topology_bestTree." + file_number)

            elif platform == "darwin":
                # Move RAxML output files into their own destination folder - Mac
                os.rename("RAxML_bestTree." + file_number, output_directory + "/RAxML_bestTree." + file_number)
                os.rename("RAxML_bipartitions." + file_number, output_directory + "/RAxML_bipartitions." + file_number)
                os.rename("RAxML_bipartitionsBranchLabels." + file_number, output_directory + "/RAxML_bipartitionsBranchLabels." + file_number)
                os.rename("RAxML_bootstrap." + file_number, output_directory + "/RAxML_bootstrap." + file_number)
                os.rename("RAxML_info." + file_number, output_directory + "/RAxML_info." + file_number)
                os.rename("topology_bestTree." + file_number, topology_output_directory + "/Topology_bestTree." + file_number)

    return



# Run commands below

if __name__ == '__main__':
    input_file = "phylip.txt"
    window_size = 10
    window_offset = 10

    windows_dir = window_splitter(input_file, window_size, window_offset)
    raxml_windows(windows_dir)