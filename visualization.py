<<<<<<< HEAD
import math
import random
import os
=======
"""
Function for splitting PHYLIP files into smaller files based on sliding windows across the sequences
"""
>>>>>>> 42745491e7de2520e16a4b23e79021df870165d6

import os.path

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
        for i in range(BENEDICTRs_CONST):
            output_files.append(open("window" + str(i + 1) + ".phylip", "w"))

        ###
        # Above for loop can be combined with one below
        ###

        # Write the number and length of the sequences to each file
        for i in range(BENEDICTRs_CONST):
            output_files[i].write(str(number_of_sequences) + "\n")
            output_files[i].write(str(BENEDICTRs_CONST) + "\n")

        l = 0

        # Subsequent lines contain taxon and sequence separated by a space
        for i in range(number_of_sequences):
            line = f.readline()
            line = line.split()

            taxon = line[0]
            sequence = line[1]

            for j in range(BENEDICTRs_CONST):
                l = j * step_size
                output_files[j].write(taxon + " ")
                window = ""
                for k in range(window_size):
                    window += sequence[l+k]

                output_files[j].write(window + "\n")

        for i in range(len(output_files)):
            output_files[i].close()

    return None

<<<<<<< HEAD
splittr("phylip.txt", 1000, 100000, "phylip-windows")
=======
splittr("phylip.txt", 10000, 200000, "none")



>>>>>>> 42745491e7de2520e16a4b23e79021df870165d6
