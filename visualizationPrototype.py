import os
import subprocess
from ete3 import Tree, TreeStyle
import math
import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib import pyplot as plt
import matplotlib.colors as colors
from PIL import Image
import shutil
from sys import platform
import re

"""
Functions for creating a visualization tool for the summary and analysis 
of phylogenetic trees.
"""

def splittr(filename, window_size, step_size):
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
            output_files.append(open(output_folder + "/window" + str(i) + ".phylip", "w"))
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

    return output_folder


def raxml_windows(window_directory):
    """
    Runs RAxML on the directory containing the windows
    Inputs:
    window_directory ---  the window directory location
    Output:
    output_directory --- the save location of the RAxML files
    """

    output_directory = "RAx_Files"

    topology_output_directory = "Topologies"

    # Delete the folder and remake it
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    os.makedirs(output_directory)

    # Delete the folder and remake it
    if os.path.exists(topology_output_directory):
        shutil.rmtree(topology_output_directory)

    os.makedirs(topology_output_directory)


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

    return output_directory


def tree_display(input_directory):
    """
    Creates phylogenetic tree image files for each newick string file outputted by RAxML
    Inputs:
    input_directory--- thee RAxML Files directory
    Output:
    output_directory --- name of folder containing tree images
    """

    output_directory = "Trees"

    # Delete the folder and remake it
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    os.makedirs(output_directory)

    # Iterate over each folder in the given directory
    for filename in os.listdir(input_directory):

        input_file = os.path.join(input_directory, filename)

        # If file is the file with the best tree newick string create an image for it
        if os.path.splitext(filename)[0] == "RAxML_bestTree":

            # Create tree image
            output_name = "Tree" + os.path.splitext(filename)[1] + ".png"

            t = Tree(input_file)
            ts = TreeStyle()
            ts.rotation = 90
            ts.show_branch_length = False
            ts.show_branch_support = False
            t.render(output_name, tree_style=ts)
            os.rename(output_name, os.path.join(output_directory, output_name))

        # If file is the file with the best tree newick string create an image for it
        if os.path.splitext(os.path.splitext(filename)[0])[0] == "RAxML_bipartitions":

            # Create tree image with bootstrapping
            output_name = "TreeBootstraps" + os.path.splitext(filename)[1] + ".png"

            t = Tree(input_file)
            ts = TreeStyle()
            ts.rotation = 90
            ts.show_branch_length = False
            ts.show_branch_support = True
            t.render(output_name, tree_style=ts)
            os.rename(output_name, os.path.join(output_directory, output_name))

    return output_directory


def num_windows(directory):
    """
    Counts the number of windows created
    for use in x-axis of the scatter plot.

    Input:
    directory -- folder containing window files

    Returns:
    A count of the number of window files.
    """
    num = 0

    for filename in os.listdir(directory):
        if filename.endswith('.phylip'):
            num += 1

    return num


def ml(num, directory):
    """
    Reads info file to find Final ML Optimization
    Likelihood for use in y-axis of the scatter plot.

    Input:
    num       -- count outputted by num_windows
    directory -- RAxML folder containing info files

    Returns:
    The Likelihood number.
    """
    likelihood = []

    while len(likelihood) <= num:
        for filename in os.listdir(directory):
            if os.path.splitext(os.path.splitext(filename)[0])[0] == "RAxML_info":
                with open(os.path.join(directory, filename), 'r') as raxmlFile:
                    info = raxmlFile.readlines()
                    for line in info:
                        words = line.split()
                        for i in range(len(words)):
                            if words[i] == 'Final':
                                likelihood.append(float(words[i + 4]))

    return likelihood


