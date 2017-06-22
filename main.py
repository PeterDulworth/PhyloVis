import sip
sip.setapi('QString', 2)
import sys, os
import gui_layout as gui
import time
import RAxMLOperations as wo
from PIL import Image
from PyQt4 import QtGui, QtCore
from shutil import copyfile, copytree
from outputWindows import allTreesWindow, donutPlotWindow, scatterPlotWindow, circleGraphWindow, pgtstWindow, \
    robinsonFouldsWindow
import topologyPlots as tp
import statisticCalculations as sc


class PhyloVisApp(QtGui.QMainWindow, gui.Ui_PhylogeneticVisualization):
    def __init__(self, parent=None):
        super(PhyloVisApp, self).__init__(parent)
        self.setupUi(self)
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("cleanlooks"))

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # gui icon
        self.setWindowIcon(QtGui.QIcon('Luay.jpg'))

        # self.welcomeLogoImage.setScaledContents(True)
        self.welcomeLogoImage.setPixmap(QtGui.QPixmap('Luay.jpg'))

        # mapping from: windows --> page index
        self.windows = {'welcomePage': 0, 'inputPageRax': 1, 'inputPageNotRaxA': 2, 'inputPageNotRaxB': 3,
                        'inputPageNotRaxC': 4,
                        'outputPage': 5}

        self.windowSizes = {'welcomePage': {'x': 459, 'y': 245}, 'inputPageRax': {'x': 459, 'y': 488 + 22 + 22 + 22+ 6 + 6 + 6},
                            'inputPageNotRaxA': {'x': 459, 'y': 245}, 'inputPageNotRaxB': {'x': 459, 'y': 245},
                            'inputPageNotRaxC': {'x': 459, 'y': 245}, 'outputPage': {'x': 459, 'y': 245}}

        self.runComplete = False
        self.checkboxWeighted.setEnabled(False)
        self.menuExport.setEnabled(False)
        self.outgroupEntry.setEnabled(False)
        self.outgroupLabel.setEnabled(False)

        self.rooted = False
        self.outGroup = ""
        # self.statisticsOptionsGroupBox.hide()

        ############################# Link Events ##############################

        # **************************** Menu Bar Events ****************************#

        # when you select a mode first deselect all other modes to ensure only a single mode is ever selected
        self.modes = self.menuMode.actions()
        self.actionRax.triggered.connect(lambda: self.ensureSingleModeSelected(self.actionRax))
        self.actionNotRaxA.triggered.connect(lambda: self.ensureSingleModeSelected(self.actionNotRaxA))
        self.actionNotRaxB.triggered.connect(lambda: self.ensureSingleModeSelected(self.actionNotRaxB))
        self.actionNotRaxC.triggered.connect(lambda: self.ensureSingleModeSelected(self.actionNotRaxC))

        # change the input mode based on which mode is selected in the menu bar
        self.actionRax.triggered.connect(lambda: self.setWindow('inputPageRax'))
        self.actionNotRaxA.triggered.connect(lambda: self.setWindow('inputPageNotRaxA'))
        self.actionNotRaxB.triggered.connect(lambda: self.setWindow('inputPageNotRaxB'))
        self.actionNotRaxC.triggered.connect(lambda: self.setWindow('inputPageNotRaxC'))

        # export files
        self.actionStandardJPG.triggered.connect(lambda: self.exportFile('Final.jpg'))
        self.actionBootstrapJPG.triggered.connect(lambda: self.exportFile('FinalBootstraps.jpg'))
        self.actionTextFile.triggered.connect(lambda: self.exportFile('FinalBootstraps.jpg'))

        # export directories
        self.actionWindowsDirectory.triggered.connect(lambda: self.exportDirectory('windows'))
        self.actionRAXDirectory.triggered.connect(lambda: self.exportDirectory('RAxML_Files'))
        self.actionTreesDirectory.triggered.connect(lambda: self.exportDirectory('Trees'))

        # set up other windows
        self.allTreesWindow = allTreesWindow.AllTreesWindow()
        self.scatterPlotWindow = scatterPlotWindow.ScatterPlotWindow()
        self.circleGraphWindow = circleGraphWindow.CircleGraphWindow()
        self.donutPlotWindow = donutPlotWindow.DonutPlotWindow()
        self.pgtstWindow = pgtstWindow.PGTSTWindow()
        self.robinsonFouldsWindow = robinsonFouldsWindow.RobinsonFouldsWindow()

        self.checkboxCircleGraph.stateChanged.connect(
            lambda: self.updatedDisplayWindows(btnClicked=self.checkboxCircleGraph))
        self.checkboxScatterPlot.stateChanged.connect(
            lambda: self.updatedDisplayWindows(btnClicked=self.checkboxScatterPlot))
        self.checkboxAllTrees.stateChanged.connect(lambda: self.updatedDisplayWindows(btnClicked=self.checkboxAllTrees))
        self.checkboxDonutPlot.stateChanged.connect(
            lambda: self.updatedDisplayWindows(btnClicked=self.checkboxDonutPlot))

        # **************************** Rax Input Page Events ****************************#

        # resize to size of welcome page
        self.resize(self.windowSizes['welcomePage']['x'], self.windowSizes['welcomePage']['y'])

        # if input file button is clicked run function -- file_open
        self.inputFileBtn.clicked.connect(lambda: self.openFile(self.inputFileEntry))
        self.actionOpen.triggered.connect(lambda: self.openFile(self.inputFileEntry))

        # set start page to the input page
        self.stackedWidget.setCurrentIndex(0)

        # run
        self.runBtn.clicked.connect(self.run)
        self.progressBar.reset()

        # disable export menu initially
        self.menuExport.setEnabled(False)

        self.newickFileBtn.clicked.connect(lambda: self.openFile(self.newickFileEntry))

        # **************************** Rax Welcome Page Events ****************************#

        self.raxBtn.clicked.connect(lambda: self.setWindow('inputPageRax'))
        self.notRax1Btn.clicked.connect(lambda: self.setWindow('inputPageNotRaxA'))
        self.notRax2Btn.clicked.connect(lambda: self.setWindow('inputPageNotRaxB'))
        self.notRax3Btn.clicked.connect(lambda: self.setWindow('inputPageNotRaxC'))

        self.raxBtn.clicked.connect(lambda: self.ensureSingleModeSelected(self.actionRax))
        self.notRax1Btn.clicked.connect(lambda: self.ensureSingleModeSelected(self.actionNotRaxA))
        self.notRax2Btn.clicked.connect(lambda: self.ensureSingleModeSelected(self.actionNotRaxB))
        self.notRax3Btn.clicked.connect(lambda: self.ensureSingleModeSelected(self.actionNotRaxC))

        self.checkboxStatistics.stateChanged.connect(lambda: self.toggleEnabled(self.statisticsOptionsGroupBox))
        self.checkboxRobinsonFoulds.clicked.connect(lambda: self.toggleEnabled(self.checkboxWeighted))
        self.checkboxRooted.stateChanged.connect(lambda: self.toggleEnabled(self.outgroupEntry))
        self.checkboxRooted.stateChanged.connect(lambda: self.toggleEnabled(self.outgroupLabel))

    ################################# Handlers #################################

    def displayResults(self, displayTree=False):
        if displayTree:
            self.setWindow('outputPage')
            self.outputTabs.setCurrentIndex(0)
            standardSize = Image.open("Final.png").size
            self.resize(int(standardSize[0]), int(standardSize[1]))
            self.standardImage.setScaledContents(True)
            self.standardImage.setPixmap(QtGui.QPixmap("Final.png"))
            self.bootstrapImage.setScaledContents(True)
            self.bootstrapImage.setPixmap(QtGui.QPixmap("FinalBootstraps.png"))

        if self.checkboxAllTrees.isChecked():
            self.allTreesWindow.show()
            self.allTreesWindow.display_image()

        if self.checkboxCircleGraph.isChecked():
            self.circleGraphWindow.show()
            self.circleGraphWindow.display_image()

        if self.checkboxDonutPlot.isChecked():
            self.donutPlotWindow.show()
            self.donutPlotWindow.display_image()

        if self.checkboxScatterPlot.isChecked():
            self.scatterPlotWindow.show()
            self.scatterPlotWindow.display_image()

        if self.checkboxStatistics.isChecked():
            if self.checkboxRobinsonFoulds.isChecked():
                if self.checkboxWeighted.isChecked():
                    self.robinsonFouldsWindow.show()
                    self.robinsonFouldsWindow.displayWeightedAndUnweightedImages()
                else:
                    self.robinsonFouldsWindow.show()
                    self.robinsonFouldsWindow.displayUnweightedImage()
            if self.checkboxProbability.isChecked():
                self.pgtstWindow.show()
                self.pgtstWindow.display_image()

    def toggleStatisticsOptionsDisplay(self):
        if self.statisticsOptionsGroupBox.isVisible():
            self.statisticsOptionsGroupBox.hide()
            self.resize(435, 245 + 22 + 22)
        else:
            self.statisticsOptionsGroupBox.show()
            self.resize(435, 488 + 22 + 22)
        print self.inputPage.size()

    def toggleEnabled(self, object):
        enabled = object.isEnabled()
        object.setEnabled(not enabled)

    def getNumberChecked(self):
        """
        returns the number of checkboxes that are checked
        """
        return (self.checkboxScatterPlot.checkState() + self.checkboxCircleGraph.checkState() + self.checkboxDonutPlot.checkState() + self.checkboxAllTrees.checkState()) / 2

    def updatedDisplayWindows(self, btnClicked=None):

        if btnClicked == None or btnClicked.isChecked():
            if self.runComplete == True:
                if self.getNumberChecked() > 0:
                    # User inputs:
                    num = self.topTopologies

                    # Function calls for plotting inputs:
                    topologies_to_counts, unique_topologies_to_newicks = tp.topology_counter(rooted=self.rooted,outgroup=self.outGroup)
                    if num > len(topologies_to_counts):
                        num = len(topologies_to_counts)
                    list_of_top_counts, labels, sizes = tp.top_freqs(num, topologies_to_counts)
                    top_topologies_to_counts = tp.top_topologies(num, topologies_to_counts)
                    windows_to_top_topologies, top_topologies_list = tp.windows_to_newick(
                        top_topologies_to_counts,unique_topologies_to_newicks, rooted=self.rooted,outgroup=self.outGroup)  # all trees, scatter, circle, donut
                    topologies_to_colors, scatter_colors, ylist = tp.topology_colors(windows_to_top_topologies,
                                                                                     top_topologies_list)  # scatter, circle, (donut?)

                if self.checkboxDonutPlot.isChecked():
                    donut_colors = tp.donut_colors(top_topologies_to_counts, topologies_to_colors)  # donut

                    tp.topology_donut(labels, sizes, donut_colors)  # donut

                if self.checkboxScatterPlot.isChecked():
                 tp.topology_scatter(windows_to_top_topologies, scatter_colors, ylist)  # scatter

                if self.checkboxAllTrees.isChecked():
                 tp.topology_colorizer(topologies_to_colors)  # all trees

                if self.checkboxCircleGraph.isChecked():
                    tp.generateCircleGraph(self.input_file_name, windows_to_top_topologies,
                                                             topologies_to_colors, self.window_size, self.window_offset)

                if self.checkboxStatistics.isChecked():
                    if self.robinsonFoulds:
                        if self.weighted:
                            windows_to_w_rf, windows_to_uw_rf = sc.calculate_windows_to_rf(self.speciesTree,
                                                                                           self.weighted)
                            sc.stat_scatter(windows_to_w_rf, "weightedRF")
                            sc.stat_scatter(windows_to_uw_rf, "unweightedRF")

                        else:
                            windows_to_uw_rf = sc.calculate_windows_to_rf(self.speciesTree, self.weighted)
                            sc.stat_scatter(windows_to_uw_rf, "unweightedRF")

                    if self.pgtst:
                        # Function calls for calculating statistics
                        windows_to_p_gtst = sc.calculate_windows_to_p_gtst(self.speciesTree)
                        sc.stat_scatter(windows_to_p_gtst, "PGTST")
                self.displayResults()

    def setWindow(self, window):
        self.stackedWidget.setCurrentIndex(self.windows[window])
        self.resize(self.windowSizes[window]['x'], self.windowSizes[window]['y'])

    def ensureSingleModeSelected(self, mode_selected):
        for mode in self.modes:
            if mode != mode_selected:
                mode.setChecked(False)

        mode_selected.setChecked(True)

    def setProgressBarVal(self, val):
        self.progressBar.setValue(val)

    def exportFile(self, fileName):
        extension = os.path.splitext(fileName)[1]
        name = QtGui.QFileDialog.getSaveFileName(self, 'Export ' + extension[1:]) + extension
        copyfile(fileName, name)

    def exportDirectory(self, dirName):
        name = QtGui.QFileDialog.getExistingDirectory(self, 'Export ' + dirName + ' Directory') + '/' + dirName
        print dirName, name
        copytree(dirName, name)

    def openFile(self, textEntry):
        # get name of file
        name = QtGui.QFileDialog.getOpenFileName()
        # set name of file to text entry
        textEntry.setText(name)

    def runProgressBar(self):
        self.completed = 0
        self.progressBar.reset()

        while True:
            time.sleep(0.05)
            value = self.progressBar.value() + 1
            self.progressBar.setValue(value)
            QtGui.qApp.processEvents()
            if value >= 101:
                break

    def run(self):

        # Error handling for input file
        try:
            self.input_file_name = str(self.inputFileEntry.text())
            self.input_file_extension = os.path.splitext(self.input_file_name)[1]

            if self.input_file_name == "":
                raise ValueError, (1, "Please choose a file")
            elif self.input_file_extension != '.txt' and self.input_file_extension != '.phylip' and self.input_file_extension != '.fasta':
                raise ValueError, (
                    2, "Luay does not approve of your filetype.\nPlease enter either a .txt, .fasta, or .phylip file")
        except ValueError, (ErrorNumber, ErrorMessage):
            QtGui.QMessageBox.about(self, "Invalid Input", str(ErrorMessage))
            return

        # Error handling for number of top topologies
        try:
            self.topTopologies = int(self.numberOfTopTopologiesEntry.text())
            if self.topTopologies <= 0 or self.topTopologies > 15:
                raise ValueError, "Please enter an integer between 0 and 15."
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input",
                                    "Number of top topologies needs to be an integer between 0 and 15.")
            return

        # Error handling for window size
        try:
            self.window_size = int(self.windowSizeEntry.text())
            if self.window_size <= 0:
                raise ValueError, "Positive integers only"
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Window size needs to be a positive integer.")
            return

        # Error handling for window offset
        try:
            self.window_offset = int(self.windowOffsetEntry.text())
            if self.window_offset <= 0:
                raise ValueError, "Positive integers only"
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Window offset needs to be a positive integer.")
            return

        # Error handling for newick file
        try:
            if self.checkboxStatistics.isChecked():
                self.newickFileName = str(self.newickFileEntry.text())
                self.newickFileExtension = os.path.splitext(self.newickFileName)[1]
                self.newickStringFromEntry = str(self.speciesTreeNewickStringsEntry.text())

                if self.newickFileName == "" and self.newickStringFromEntry == "":
                    raise ValueError, (1, "Please choose a file or enter a newick string")
                elif self.newickFileName != "" and self.newickStringFromEntry != "":
                    raise ValueError, (2, "You have chosen a file and entered a newick string. Please choose one.")

                # get checkbox values
                self.robinsonFoulds = self.checkboxRobinsonFoulds.isChecked()
                self.weighted = self.checkboxWeighted.isChecked()
                self.pgtst = self.checkboxProbability.isChecked()

                # if the newick input is from the file chooser
                if self.newickFileName != '':
                    with open(self.newickFileEntry.text(), 'r') as f:
                        self.speciesTree = f.read().replace('\n', '')
                # else if the newick input is from the manual text entry
                elif self.newickStringFromEntry != '':
                    self.speciesTree = str(self.speciesTreeNewickStringsEntry.text())

        except ValueError, (ErrorNumber, ErrorMessage):
            QtGui.QMessageBox.about(self, "Invalid Input", str(ErrorMessage))
            return

        try:
            if self.checkboxRooted.isChecked():
                self.outGroup = str(self.outgroupEntry.text())
                self.rooted = self.checkboxRooted.isChecked()
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Invalid Input")
            return

        # self.runProgressBar()

        try:
            self.windows_dirs = wo.window_splitter(self.input_file_name, self.window_size,
                                           self.window_offset)  # run once - not rerun
            wo.raxml_windows(self.windows_dirs)  # run once - not rerun
        except IndexError:
            QtGui.QMessageBox.about(self, "asd", "Invalid file format.\nPlease check your data.")
            return

        #####################################################################

        self.runComplete = True
        self.updatedDisplayWindows()
        self.menuExport.setEnabled(True)


if __name__ == '__main__':  # if we're running file directly and not importing it
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication

    # initialize main input window
    form = PhyloVisApp()  # We set the form to be our PhyloVisApp (design)
    form.show()  # Show the form

    sys.exit(app.exec_())  # and execute the app
