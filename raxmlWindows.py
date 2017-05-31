import os
import subprocess

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

