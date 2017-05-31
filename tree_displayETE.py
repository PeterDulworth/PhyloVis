import os
from ete3 import Tree, TreeStyle

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

input_directory = "RAx_Files"
destination_directory = "Trees"
tree_display(input_directory, destination_directory)


