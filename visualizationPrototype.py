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
            output_files.append(open(destination_directory + "/window" + str(i) + ".phylip", "w"))
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
    Runs RAxML on the directory containing the windows
    Inputs:
    window_directory --- name of directory that holds window files
    Output:
    destination_directory --- the save location of the RAxML files
    """

    destination_directory = "RAx_Files"

    # Delete the folder and remake it
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)

    os.makedirs(destination_directory)


    # Iterate over each folder in the given directory
    for filename in os.listdir(window_directory):

        # If file is a phylip file run RAxML on it
        if filename.endswith(".phylip"):

            file_number = filename.replace("window","")

            input_file = os.path.join(window_directory, filename)

            # Run RAxML
            p = subprocess.Popen("raxmlHPC -f a -x12345 -p 12345 -# 2 -m GTRGAMMA -s {0} -n {1}".format(input_file, file_number), shell=True)
            # Wait until command line is finished running
            p.wait()


            if platform == "win32":
                # Move RAxML output files into their own destination folder Windows
                os.rename("RAxML_bestTree." + file_number, "RAx_Files\RAxML_bestTree." + file_number)
                os.rename("RAxML_bipartitions." + file_number, "RAx_Files\RAxML_bipartitions." + file_number)
                os.rename("RAxML_bipartitionsBranchLabels." + file_number, "RAx_Files\RAxML_bipartitionsBranchLabels." + file_number)
                os.rename("RAxML_bootstrap." + file_number, "RAx_Files\RAxML_bootstrap." + file_number)
                os.rename("RAxML_info." + file_number, "RAx_Files\RAxML_info." + file_number)

            elif platform == "darwin":
                # Move RAxML output files into their own destination folder Mac
                os.rename("RAxML_bestTree." + file_number, "RAx_Files/RAxML_bestTree." + file_number)
                os.rename("RAxML_bipartitions." + file_number, "RAx_Files/RAxML_bipartitions." + file_number)
                os.rename("RAxML_bipartitionsBranchLabels." + file_number, "RAx_Files/RAxML_bipartitionsBranchLabels." + file_number)
                os.rename("RAxML_bootstrap." + file_number, "RAx_Files/RAxML_bootstrap." + file_number)
                os.rename("RAxML_info." + file_number, "RAx_Files/RAxML_info." + file_number)

    return destination_directory


def tree_display(input_directory, destination_directory):
    """
    Creates phylogenetic tree image files for each newick string file outputted by RAxML
    Inputs:
    input_directory --- name of folder containing RAxML files
    output_directory --- name of folder to save tree images to
    """

    # Delete the folder and remake it
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)

    os.makedirs(destination_directory)


    # Iterate over each folder in the given directory
    for filename in os.listdir(input_directory):

        input_file = os.path.join(input_directory, filename)

        # If file is the file with the newick string create an image for it
        if os.path.splitext(os.path.splitext(filename)[0])[0] == "RAxML_bestTree":

            output_name = "Tree" + os.path.splitext(os.path.splitext(filename)[0])[1] + ".png"

            t = Tree(input_file)
            ts = TreeStyle()
            ts.rotation = 90
            ts.show_branch_length = False
            ts.show_branch_support = False
            t.render(output_name, tree_style=ts)
            os.rename(output_name, os.path.join(destination_directory, output_name))

    return destination_directory


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

    plt.savefig("Plot.png")
    return "Plot.png"


def image_combination(input_directory, plot):
    """
    Combines images from the inout directory horizontally and adds a plot vertically
    Inputs:
    input_directory --- name of directory containing tree images
    plot --- the plot to be included at the top of the image
    """

    bottom_images = []

    # Iterate over each folder in the given directory
    for filename in os.listdir(input_directory):

        input_file = os.path.join(input_directory, filename)

        # If file is a Tree image
        if os.path.splitext(os.path.splitext(filename)[0])[0] == "Tree":
            # Get the tree number
            list_idx  = int((os.path.splitext(os.path.splitext(filename)[0])[1]).replace(".",""))
            # Place the tree in the correct position in the list
            bottom_images.insert(list_idx,input_file)

    # Open the bottom images
    bottom_images = map(Image.open, bottom_images)
    top_image = Image.open(plot)

    widths, heights = zip(*(i.size for i in bottom_images))

    #Total width is either the total of the bottom widths or the width of the top
    total_width = sum(widths)

    # Scale top image properly
    ratio = float(top_image.size[1]) / top_image.size[0]
    top_image = top_image.resize((total_width, int(total_width * ratio)))

    # Total height is sum of the top image and max of the bottom
    total_height = max(heights) + top_image.size[1]

    new_im = Image.new('RGB', (total_width, total_height))

    new_im.paste(top_image, (0,0))

    x_offset = 0
    y_offset = top_image.size[1]

    #Combine bottom images horizontally with no vertical offset
    for im in bottom_images:
        new_im.paste(im, (x_offset,y_offset))
        x_offset += im.size[0]

    new_im.save('Final.jpg')

    if platform == "win32":
        # WINDOWS OPEN FILE
        os.startfile("Final.jpg")

    elif platform == "darwin":
        # MAC OPEN FILE
        os.system("open Final.jpg")

# Run command
# image_combination(tree_display(RAxML_windows(splittr("test.txt", 5, 5, "windows")), "Trees"), scatter(num_windows('windows'), ml(num_windows('windows'), 'RAx_Files')))
# image_combination(tree_display(RAxML_windows(splittr("phylip.txt", 10, 10, "windows")), "Trees"), scatter(num_windows('windows'), ml(num_windows('windows'), 'RAx_Files')))
# image_combination(tree_display(RAxML_windows(splittr("phylip.txt", 5, 5, "windows")), "Trees"), scatter(num_windows('windows'), ml(num_windows('windows'), 'RAx_Files')))



# input_file_name = "C:/Users/travi/Documents/Evolutionary-Diversity-Visualization-Python/phylip.txt"
# output_dir_name = r"C:\Users\travi\Documents\Evolutionary-Diversity-Visualization-Python\windows"
# window_size = 10
# window_offset = 10
# image_combination(tree_display(RAxML_windows(splittr(input_file_name, window_size, window_offset, output_dir_name)), "Trees"),scatter(num_windows(output_dir_name), ml(num_windows(output_dir_name), 'RAx_Files')))
