import os
from natsort import natsorted
import statisticCalculations as sc
from PyQt4 import QtCore

class MsComparison(QtCore.QThread):
    def __init__(self, output_directory='RAxML_Files', parent=None):
        super(MsComparison, self).__init__(parent)
        self.output_directory = output_directory

        # create new instance of Statistics Calculations class
        self.statisticsCalculations = sc.StatisticsCalculations(output_directory=output_directory)


    def sites_to_newick_ms(self, input_file):
        """
        Creates a mapping of sites to their corresponding best tree newick string as outputted by MS
        Input:
        input_file --- an MS output file
        Output:
        sites_to_newick --- a mapping of site indices to their corresponding best tree newick string
        """

        sites_to_newick = {}

        current_site = 0

        with open(input_file) as f:
            # Create a list of each line in the file
            lines = f.readlines()

            # Iterate over each line in the file
            for line in lines:

                # If the end of the site-tree information is reached break
                if line[0] != "[":
                    break

                # Split the lines at ] to separate the integer and newick string
                line = line.split("]")

                num_sites = int(line[0].replace("[",""))
                newick = line[1].replace("\n", "")

                for i in range(num_sites):

                    sites_to_newick[current_site] = newick
                    current_site += 1


            return sites_to_newick


    def sites_to_newick_rax(self, rax_dir, window_size, window_offset):
        """
        Creates a mapping of sites to their corresponding best tree newick string as outputted by RAxML
        Input:
        rax_dir --- the directory containing RAxML output file
        window_size --- the number of bases included in each window
        window_offset --- the number of bases between the beginning of each window
        Output:
        sites_to_newick --- a mapping of site indices to their corresponding best tree newick string
        """

        sites_to_newick = {}

        current_site = 0

        # Iterate over each folder in the given directory in numerical order
        for filename in natsorted(os.listdir(rax_dir)):

            # If file is the file with the best tree newick string
            if os.path.splitext(filename)[0] == "RAxML_bestTree":

                input_file = os.path.join(rax_dir, filename)

                with open(input_file) as f:
                    # Read the newick string from the file and reformat it
                    newick = f.readline()
                    newick = newick.replace("\n","")

                for i in range(window_size):

                    sites_to_newick[current_site] = newick
                    current_site += 1

                current_site += (window_offset - window_size)


        return sites_to_newick


    def ms_rax_difference(self, sites_to_newick_1,  sites_to_newick_2):
        """
        Creates a mapping of sites to both the unweighted and weighted Robinson-Foulds Distance
        between the best tree outputted by MS and the best tree outputted by RAxML
        Input:
        sites_to_newick_ms_map --- a mapping of site indices to their corresponding best tree
        newick string
        sites_to_newick_rax_map --- a mapping of site indices to their corresponding best tree
        newick string
        Output:
        sites_to_difference_w --- a mapping of sites to the weighted RF distance between the trees
        sites_to_difference_uw --- a mapping of sites to the unweighted RF distance between the trees
        """

        # Initialize the mappings
        sites_to_difference_w = {}
        sites_to_difference_uw = {}

        # The number of total sites in the alignment is the largest site index in either dictionary + 1
        num_sites = max(max(sites_to_newick_1.keys()), max((sites_to_newick_2.keys()))) + 1

        # Iterate over each index
        for i in range(num_sites):

            # If the current site index exists in both mappings
            if (i in sites_to_newick_1) and (i in sites_to_newick_):

                # Get the respective newick strings
                newick_1 = sites_to_newick_1[i]
                newick_2 = sites_to_newick_2[i]

                # Do both the weighted and unweighted Robinson Foulds calculations
                w_rf, uw_rf = self.statisticsCalculations.calculate_robinson_foulds(newick_1, newick_2, True)

                # Map the site to those distances
                sites_to_difference_w[i] = w_rf
                sites_to_difference_uw[i] = uw_rf

        return sites_to_difference_w, sites_to_difference_uw


if __name__ == '__main__':  # if we're running file directly and not importing it
    ms = MsComparison()

    # input_file = "treefileWF1200"
    input_file = "testFiles/fakeMS.txt"
    sites_to_newick_ms_map = ms.sites_to_newick_ms(input_file)

    window_size, window_offset = 10, 10
    sites_to_newick_rax_map = ms.sites_to_newick_rax(ms.output_directory, window_size, window_offset)

    sites_to_difference_w, sites_to_difference_uw = ms.ms_rax_difference(sites_to_newick_ms_map,  sites_to_newick_rax_map)

    ms.statisticsCalculations.stat_scatter(sites_to_difference_w, "WRFdifference.png", "Difference Between MS and RAxML Output", "Sites Indices", "Weighted Robinson-Foulds Distance")
    ms.statisticsCalculations.stat_scatter(sites_to_difference_uw, "UWRFdifference.png", "Difference Between MS and RAxML Output", "Sites Indices"," Unweighted Robinson-Foulds Distance")




