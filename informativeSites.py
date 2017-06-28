from collections import defaultdict
from natsort import natsorted
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def is_site_informative(site):
    """
    Determines if a site is informative or not
    Input:
    site --- a list of bases located at a site in the alignment 
    Output:
    1 if a site is informative 0 if a site is uninformative
    """

    # Create a mapping of bases to the number of times they occur
    base_to_counts = defaultdict(int)

    # Iterate over each base in the list site
    for base in site:

        # Add one each time a base occurs
        base_to_counts[base] += 1

    # Create a list of counts in descending order
    base_counts = sorted(base_to_counts.values(), reverse=True)

    if len(base_counts) >= 2:
        # If two different bases occur at least twice the site is informative
        if (base_counts[0] >= 2) and (base_counts[1] >= 2):
            return 1

        else:
            return 0
    else:
        return 0


def calculate_informativeness(window_directory, window_offset):
    """
    Calculates information about informative sites in an alignment
    Input:
    window_directory --- the location of the folder containing the phylip window files
    window_offset --- the offset that was used to create the windows
    Output:
    sites_to_informative --- a mapping of each site in the alignment to 1 if informative 0 if not
    windows_to_informative_count --- a mapping of each window number to the number of informative sites it has
    windows_to_informative_pct --- a mapping of each window number to the percentage of informative sites it has
    pct_informative --- the percentage of informative sites over the entire alignment
    """

    # Initialize the site index to 0
    site_idx = 0

    sites_to_informative = defaultdict(int)
    windows_to_informative_count = defaultdict(int)
    windows_to_informative_pct = {}
    total_window_size = 0

    # Iterate over each folder in the given directory in numerical order
    for filename in natsorted(os.listdir(window_directory)):

        # If file is a phylip file get the number of the window
        if filename.endswith(".phylip"):
            file_number = filename.replace("window", "")
            file_number = int(file_number.replace(".phylip", ""))

            input_file = os.path.join(window_directory, filename)

            sequence_list = []

            with open(input_file) as f:

                # Create a list of each line in the file
                lines = f.readlines()
                # line = f.readline()
                # line = line.split()

                # First line contains the number and length of the sequences
                first_line = lines[0].split()
                number_of_sequences = int(first_line[0])
                length_of_sequences = int(first_line[1])

            for line in lines[1:]:
                # Add each sequence to a list
                sequence = line.split()[1]
                sequence_list.append(sequence)

            # Iterate over the indices in each window
            for window_idx in range(length_of_sequences):

                site = []

                # Iterate over each sequence in the alignment
                for sequence in sequence_list:

                    # Add each base in a site to a list
                    site.append(sequence[window_idx])

                # Determine if a site is informative
                informative = is_site_informative(site)

                # If the site has not been visited before add to mappings (deals with overlapping windows)
                if site_idx not in sites_to_informative:
                    # If the site is informative add 1 to the mappings otherwise add 0
                    sites_to_informative[site_idx] += informative

                windows_to_informative_count[file_number] += informative

                # Increment the site index
                site_idx += 1

            # Account for overlapping windows
            site_idx += (window_offset - length_of_sequences)

            # Map windows_to_informative_count to a percentage
            windows_to_informative_pct[file_number] = windows_to_informative_count[file_number] * (100/float(length_of_sequences))

            total_window_size += length_of_sequences

    total_num_informative = sum(windows_to_informative_count.values())
    pct_informative = float(total_num_informative * 100) / total_window_size

    return sites_to_informative, windows_to_informative_count, windows_to_informative_pct, pct_informative


def line_graph_generator(dictionary, xlabel, ylabel, name):
    """
    Create a line graph based on the inputted dictionary
    Input:
    dictionary --- a dictionary mapping integers to floats or integers
    xlabel --- a string for the labeling the x-axis
    ylabel --- a string for the labeling the y-axis
    name --- a string for the image name
    Output:
    """

    x = dictionary.keys()
    y = dictionary.values()
    plt.plot(x, y, "-", )
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(name, dpi=250)
    plt.clf()


def heat_map_generator(dictionary, name):
    """
    Create a heat map based on the inputted dictionary
    Input:
    dictionary --- a dictionary mapping integers to floats or integers
    name --- a string for the image name
    """

    # Create custom color map
    colors = [(1.0, 1.0, 1.0), (1.0, 1.0, 1.0),(0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0)]
    color_name = "Chab's Colors"

    blue_green = LinearSegmentedColormap.from_list(color_name, colors)
    plt.register_cmap(cmap=blue_green)

    plt.figure(figsize=(15, 2))

    array = np.array(dictionary.values())

    x_vals = np.empty([5, array.shape[0]])

    x_vals[:, :] = array

    plt.contourf(x_vals, cmap=blue_green)
    plt.colorbar()
    plt.yticks([])

    plt.savefig(name, dpi=250)
    plt.clf()


if __name__ == '__main__':  # if we're running file directly and not importing it
    # travys window dir
    # window_dir = "C:\\Users\\travi\\Documents\\Evolutionary-Diversity-Visualization-Python\\windows"

    # peters window dir
    # window_dir = '/Users/Peter/PycharmProjects/Evolutionary-Diversity-Visualization-Python/windows'

    # chabs window dir ?
    # window_dir = ''

    sites_to_informative, windows_to_informative_count, windows_to_informative_pct, pct_informative = calculate_informativeness(window_dir, 50000)

    # print str(pct_informative) + "%"
    line_graph_generator(windows_to_informative_pct, "Windows", "Percentage of Informative Sites", "pctInformative.png")

    heat_map_generator(sites_to_informative, "HeatMapInfSites.png")