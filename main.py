import sip
sip.setapi('QString', 2)
import sys, os
import gui_layout as gui
import RAxMLOperations as ro
from PIL import Image
from PyQt4 import QtGui, QtCore
from shutil import copyfile, copytree
from outputWindows import allTreesWindow, donutPlotWindow, scatterPlotWindow, circleGraphWindow, pgtstWindow, \
    robinsonFouldsWindow, heatMapWindow
import topologyPlots as tp
import statisticCalculations as sc
import fileConverterController as fcc
import informativeSites as infSites
import tetris, snake


class PhyloVisApp(QtGui.QMainWindow, gui.Ui_PhylogeneticVisualization):
    def __init__(self, parent=None):
        super(PhyloVisApp, self).__init__(parent)
        self.setupUi(self)

        # set UI style
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("cleanlooks"))

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # gui icon
        self.setWindowIcon(QtGui.QIcon('Luay.jpg'))

        # self.welcomeLogoImage.setScaledContents(True)
        self.welcomeLogoImage.setPixmap(QtGui.QPixmap('Luay.jpg'))

        self.input_file_name = self.window_size = self.window_offset = None
        self.raxmlOperations = ro.RAxMLOperations(self.input_file_name, self.window_size, self.window_offset)
        self.connect(self.raxmlOperations, QtCore.SIGNAL('RAX_PER'), self.updateProgressBar)

        # mapping from: windows --> page index
        self.windows = {'welcomePage': 0, 'inputPageRax': 1, 'inputPageFileConverter': 2, 'inputPageNotRaxB': 3, 'inputPageNotRaxC': 4, 'outputPage': 5}
        # mapping from: windows --> dictionary of page dimensions
        self.windowSizes = {'welcomePage': {'x': 459, 'y': 245}, 'inputPageRax': {'x': 459, 'y': 488 + 22 + 22 + 22 + 6 + 6 + 6 + 30}, 'inputPageFileConverter': {'x': 459, 'y': 245 + 40}, 'inputPageNotRaxB': {'x': 459, 'y': 245}, 'inputPageNotRaxC': {'x': 459, 'y': 245}, 'outputPage': {'x': 459, 'y': 245}}
        # mapping from: mode --> page
        self.comboboxModes_to_windowNames = {'RAx_ML': 'inputPageRax', 'File Converter': 'inputPageFileConverter', 'not rax B': 'inputPageNotRaxB', 'not rax C': 'inputPageNotRaxC'}
        # mapping from: mode --> menu action
        self.comboboxModes_to_actionModes = {'RAx_ML': self.actionRax, 'File Converter': self.actionConverter, 'not rax B': self.actionNotRaxB, 'not rax C': self.actionNotRaxC}

        # initialize window
        self.allTreesWindow = allTreesWindow.AllTreesWindow()
        self.scatterPlotWindow = scatterPlotWindow.ScatterPlotWindow()
        self.circleGraphWindow = circleGraphWindow.CircleGraphWindow()
        self.donutPlotWindow = donutPlotWindow.DonutPlotWindow()
        self.pgtstWindow = pgtstWindow.PGTSTWindow()
        self.robinsonFouldsWindow = robinsonFouldsWindow.RobinsonFouldsWindow()
        self.heatMapWindow = heatMapWindow.HeatMapWindow()

        # default values
        self.runComplete = False
        self.checkboxWeighted.setEnabled(False)
        self.menuExport.setEnabled(False)
        self.outgroupEntry.setEnabled(False)
        self.outgroupLabel.setEnabled(False)
        self.progressBar.reset()
        self.rooted = False
        self.outGroup = ""
        self.stackedWidget.setCurrentIndex(0)
        self.resize(self.windowSizes['welcomePage']['x'], self.windowSizes['welcomePage']['y'])

        # **************************** RAXML PAGE ****************************#

        # selecting a mode in the menu bar -> deselects all other modes first
        # change the input mode based on which mode is selected in the menu bar
        self.actionRax.triggered.connect(lambda: self.ensureSingleModeSelected(self.actionRax))
        self.actionRax.triggered.connect(lambda: self.setWindow('inputPageRax'))
        self.actionConverter.triggered.connect(lambda: self.ensureSingleModeSelected(self.actionConverter))
        self.actionConverter.triggered.connect(lambda: self.setWindow('inputPageFileConverter'))
        self.actionNotRaxB.triggered.connect(lambda: self.ensureSingleModeSelected(self.actionNotRaxB))
        self.actionNotRaxB.triggered.connect(lambda: self.setWindow('inputPageNotRaxB'))
        self.actionNotRaxC.triggered.connect(lambda: self.ensureSingleModeSelected(self.actionNotRaxC))
        self.actionNotRaxC.triggered.connect(lambda: self.setWindow('inputPageNotRaxC'))

        # triggers export dialogs
        self.actionStandardJPG.triggered.connect(lambda: self.exportFile('Final.jpg'))
        self.actionBootstrapJPG.triggered.connect(lambda: self.exportFile('FinalBootstraps.jpg'))
        self.actionTextFile.triggered.connect(lambda: self.exportFile('FinalBootstraps.jpg'))
        self.actionWindowsDirectory.triggered.connect(lambda: self.exportDirectory('windows'))
        self.actionRAXDirectory.triggered.connect(lambda: self.exportDirectory('RAxML_Files'))
        self.actionTreesDirectory.triggered.connect(lambda: self.exportDirectory('Trees'))

        # triggers select file dialogs
        self.inputFileBtn.clicked.connect(lambda: self.openFile(self.inputFileEntry))
        self.actionOpen.triggered.connect(lambda: self.openFile(self.inputFileEntry))
        self.newickFileBtn.clicked.connect(lambda: self.openFile(self.newickFileEntry))

        # regenerates each graph every time checkbox is checked
        self.checkboxCircleGraph.stateChanged.connect(lambda: self.updatedDisplayWindows(btnClicked=self.checkboxCircleGraph))
        self.checkboxScatterPlot.stateChanged.connect(lambda: self.updatedDisplayWindows(btnClicked=self.checkboxScatterPlot))
        self.checkboxAllTrees.stateChanged.connect(lambda: self.updatedDisplayWindows(btnClicked=self.checkboxAllTrees))
        self.checkboxDonutPlot.stateChanged.connect(lambda: self.updatedDisplayWindows(btnClicked=self.checkboxDonutPlot))
        self.checkboxHeatMap.stateChanged.connect(lambda: self.updatedDisplayWindows(btnClicked=self.checkboxHeatMap))

        # toggle what inputs are actionable based on checkboxes
        self.checkboxStatistics.stateChanged.connect(lambda: self.toggleEnabled(self.statisticsOptionsGroupBox))
        self.checkboxRobinsonFoulds.clicked.connect(lambda: self.toggleEnabled(self.checkboxWeighted))
        self.checkboxRooted.stateChanged.connect(lambda: self.toggleEnabled(self.outgroupEntry))
        self.checkboxRooted.stateChanged.connect(lambda: self.toggleEnabled(self.outgroupLabel))

        # run RAX_ML and generate graphs
        self.runBtn.clicked.connect(self.run)

        # **************************** WELCOME PAGE ****************************#

        self.launchBtn.clicked.connect(lambda: self.initializeMode())

        # **************************** CONVERTER PAGE ****************************#

        self.fileConverterBtn.clicked.connect(lambda: self.openFile(self.fileConverterEntry))
        self.runFileConverterBtn.clicked.connect(lambda: self.convertFile())

    ################################# Handlers #################################

    def updateProgressBar(self, val):
        self.progressBar.setValue(self.progressBar.value() + val)

    def runProgressBar(self):
        self.raxmlOperations.start()

    def initializeMode(self):
        if self.modeComboBox.currentText() != "Tetris" and self.modeComboBox.currentText() != "Snake":
            self.setWindow(self.comboboxModes_to_windowNames[self.modeComboBox.currentText()])
            self.ensureSingleModeSelected(self.comboboxModes_to_actionModes[self.modeComboBox.currentText()])
        else:
            if self.modeComboBox.currentText() == "Tetris":
                self.tetrisWindow = tetris.Tetris()
                self.tetrisWindow.show()
            if self.modeComboBox.currentText() == "Snake":
                self.snakeWindow = snake.Snake()
                self.snakeWindow.show()

    def convertFile(self):
        try:
            self.fileToBeConverted = str(self.fileConverterEntry.text())

            if self.fileToBeConverted == "":
                raise ValueError, (1, "Please choose a file")
        except ValueError, (ErrorNumber, ErrorMessage):
            QtGui.QMessageBox.about(self, "Invalid Input", str(ErrorMessage))
            return

        outputDir = os.path.splitext(self.fileToBeConverted)[0] + '.phylip-sequential.txt'
        try:
            fcc.file_converter(self.fileToBeConverted, self.inputFormatComboBox.currentText().lower(), 'phylip-sequential', outputDir)
        except IOError:
            QtGui.QMessageBox.about(self, "Invalid Input", "File does not exist.")
            return
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Inputted file type does not match selected file type.")
            return
        QtGui.QMessageBox.about(self, "File Converted", "Your file has been converted. It lives at " + str(os.path.splitext(self.fileToBeConverted)[0]))

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

        if self.checkboxHeatMap.isChecked():
            self.heatMapWindow.show()
            self.heatMapWindow.display_image()

        if self.checkboxStatistics.isChecked():
            if self.checkboxRobinsonFoulds.isChecked():
                if self.checkboxWeighted.isChecked():
                    self.robinsonFouldsWindow.show()
                    self.robinsonFouldsWindow.displayWeightedAndUnweightedImages()
                else:
                    self.robinsonFouldsWindow.show()
                    self.robinsonFouldsWindow.displayUnweightedImage()
            if self.checkboxPGTST.isChecked():
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
        return (self.checkboxHeatMap.checkState() + self.checkboxScatterPlot.checkState() + self.checkboxCircleGraph.checkState() + self.checkboxDonutPlot.checkState() + self.checkboxAllTrees.checkState()) / 2

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
                    topologies_to_colors, scatter_colors, ylist = tp.topology_colors(windows_to_top_topologies,top_topologies_list)  # scatter, circle, (donut?)

                if self.checkboxDonutPlot.isChecked():
                    donut_colors = tp.donut_colors(top_topologies_to_counts, topologies_to_colors)  # donut
                    tp.topology_donut(labels, sizes, donut_colors)  # donut

                if self.checkboxScatterPlot.isChecked():
                    tp.topology_scatter(windows_to_top_topologies, scatter_colors, ylist)  # scatter

                if self.checkboxCircleGraph.isChecked():
                    sites_to_informative, windows_to_informative_count, windows_to_informative_pct, pct_informative = infSites.calculate_informativeness('windows', self.window_offset)
                    # sites_to_informative = {0: 1, 1: 0, 2: 0, 3: 1, 4: 1, 5: 0, 6: 1, 7: 1, 8: 0, 9: 1, 10: 1, 11: 1,
                    #                         12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1,
                    #                         23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1,
                    #                         34: 1, 35: 1, 36: 1, 37: 1, 38: 1, 39: 1, 40: 1, 41: 1, 42: 1, 43: 1, 44: 1,
                    #                         45: 1, 46: 1, 47: 1, 48: 1, 49: 1, 50: 1, 51: 1, 52: 1, 53: 1, 54: 1, 55: 1,
                    #                         56: 1, 57: 1, 58: 1, 59: 1, 60: 1, 61: 1, 62: 1, 63: 1, 64: 1, 65: 1, 66: 1,
                    #                         67: 1, 68: 1, 69: 1, 70: 1, 71: 1, 72: 1, 73: 1, 74: 1, 75: 1, 76: 1, 77: 1,
                    #                         78: 1, 79: 1, 80: 1, 81: 1, 82: 1, 83: 1, 84: 1, 85: 1, 86: 1, 87: 1, 88: 1,
                    #                         89: 1, 90: 1, 91: 1, 92: 1, 93: 1, 94: 1, 95: 0, 96: 1, 97: 1, 98: 1, 99: 1}
                    tp.generateCircleGraph(self.input_file_name, windows_to_top_topologies, topologies_to_colors, self.window_size, self.window_offset, sites_to_informative)

                if self.checkboxHeatMap.isChecked():
                    sites_to_informative, windows_to_informative_count, windows_to_informative_pct, pct_informative = infSites.calculate_informativeness('windows', self.window_offset)
                    infSites.heat_map_generator(sites_to_informative, "HeatMapInfSites.png")

                if self.checkboxStatistics.isChecked():
                    if self.checkboxRobinsonFoulds.isChecked():
                        if self.checkboxWeighted.isChecked():
                            windows_to_w_rf, windows_to_uw_rf = sc.calculate_windows_to_rf(self.speciesTree, self.checkboxWeighted.isChecked())
                            sc.stat_scatter(windows_to_w_rf, "weightedRF")
                            sc.stat_scatter(windows_to_uw_rf, "unweightedRF")

                        else:
                            windows_to_uw_rf = sc.calculate_windows_to_rf(self.speciesTree, self.checkboxWeighted.isChecked())
                            sc.stat_scatter(windows_to_uw_rf, "unweightedRF")

                    if self.checkboxPGTST.isChecked():
                        # Function calls for calculating statistics
                        windows_to_p_gtst = sc.calculate_windows_to_p_gtst(self.speciesTree)
                        sc.stat_scatter(windows_to_p_gtst, "PGTST")

                if self.checkboxAllTrees.isChecked():
                    tp.topology_colorizer(topologies_to_colors, rooted=self.rooted,outgroup=self.outGroup)  # all trees

                self.displayResults()

    def setWindow(self, window):
        self.stackedWidget.setCurrentIndex(self.windows[window])
        self.resize(self.windowSizes[window]['x'], self.windowSizes[window]['y'])

    def ensureSingleModeSelected(self, mode_selected):
        for mode in self.menuMode.actions():
            if mode != mode_selected:
                mode.setChecked(False)

        mode_selected.setChecked(True)

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

    def run(self):

        # Error handling for input file
        try:
            self.input_file_name = str(self.inputFileEntry.text())
            self.raxmlOperations.inputFilename = str(self.inputFileEntry.text())
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
            self.raxmlOperations.windowSize = int(self.windowSizeEntry.text())

            if self.window_size <= 0:
                raise ValueError, "Positive integers only"
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Window size needs to be a positive integer.")
            return

        # Error handling for window offset
        try:
            self.window_offset = int(self.windowOffsetEntry.text())
            self.raxmlOperations.windowOffset = int(self.windowOffsetEntry.text())

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

        self.runProgressBar()

        #####################################################################


        self.runComplete = True
        # self.updatedDisplayWindows()
        self.menuExport.setEnabled(True)


if __name__ == '__main__':  # if we're running file directly and not importing it
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication

    # initialize main input window
    form = PhyloVisApp()  # We set the form to be our PhyloVisApp (design)
    form.show()  # Show the form

    sys.exit(app.exec_())  # and execute the app
