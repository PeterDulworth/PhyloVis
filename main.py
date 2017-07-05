# utilities
import sip
sip.setapi('QString', 2)
import sys, os
from PIL import Image
from PyQt4 import QtGui, QtCore
from shutil import copyfile, copytree
from functools import partial

# GUI
from raxmlOutputWindows import allTreesWindow, donutPlotWindow, scatterPlotWindow, circleGraphWindow, pgtstWindow, robinsonFouldsWindow, heatMapWindow, bootstrapContractionWindow, dStatisticWindow
from msOutputWindows import msRobinsonFouldsWindow
from module import gui_layout as gui

# logic
from module import RAxMLOperations as ro
from module import topologyPlots as tp
from module import statisticCalculations as sc
from module import fileConverterController as fcc
from module import informativeSites as infSites
from module import bootstrapContraction as bc
from module import msComparison as ms

# more important logic
from games import tetris, snake


class ErrorHandling(object):
    def __init__(self):
        pass


class PhyloVisApp(QtGui.QMainWindow, gui.Ui_PhylogeneticVisualization):
    def __init__(self, parent=None):
        super(PhyloVisApp, self).__init__(parent)
        self.setupUi(self)

        self.dStatisticTaxonComboBoxes = [self.dTaxonComboBox1, self.dTaxonComboBox2, self.dTaxonComboBox3, self.dTaxonComboBox4]
        self.raxmlTaxonComboBoxes = [self.outgroupComboBox]

        # set UI style
        # options: [u'Windows', u'Motif', u'CDE', u'Plastique', u'Cleanlooks', u'Macintosh (aqua)']
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'Macintosh (aqua)'))

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # gui icon
        self.setWindowIcon(QtGui.QIcon('Luay.jpg'))

        # self.welcomeLogoImage.setScaledContents(True)
        self.welcomeLogoImage.setPixmap(QtGui.QPixmap('Luay.jpg'))

        # create new instance of RaxmlOperations class
        self.raxmlOperations = ro.RAxMLOperations(None, None, None, None)
        # every time the 'RAX_PER' signal is emitted -> update the progress bar
        self.connect(self.raxmlOperations, QtCore.SIGNAL('RAX_PER'), self.progressBar.setValue)
        self.connect(self.raxmlOperations, QtCore.SIGNAL('RAX_COMPLETE'), self.updatedDisplayWindows)
        self.connect(self.raxmlOperations, QtCore.SIGNAL('RAX_COMPLETE'), lambda: self.progressBar.setValue(100))
        self.connect(self.raxmlOperations, QtCore.SIGNAL('SPECIES_TREE_PER'), self.updateSpeciesTreeProgressBar)
        self.connect(self.raxmlOperations, QtCore.SIGNAL('INVALID_ALIGNMENT_FILE'), lambda: self.message('Invalid File', 'Invalid alignment file. Please choose another.', 'Make sure your file has 4 sequences and is in the phylip-relaxed format.', type='Err'))
        self.connect(self.raxmlOperations, QtCore.SIGNAL('INVALID_ALIGNMENT_FILE'), self.connectionTester)

        # create new instance of TopologyPlotter class
        self.topologyPlotter = tp.TopologyPlotter()
        # create new instance of Statistics Calculations class
        self.statisticsCalculations = sc.StatisticsCalculations()
        # create new instance of Informative Sites class
        self.informativeSites = infSites.InformativeSites()
        # create new instance of BootstrapContraction class
        self.bootstrapContraction = bc.BootstrapContraction()
        # create new instance of MsComparison class
        self.msComparison = ms.MsComparison()

        # mapping from: windows --> page index
        self.windows = {'welcomePage': 0, 'inputPageRax': 1, 'inputPageFileConverter': 2, 'inputPageMS': 3, 'inputPageDStatistic': 4}
        # mapping from: windows --> dictionary of page dimensions 493
        self.windowSizes = {'welcomePage': {'x': 459, 'y': 245}, 'inputPageRax': {'x': 600, 'y': 530}, 'inputPageFileConverter': {'x': 459, 'y': 245 + 40}, 'inputPageMS': {'x': 459, 'y': 306}, 'inputPageDStatistic': {'x': 600, 'y': 570}}
        # mapping from: mode --> page
        self.comboboxModes_to_windowNames = {'RAx_ML': 'inputPageRax', 'File Converter': 'inputPageFileConverter', 'MS Comparison': 'inputPageMS', 'D Statistic': 'inputPageDStatistic'}
        # mapping from: mode --> menu action
        self.comboboxModes_to_actionModes = {'RAx_ML': self.actionRax, 'File Converter': self.actionConverter, 'MS Comparison': self.actionMS, 'D Statistic': self.actionDStatistic}

        if sys.platform == 'win32':
            # mapping from: windows --> dictionary of page dimensions 493
            self.windowSizes = {'welcomePage': {'x': 459, 'y': 245}, 'inputPageRax': {'x': 871, 'y': 688}, 'inputPageFileConverter': {'x': 630, 'y': 275}, 'inputPageMS': {'x': 600, 'y': 375}, 'inputPageDStatistic': {'x': 600, 'y': 570}}

        # initialize window
        self.allTreesWindow = allTreesWindow.AllTreesWindow()
        self.scatterPlotWindow = scatterPlotWindow.ScatterPlotWindow()
        self.circleGraphWindow = circleGraphWindow.CircleGraphWindow()
        self.donutPlotWindow = donutPlotWindow.DonutPlotWindow()
        self.pgtstWindow = pgtstWindow.PGTSTWindow()
        self.robinsonFouldsWindow = robinsonFouldsWindow.RobinsonFouldsWindow()
        self.heatMapWindow = heatMapWindow.HeatMapWindow()
        self.bootstrapContractionWindow = bootstrapContractionWindow.BootstrapContractionWindow()
        self.msComparisonWindow = msRobinsonFouldsWindow.MSRobinsonFouldsWindow()
        self.dStatisticWindow = dStatisticWindow.DStatisticWindow()

        # remove all files in plots folder
        fileList = os.listdir('plots')
        for fileName in fileList:
            os.remove('plots/' + fileName)

        # default values
        self.runComplete = False
        self.checkboxWeighted.setEnabled(False)
        self.menuExport.setEnabled(False)
        self.outgroupComboBox.setEnabled(False)
        self.outgroupLabel.setEnabled(False)
        # self.statisticsOptionsPage.setEnabled(False)
        self.bootstrapGroupBox.setEnabled(False)
        self.outgroupGroupBox.setEnabled(False)
        self.progressBar.reset()
        self.generateSpeciesTreeProgressBar.reset()
        self.rooted = False
        self.stackedWidget.setCurrentIndex(0)
        self.raxmlToolBox.setCurrentIndex(0)
        self.raxmlOptionsTabWidget.setCurrentIndex(0)
        self.resize(self.windowSizes['welcomePage']['x'], self.windowSizes['welcomePage']['y'])

        # **************************** RAXML PAGE ****************************#

        # selecting a mode in the menu bar -> deselects all other modes first
        # change the input mode based on which mode is selected in the menu bar
        self.actionRax.triggered.connect(lambda: self.ensureSingleModeSelected(self.actionRax))
        self.actionRax.triggered.connect(lambda: self.setWindow('inputPageRax'))
        self.actionConverter.triggered.connect(lambda: self.ensureSingleModeSelected(self.actionConverter))
        self.actionConverter.triggered.connect(lambda: self.setWindow('inputPageFileConverter'))
        self.actionMS.triggered.connect(lambda: self.ensureSingleModeSelected(self.actionMS))
        self.actionMS.triggered.connect(lambda: self.setWindow('inputPageMS'))
        self.actionDStatistic.triggered.connect(lambda: self.ensureSingleModeSelected(self.actionDStatistic))
        self.actionDStatistic.triggered.connect(lambda: self.setWindow('inputPageDStatistic'))

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
        self.checkboxBootstrap.stateChanged.connect(lambda: self.updatedDisplayWindows(btnClicked=self.checkboxBootstrap))

        # toggle what inputs are actionable based on checkboxes
        # self.checkboxRobinsonFoulds.isChecked( or self.checkboxPGTST.isChecked())d.connect(lambda: self.toggleEnabled(self.statisticsOptionsPage))
        self.checkboxRobinsonFoulds.clicked.connect(lambda: self.toggleEnabled(self.checkboxWeighted))
        self.checkboxRooted.stateChanged.connect(lambda: self.toggleEnabled(self.outgroupComboBox))
        self.checkboxRooted.stateChanged.connect(lambda: self.toggleEnabled(self.outgroupLabel))
        self.checkboxBootstrap.stateChanged.connect(lambda: self.toggleEnabled(self.bootstrapGroupBox))
        self.checkboxRooted.stateChanged.connect(lambda: self.toggleEnabled(self.outgroupGroupBox))

        # when file entry text is changed
        self.connect(self.inputFileEntry, QtCore.SIGNAL("FILE_SELECTED"), lambda: self.updateTaxonComboBoxes(self.raxmlTaxonComboBoxes, self.inputFileEntry))

        # run RAX_ML and generate graphs
        self.runBtn.clicked.connect(self.runRAxML)
        self.generateSpeciesTreeBtn.clicked.connect(self.generateSpeciesTree)

        # **************************** WELCOME PAGE ****************************#

        self.launchBtn.clicked.connect(self.initializeMode)

        # **************************** CONVERTER PAGE ****************************#

        self.fileConverterBtn.clicked.connect(lambda: self.openFile(self.fileConverterEntry))
        self.runFileConverterBtn.clicked.connect(lambda: self.convertFile())

        # **************************** MS PAGE ****************************#

        self.msCompareBtn.clicked.connect(self.runMSCompare)
        self.msRaxmlDirectoryBtn.clicked.connect(lambda: self.openDirectory(self.msRaxmlDirectoryEntry))
        self.msFileBtn.clicked.connect(lambda: self.openFile(self.msFileEntry))

        # **************************** D STATISTIC PAGE ****************************#

        # set background image
        self.imagePixmap = QtGui.QPixmap('tree.png')
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setPixmap(self.imagePixmap)

        # run
        self.dAlignmentBtn.clicked.connect(lambda: self.openFile(self.dAlignmentEntry))

        # when file entry text is changed
        self.connect(self.dAlignmentEntry, QtCore.SIGNAL("FILE_SELECTED"), lambda: self.updateTaxonComboBoxes(self.dStatisticTaxonComboBoxes, self.dAlignmentEntry, errHandling=True))

        # update progress bar
        self.connect(self.statisticsCalculations, QtCore.SIGNAL('D_PER'), self.dProgressBar.setValue)
        self.connect(self.statisticsCalculations, QtCore.SIGNAL('D_FINISHED'), self.displayDStatistic)

        # run
        self.dRunBtn.clicked.connect(self.runDStatistic)
        self.connect(self.statisticsCalculations, QtCore.SIGNAL('INVALID_ALIGNMENT_FILE'), partial(self.message, type='testType2'))

        # reset progress bar when window is closed
        self.connect(self.dStatisticWindow, QtCore.SIGNAL('WINDOW_CLOSED'), lambda: self.dProgressBar.setValue(0))

    # **************************** WELCOME PAGE ****************************#

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

    # **************************** D STATISTIC PAGE ****************************#

    def updateTaxonComboBoxes(self, comboBoxes, textEntry, errHandling=False):
        try:
            if textEntry.text() == "":
                return

            # get list of taxon names from file
            taxonNames = list(self.raxmlOperations.taxon_names_getter(textEntry.text()))
            print 'taxonNames:', taxonNames

            if errHandling:
                # if there are not exactly 4 taxons
                if len(taxonNames) != 4:
                    self.message('Invalid File.', 'Need exactly 4 taxons.', textEntry.text())
                    return

            for comboBox in comboBoxes:
                comboBox.clear()

            for taxon in taxonNames:
                for comboBox in comboBoxes:
                    comboBox.addItem(taxon)

            for i in range(len(comboBoxes)):
                comboBoxes[i].setCurrentIndex(i)

        except:
            self.message('Invalid File', 'Invalid alignment file. Please choose another.', 'Make sure your file has 4 sequences and is in the phylip-relaxed format.', type='Err')
            return

    def runDStatistic(self):
        try:
            if self.dAlignmentEntry.text() == "":
                raise IOError
            self.statisticsCalculations.dAlignment = str(self.dAlignmentEntry.text())
            self.statisticsCalculations.dWindowSize = int(self.dWindowSizeEntry.text())
            self.statisticsCalculations.dWindowOffset = int(self.dWindowOffsetEntry.text())
            self.statisticsCalculations.taxon1 = self.dTaxonComboBox1.currentText()
            self.statisticsCalculations.taxon2 = self.dTaxonComboBox2.currentText()
            self.statisticsCalculations.taxon3 = self.dTaxonComboBox3.currentText()
            self.statisticsCalculations.taxon4 = self.dTaxonComboBox4.currentText()

        except:
            QtGui.QMessageBox.about(self, "sadfasdf", "1asdfasdf", "2asdfadsfasfd")

        self.statisticsCalculations.start()

    def displayDStatistic(self, val):
        self.D = val[0]
        self.DStat = val[1]
        self.statisticsCalculations.stat_scatter(self.DStat, "plots/WindowsToD.png", "Window Indices to D statistic", "Window Indices", "D statistic values")
        self.dStatisticWindow.show()
        self.dStatisticWindow.display_image()

    # **************************** MS PAGE ****************************#

    def runMSCompare(self):

        # run logic
        sites_to_newick_ms_map = self.msComparison.sites_to_newick_ms(self.msFileEntry.text())
        sites_to_newick_rax_map = self.msComparison.sites_to_newick_rax(self.msComparison.output_directory, int(self.msWindowSizeEntry.text()), int(self.msWindowOffsetEntry.text()))
        sites_to_difference_w, sites_to_difference_uw = self.msComparison.ms_rax_difference(sites_to_newick_ms_map, sites_to_newick_rax_map)

        # generate graphs
        self.statisticsCalculations.stat_scatter(sites_to_difference_w, "WRFdifference.png", "Difference Between MS and RAxML Output", "Sites Indices", "Weighted Robinson-Foulds Distance")
        self.statisticsCalculations.stat_scatter(sites_to_difference_uw, "UWRFdifference.png", "Difference Between MS and RAxML Output", "Sites Indices", "Unweighted Robinson-Foulds Distance")

        # display window
        self.msComparisonWindow.show()
        self.msComparisonWindow.displayImages()

    def updateSpeciesTreeProgressBar(self, val):
        self.generateSpeciesTreeProgressBar.setValue(self.generateSpeciesTreeProgressBar.value() + val)
        if self.generateSpeciesTreeProgressBar.value() >= 100:
            QtGui.QMessageBox.about(self, "Species Tree Complete", "Species Tree has been generated.")

    # **************************** CONVERTER PAGE ****************************#

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

    # **************************** RAXML PAGE ****************************#

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

        if self.checkboxBootstrap.isChecked():
            self.bootstrapContractionWindow.show()
            self.bootstrapContractionWindow.display_image()

        if self.checkboxRobinsonFoulds.isChecked() or self.checkboxPGTST.isChecked():
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

    def generateSpeciesTree(self):
        # Error handling for input file
        try:
            self.input_file_name = str(self.inputFileEntry.text())
            self.raxmlOperations.inputFilename = str(self.inputFileEntry.text())
            self.input_file_extension = os.path.splitext(self.input_file_name)[1]

            if self.input_file_name == "":
                raise ValueError, (1, "Please choose a file")
            elif self.input_file_extension != '.txt' and self.input_file_extension != '.phylip' and self.input_file_extension != '.fasta':
                raise ValueError, (
                    2, "Luay does not approve of your file type.\nPlease enter either a .txt, .fasta, or .phylip file")
        except ValueError, (ErrorNumber, ErrorMessage):
            QtGui.QMessageBox.about(self, "Invalid Input", str(ErrorMessage))
            return

        self.raxmlOperations.raxml_species_tree(self.input_file_name)

    def updatedDisplayWindows(self, btnClicked=None):

        if btnClicked == None or btnClicked.isChecked():
            if self.runComplete == True:
                if self.getNumberChecked() > 0:
                    # User inputs:
                    num = self.topTopologies

                    # Function calls for plotting inputs:
                    topologies_to_counts, unique_topologies_to_newicks = self.topologyPlotter.topology_counter(rooted=self.rooted, outgroup=self.outgroupComboBox.currentText())
                    if num > len(topologies_to_counts):
                        num = len(topologies_to_counts)
                    list_of_top_counts, labels, sizes = self.topologyPlotter.top_freqs(num, topologies_to_counts)
                    top_topologies_to_counts = self.topologyPlotter.top_topologies(num, topologies_to_counts)
                    windows_to_top_topologies, top_topologies_list = self.topologyPlotter.windows_to_newick(
                            top_topologies_to_counts, unique_topologies_to_newicks, rooted=self.rooted, outgroup=self.outgroupComboBox.currentText())  # all trees, scatter, circle, donut
                    topologies_to_colors, scatter_colors, ylist = self.topologyPlotter.topology_colors(windows_to_top_topologies, top_topologies_list)  # scatter, circle, (donut?)

                if self.checkboxDonutPlot.isChecked():
                    donut_colors = self.topologyPlotter.donut_colors(top_topologies_to_counts, topologies_to_colors)  # donut
                    self.topologyPlotter.topology_donut(labels, sizes, donut_colors)  # donut

                if self.checkboxScatterPlot.isChecked():
                    self.topologyPlotter.topology_scatter(windows_to_top_topologies, scatter_colors, ylist)  # scatter

                if self.checkboxCircleGraph.isChecked():
                    sites_to_informative, windows_to_informative_count, windows_to_informative_pct, pct_informative = self.informativeSites.calculate_informativeness('windows', self.window_offset)
                    self.topologyPlotter.generateCircleGraph(self.input_file_name, windows_to_top_topologies, topologies_to_colors, self.window_size, self.window_offset, sites_to_informative)

                if self.checkboxHeatMap.isChecked():
                    sites_to_informative, windows_to_informative_count, windows_to_informative_pct, pct_informative = self.informativeSites.calculate_informativeness('windows', self.window_offset)
                    self.informativeSites.heat_map_generator(sites_to_informative, "plots/HeatMapInfSites.png")

                if self.checkboxRobinsonFoulds.isChecked() or self.checkboxPGTST.isChecked():
                    if self.checkboxRobinsonFoulds.isChecked():
                        if self.checkboxWeighted.isChecked():
                            windows_to_w_rf, windows_to_uw_rf = self.statisticsCalculations.calculate_windows_to_rf(self.speciesTree, self.checkboxWeighted.isChecked())

                            self.statisticsCalculations.stat_scatter(windows_to_w_rf, "plots/WeightedFouldsPlot.png", "Weighted Robinson-Foulds Distance", "Windows", "RF Distance")
                            self.statisticsCalculations.stat_scatter(windows_to_uw_rf, "plots/UnweightedFouldsPlot.png", "Unweighted Robinson-Foulds Distance", "Windows", "RF Distance")

                        else:
                            windows_to_uw_rf = self.statisticsCalculations.calculate_windows_to_rf(self.speciesTree, self.checkboxWeighted.isChecked())
                            self.statisticsCalculations.stat_scatter(windows_to_uw_rf, "plots/UnweightedFouldsPlot.png", "Unweighted Robinson-Foulds Distance", "Windows", "RF Distance")

                    if self.checkboxPGTST.isChecked():
                        # Function calls for calculating statistics
                        windows_to_p_gtst = self.statisticsCalculations.calculate_windows_to_p_gtst(self.speciesTree)
                        self.statisticsCalculations.stat_scatter(windows_to_p_gtst, "plots/PGTSTPlot.png", "p(gt|st)", "Windows", "Probability")

                if self.checkboxBootstrap.isChecked():
                    xLabel = "Window Indices"
                    yLabel = "Number of Internal Nodes"
                    name = "plots/ContractedGraph.png"
                    internal_nodes_i, internal_nodes_f = self.bootstrapContraction.internal_nodes_after_contraction(self.confidenceLevel)
                    # generate bootstrap confidence graph
                    self.bootstrapContraction.double_line_graph_generator(internal_nodes_i, internal_nodes_f, xLabel, yLabel, name, self.confidenceLevel)

                if self.checkboxAllTrees.isChecked():
                    if self.checkboxRooted.isChecked():
                        self.topologyPlotter.topology_colorizer(topologies_to_colors, rooted=self.rooted, outgroup=self.outgroupComboBox.currentText())  # all trees
                        self.topologyPlotter.top_topology_visualization()
                    else:
                        self.topologyPlotter.topology_colorizer(topologies_to_colors, rooted=False, outgroup="")  # all trees
                        self.topologyPlotter.top_topology_visualization()

                self.displayResults()

    def raxmlInputErrorHandling(self):
        # Error handling for input file
        try:
            self.input_file_name = str(self.inputFileEntry.text())
            self.raxmlOperations.inputFilename = str(self.inputFileEntry.text())
            self.input_file_extension = os.path.splitext(self.input_file_name)[1]

            if self.input_file_name == "":
                raise ValueError, (1, "Please choose a file")
            elif self.input_file_extension != '.txt' and self.input_file_extension != '.phylip' and self.input_file_extension != '.fasta':
                raise ValueError, (
                    2, "Luay does not approve of your file type.\nPlease enter either a .txt, .fasta, or .phylip file")
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
            if self.checkboxRobinsonFoulds.isChecked() or self.checkboxPGTST.isChecked():
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

        # error handling for is rooted checkbox
        try:
            if self.checkboxRooted.isChecked():
                self.rooted = self.checkboxRooted.isChecked()
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Invalid Input")
            return

        # Error handling for confidence threshold
        try:
            if self.checkboxBootstrap.isChecked():
                self.confidenceLevel = int(self.confidenceLevelEntry.text())
                if self.confidenceLevel < 0 or self.confidenceLevel > 100:
                    raise ValueError, "Please enter an integer between 0 and 100."
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Confidence level needs to be an integer between 0 and 100.")
            return

        # Error handling for number of bootstraps
        try:
            if self.checkboxBootstrap.isChecked():
                self.numBootstraps = int(self.numberOfBootstrapsEntry.text())
                self.raxmlOperations.numBootstraps = int(self.numberOfBootstrapsEntry.text())
                if self.numBootstraps < 2:
                    raise ValueError, "Please enter an integer greater than 1."
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Number of bootstraps needs to be an integer greater than 1.")
            return

    def runRAxML(self):

        self.raxmlInputErrorHandling()

        self.raxmlOperations.customRaxmlCommand = self.checkBoxCustomRaxml.isChecked()
        self.raxmlOperations.raxmlCommand = self.customRaxmlCommandEntry.text()
        self.raxmlOperations.bootstrap = self.checkboxBootstrap.isChecked()
        self.raxmlOperations.model = self.modelComboBox.currentText()

        self.raxmlOperations.start()

        #####################################################################

        self.runComplete = True
        self.menuExport.setEnabled(True)

    # **************************** ABSTRACT ****************************#

    def message(self, title, description, extraInfo, type='Err'):
        """
            creates and displays and window displaying the message
        """

        # create object
        errMessage = QtGui.QMessageBox()

        # set text
        errMessage.setText(title)
        errMessage.setInformativeText(description)
        errMessage.setDetailedText(extraInfo)

        # default pixmap for error
        pixmap = QtGui.QPixmap('warning-128.lowQual.png')

        # choose icon based on type
        if type=='testType2':
            pixmap = 'tree.png'

        # set icon
        errMessage.setIconPixmap(pixmap)

        # execute window
        errMessage.exec_()

    def getNumberChecked(self):
        """
        returns the number of checkboxes that are checked
        """
        return (self.checkboxHeatMap.checkState() + self.checkboxScatterPlot.checkState() + self.checkboxCircleGraph.checkState() + self.checkboxDonutPlot.checkState() + self.checkboxAllTrees.checkState()) / 2

    def toggleEnabled(self, object):
        enabled = object.isEnabled()
        object.setEnabled(not enabled)

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
        textEntry.emit(QtCore.SIGNAL('FILE_SELECTED'))

    def openDirectory(self, textEntry):
        # get name of file
        name = QtGui.QFileDialog.getExistingDirectory()
        # set name of file to text entry
        textEntry.setText(name)
        textEntry.emit(QtCore.SIGNAL("DIRECTORY_SELECTED"))

    def resizeEvent(self, event):
        print self.size()

    def moveEvent(self, QMoveEvent):
        print self.pos()

    def connectionTester(self):
        print
        print '*********************************'
        print '* CONNECTION HAS BEEN TRIGGERED *'
        print '*********************************'
        print


if __name__ == '__main__':  # if we're running file directly and not importing it
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication

    # initialize main input window
    form = PhyloVisApp()  # We set the form to be our PhyloVisApp (design)
    form.show()  # Show the form

    sys.exit(app.exec_())  # and execute the app
