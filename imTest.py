from Bio import Phylo
from cStringIO import StringIO
import matplotlib.pyplot as plt
from PIL import Image

def topology_colorizer (color_scheme):
    """
    Create colored tree topology images based on a color scheme where
    the color of a tree is determined by the frequency that it occurs
    Inputs:
    color scheme --- a dictionary mapping newick strings to colors
    """

    # Create a count for the number of the topologies
    count = 0
    # Iterate over each newick string in color_scheme
    for newick in color_scheme:

        # Create a unique output file for each topology image
        output_file = "Topology" + str(count) + ".png"

        # Create the tree object and assign it to the appropriate color
        tree = Phylo.read(StringIO(newick), "newick")
        tree.rooted = True
        tree.root.color = color_scheme[newick]

        # Create the figure
        fig = plt.figure()
        axes = fig.add_subplot(1, 1, 1)

        # Create the tree image
        Phylo.draw(tree, output_file, axes=axes, do_show=False)

        # Rotate the image and save it
        im = Image.open(output_file)
        im.rotate(-90).save(output_file)

        count += 1

    return

# Example run
# color_scheme = {"((A,B),C);":'red',"((B,C),A);":'blue',"((C,A),B);":'yellow'}
# topology_colorizer(color_scheme)


def windows_to_newick(topologies):
    """
    Creates a dictionary of window numbers to the topology of that window if 
    the newick string contained in the window is a top topology otherwise the
    window number is mapped to "other"
    Inputs
    topologies --- a list containing the top topologies of the phylogenetic trees
    Output
    wins_to_tops --- a dictionary as described above
    """

    ###May be possible to optimize this so it doesn't have to iterate over files that aren't Topology_bestTree

    wins_to_tops = {}

    # Iterate over each folder in the given directory
    for filename in os.listdir("Rax_Files"):

        # If file is the file with the topology of the best tree newick string
        if os.path.splitext(filename)[0] == "Topology_bestTree":

            filename = os.path.join("Rax_Files", filename)

            # Open file and read newick string
            with open(filename) as f:
                # Read newick string from file
                newick = f.readline()

            window_number = (os.path.splitext(filename)[1]).replace(".","")

            # Only map windows to newick strings that are in the top topologies
            if newick in topologies:

                wins_to_tops[window_number] = newick

            else:

                wins_to_tops[window_number] = "Other"

    return wins_to_tops

# Example run
# topologies = ["((seq4,(seq7,(((seq2,(seq5,seq1)),seq9),seq3))),(seq8,seq6),seq0);","(seq5,(((seq1,((seq2,((seq6,seq3),seq4)),seq8)),seq7),seq9),seq0);"]
# print windows_to_newick(topologies)



# def plot_tree(newick, output_file):
#     """
#     Create colored tree topology images based on a color scheme where
#     the color of a tree is determined by the frequency that it occurs
#     Inputs:
#     color scheme --- a dictionary mapping newick strings to colors
#     output_file --- the name of the desired output image
#     """
#
#     tree = Phylo.read(StringIO(newick), "newick")
#     tree.rooted = True
#     tree.root.color = "#2587FF"
#     # # set the size of the figure
#     fig = plt.figure(dpi=100)
#     axes = fig.add_subplot(1, 1, 1)
#
#     Phylo.draw(tree, output_file, axes=axes, do_show=False)
#
#     return
#
# color_scheme = {"((a,b),c);":'red',"((b,c),a);":'blue',"((c,a),b);":'yellow'}
# print plot_tree(color_scheme.keys()[0],"PlzWOrk.png")


