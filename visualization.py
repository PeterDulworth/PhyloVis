import os
import shutil


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

    # Delete the folder and remake it
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)

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


# splittr("phylip.txt", 10, 10, "windows")
splittr("test.txt", 5, 5, "windows")