def scatter(num, likelihood):
    """
    Creates a scatter plot for use in the
    visualization tool.

    Input:
    num        -- count outputted by num_windows
    likelihood -- number outputted by ml

    Returns:
    A scatter plot with num as the x-axis and
    likelihood as the y-axis.
    """
    area = math.pi * (5)**2

    for i in range(1, num + 1):
        x = i
        y = float(likelihood[i]) / 100

        # changes color for different ranges
        if y <= 0.25:
            color = colors.hex2color('#0000FF')
        elif y > 0.25 and y <= 0.50:
            color = colors.hex2color('#00CC00')
        elif y > 0.50 and y <= 0.75:
            color = colors.hex2color('#FFFF00')
        elif y > 0.75 and y <= 1:
            color = colors.hex2color('#FF0000')

        plt.scatter(x, y, s = area, c = color, alpha = 1)

    plot = "Plot.png"
    plt.savefig(plot)
    return plot


def image_combination(input_directory, plot):
    """
    Combines images from the inout directory horizontally and adds a plot vertically
    Inputs:
    input_directory --- name of directory containing tree images
    plot --- the plot to be included at the top of the image
    """

    tree_images = []
    tree_bootstrap_images = []

    # Iterate over each folder in the given directory
    for filename in os.listdir(input_directory):

        input_file = os.path.join(input_directory, filename)

        # If file is a Tree image
        if os.path.splitext(os.path.splitext(filename)[0])[0] == "Tree":
            # Get the tree number
            list_idx  = int(os.path.splitext(os.path.splitext(filename)[0])[1].replace(".",""))
            # Place the tree in the correct position in the list
            tree_images.insert(list_idx,input_file)

        # File is a tree imagee with bootstrapping
        else:
            # Get the tree number
            list_idx = int(os.path.splitext(os.path.splitext(filename)[0])[1].replace(".",""))
            # Place the tree in the correct position in the list
            tree_bootstrap_images.insert(list_idx, input_file)

    # Open the bottom images
    tree_images = map(Image.open, tree_images)
    tree_bootstrap_images = map(Image.open, tree_bootstrap_images)
    top_image = Image.open(plot)

    widths, heights = zip(*(i.size for i in tree_images))

    #Total width is either the total of the bottom widths or the width of the top
    total_width = sum(widths)

    # Scale top image properly
    ratio = float(top_image.size[1]) / top_image.size[0]
    top_image = top_image.resize((total_width, int(total_width * ratio)))

    # Total height is sum of the top image and max of the bottom
    total_height = max(heights) + top_image.size[1]

    # Create combined image of plot and trees
    new_im = Image.new('RGB', (total_width, total_height))

    new_im.paste(top_image, (0,0))

    x_offset = 0
    y_offset = top_image.size[1]

    #Combine bottom images horizontally with no vertical offset
    for im in tree_images:
        new_im.paste(im, (x_offset,y_offset))
        x_offset += im.size[0]

    final_image = 'Final.jpg'
    new_im.save(final_image)

    # Create combined image of plot and bootstrapped trees
    new_im = Image.new('RGB', (total_width, total_height))

    new_im.paste(top_image, (0, 0))

    x_offset = 0
    y_offset = top_image.size[1]

    # Combine bottom images horizontally with no vertical offset
    for im in tree_bootstrap_images:
        new_im.paste(im, (x_offset, y_offset))
        x_offset += im.size[0]

    final_bootstrap_image =  'FinalBootstraps.jpg'
    new_im.save(final_bootstrap_image)

    # Automatically open image files
    # if platform == "win32":
    #     # WINDOWS OPEN FILE
    #     os.startfile(final_image)
    #     os.startfile(final_bootstrap_image)
    #
    # elif platform == "darwin":
    #     # MAC OPEN FILE
    #     os.system("open " + final_image)
    #     os.system("open " + final_bootstrap_image)


# Run commands below

if __name__ == '__main__':
    input_file = "phylip.txt"
    window_size = 10
    window_offset = 10

    windows_dirs = splittr(input_file, window_size, window_offset)
    RAx_dirs = raxml_windows(windows_dirs)
    Tree_dir = tree_display(RAx_dirs)
    num = num_windows(windows_dirs)
    likelihood = ml(num, RAx_dirs)
    plot = scatter(num, likelihood)
    image_combination(Tree_dir,plot)