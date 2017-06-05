import re
import os
from sys import platform
import shutil
import subprocess

def raxml_windows(directories):
    """
    Runs RAxML on the directory containing the windows
    Inputs:
    directories --- a tuple containing the window directory and the destination directory
    Output:
    output_directory --- the save location of the RAxML files
    destination directory --- the folder containing the output directory
    """

    window_directory = directories[0]
    destination_directory = directories[1]

    output_directory = os.path.join(destination_directory,"RAx_Files")

    # Delete the folder and remake it
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    os.makedirs(output_directory)


    # Iterate over each folder in the given directory
    for filename in os.listdir(window_directory):

        # If file is a phylip file run RAxML on it
        if filename.endswith(".phylip"):

            file_number = filename.replace("window","")
            file_number = file_number.replace(".phylip", "")

            input_file = os.path.join(window_directory, filename)

            # Run RAxML
            p = subprocess.Popen("raxmlHPC -f a -x12345 -p 12345 -# 2 -m GTRGAMMA -s {0} -n {1}".format(input_file, file_number), shell=True)
            # Wait until command line is finished running
            p.wait()

            # Regular expression for floats
            float_pattern = "([+-]?\\d*\\.\\d+)(?![-+0-9\\.])"

            # Create a separate file with the topology of the best tree
            with open("RAxML_bestTree." + file_number) as f:
                # Read newick string from file
                topology = f.readline()

                # Delete float branch lengths and ":" from newick string
                topology = ((re.sub(float_pattern, '', topology)).replace(":", "")).replace("\n", "")
                file = open("Topology_bestTree." + file_number, "w")
                file.write(topology)
                file.close()

            if platform == "win32":
                # Move RAxML output files into their own destination folder Windows
                os.rename("RAxML_bestTree." + file_number, output_directory + "\RAxML_bestTree." + file_number)
                os.rename("RAxML_bipartitions." + file_number, output_directory + "\RAxML_bipartitions." + file_number)
                os.rename("RAxML_bipartitionsBranchLabels." + file_number, output_directory + "\RAxML_bipartitionsBranchLabels." + file_number)
                os.rename("RAxML_bootstrap." + file_number, output_directory + "\RAxML_bootstrap." + file_number)
                os.rename("RAxML_info." + file_number, output_directory + "\RAxML_info." + file_number)
                os.rename("topology_bestTree." + file_number, output_directory + "\Topology_bestTree." + file_number)

            elif platform == "darwin":
                # Move RAxML output files into their own destination folder Mac
                os.rename("RAxML_bestTree." + file_number, output_directory + "/RAxML_bestTree." + file_number)
                os.rename("RAxML_bipartitions." + file_number, output_directory + "/RAxML_bipartitions." + file_number)
                os.rename("RAxML_bipartitionsBranchLabels." + file_number, output_directory + "/RAxML_bipartitionsBranchLabels." + file_number)
                os.rename("RAxML_bootstrap." + file_number, output_directory + "/RAxML_bootstrap." + file_number)
                os.rename("RAxML_info." + file_number, output_directory + "/RAxML_info." + file_number)
                os.rename("topology_bestTree." + file_number, output_directory + "/topology_bestTree." + file_number)

    return output_directory, destination_directory

directories = ("C:\\Users\\travi\\Documents\\Evolutionary-Diversity-Visualization-Python\\windows","C:\\Users\\travi\\Documents\\Evolutionary-Diversity-Visualization-Python")
raxml_windows(directories)