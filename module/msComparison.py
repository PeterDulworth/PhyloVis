import os
from natsort import natsorted
import statisticCalculations as sc
from PyQt4 import QtCore

"""
Functions:
    __init__(self, output_directory='RAxML_Files', parent=None)
    sites_to_newick_ms(self, input_file)
    sites_to_newick_rax(self, rax_dir, window_size, window_offset)
    sitesToRobinsonFouldsDistance(self, sites_to_newick_1,  sites_to_newick_2)
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

class MsComparison(QtCore.QThread):
    def __init__(self, msToRax=True, output_directory='RAxML_Files', parent=None):
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

    def sitesToRobinsonFouldsDistance(self, sites_to_newick_1,  sites_to_newick_2):
        """
            Creates a mapping of sites to both the unweighted and weighted Robinson-Foulds Distance
            between the best tree outputted by MS and the best tree outputted by RAxML

            Input:
                sites_to_newick_ms_map --- a mapping of site indices to their corresponding best tree newick string
                sites_to_newick_rax_map --- a mapping of site indices to their corresponding best tree newick string

            Output:
                sites_to_difference_w --- a mapping of sites to the weighted RF distance between the trees
                sites_to_difference_uw --- a mapping of sites to the unweighted RF distance between the trees
        """

        # Initialize the mappings
        sites_to_difference_w = {}
        sites_to_difference_uw = {}

        # The number of total sites in the alignment is the largest site index in either dictionary + 1
        num_sites = max(max(sites_to_newick_1.keys()), max((sites_to_newick_2.keys()))) + 1

        # initialize percentComplete
        percentComplete = 0

        # Iterate over each index
        for i in range(num_sites):

            percentComplete += (1.0 / float(num_sites)) * 100

            # If the current site index exists in both mappings
            if (i in sites_to_newick_1) and (i in sites_to_newick_2):

                # Get the respective newick strings
                newick_1 = sites_to_newick_1[i]
                newick_2 = sites_to_newick_2[i]

                # Do both the weighted and unweighted Robinson Foulds calculations
                w_rf, uw_rf = self.statisticsCalculations.calculate_robinson_foulds(newick_1, newick_2, True)

                # Map the site to those distances
                sites_to_difference_w[i] = w_rf
                sites_to_difference_uw[i] = uw_rf

            self.emit(QtCore.SIGNAL('MS_PER'), percentComplete)

        return sites_to_difference_w, sites_to_difference_uw

    def run(self):
        graphLabels = []
        sitesToNewickMsMaps = []
        weightedRobinsonFouldsSums = []
        unweightedRobinsonFouldsSums = []
        percentMatchingSitesWeighted = []
        percentMatchingSitesUnweighted = []

        # create sites to newick map for MS truth file
        sitesToNewickMsTruth = self.sites_to_newick_ms(self.msTruth)

        # create sites to newick map for each MS file
        for msFile in self.msFiles:
            sitesToNewickMsMaps.append(self.sites_to_newick_ms(msFile))
            graphLabels.append(os.path.basename(msFile))

        for sitesToNewickMsMap in sitesToNewickMsMaps:
            sitesToRFDWeighted, sitesToRFDUnweighted = self.sitesToRobinsonFouldsDistance(sitesToNewickMsTruth, sitesToNewickMsMap)

            # total robinson foulds distances
            weightedRobinsonFouldsSums.append(sum(sitesToRFDWeighted.values()))
            unweightedRobinsonFouldsSums.append(sum(sitesToRFDUnweighted.values()))

            matchingSites = 0
            for site in sitesToRFDWeighted:
                if sitesToRFDWeighted[site] == 0:
                    matchingSites += 1.0
            percentMatchingSitesWeighted.append(100.0 * matchingSites / len(sitesToRFDWeighted))

            matchingSites = 0
            for site in sitesToRFDUnweighted:
                if sitesToRFDUnweighted[site] == 0:
                    matchingSites += 1.0
            percentMatchingSitesUnweighted.append(100.0 * matchingSites / len(sitesToRFDUnweighted))



        # sites_to_difference_w, sites_to_difference_uw = self.sitesToRobinsonFouldsDistance(sitesToNewickMsTruth, sitesToNewickMsMaps[0])

        self.emit(QtCore.SIGNAL('MS_COMPLETE'), weightedRobinsonFouldsSums, unweightedRobinsonFouldsSums, percentMatchingSitesWeighted, percentMatchingSitesUnweighted,  graphLabels)

if __name__ == '__main__':  # if we're running file directly and not importing it

    ms = MsComparison()
    ms.statisticsCalculations.output_directory = '../RAxML_Files'

    ms.msTruth = '../testFiles/fakeMS.txt'
    ms.msFiles = []
    ms.msFiles.append('../testFiles/fakeMS2.txt')
    ms.msFiles.append('../testFiles/fakeMS5.txt')
    ms.msFiles.append('../testFiles/fakeMS6.txt')

    def plot(weightedData, unweightedData, percentMatchingSitesWeighted, percentMatchingSitesUnweighted, msFiles):
        # ms.statisticsCalculations.barPlot(weightedData, '../plots/WRFdifference.png', 'Weighted', '', 'IDK', groupLabels=msFiles, xTicks=True)
        # ms.statisticsCalculations.barPlot(unweightedData, '../plots/UWRFdifference.png', 'Unweighted', '', 'IDK', groupLabels=msFiles)
        ms.statisticsCalculations.barPlot(percentMatchingSitesWeighted, '../plots/percentMatchingSitesWeighted', 'Percent Matching Sites Weighted', '', '% Matching Sites Weighted')
        ms.statisticsCalculations.barPlot(percentMatchingSitesUnweighted, '../plots/percentMatchingSitesUnweighted', 'Percent Matching Sites Unweighted', '', '% Matching Sites Unweighted')
        # ms.statisticsCalculations.plt.show()

    ms.connect(ms, QtCore.SIGNAL('MS_COMPLETE'), plot)
    ms.run()



    # for sitesToNewickMsMap in sitesToNewickMsMaps:
    #     weightedData, unweightedData = ms.sitesToRobinsonFouldsDistance(sitesToNewickMsTruth, sitesToNewickMsMap)

        # ms.statisticsCalculations.barPlot(weightedData.values(), 'name', 'title', 'x', '% Accuracy')
        # ms.statisticsCalculations.stat_scatter(weightedData, "../plots/WRFdifference.png", "Difference Between MS-1 and MS-2", "Sites Indices", "Weighted Robinson-Foulds Distance")
        # ms.statisticsCalculations.stat_scatter(unweightedData, "../plots/UWRFdifference.png", "Difference Between MS-1 and MS-2", "Sites Indices", "Unweighted Robinson-Foulds Distance")
