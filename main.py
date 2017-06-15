import sip
sip.setapi('QString', 2)
import sys, os
import gui_layout as gui
import time
import visualizationPrototype as vp
from PIL import Image
from PyQt4 import QtGui, QtCore
from shutil import copyfile, copytree
from outputWindows import allTreesWindow, donutPlotWindow, scatterPlotWindow, circleGraphWindow
import topologyFrequency as tf
import matplotlib.pyplot as plt
import circleGraphGenerator

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

        # windows dictionary
        self.windows = {'welcomePage': 0, 'inputPageRax': 1, 'inputPageNotRaxA': 2, 'inputPageNotRaxB': 3, 'inputPageNotRaxC': 4,
                        'outputPage': 5}

        self.runComplete = False

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
        self.actionRAXDirectory.triggered.connect(lambda: self.exportDirectory('RAx_Files'))
        self.actionTreesDirectory.triggered.connect(lambda: self.exportDirectory('Trees'))

        # set up other windows
        self.allTreesWindow = allTreesWindow.AllTreesWindow()
        self.scatterPlotWindow = scatterPlotWindow.ScatterPlotWindow()
        self.circleGraphWindow = circleGraphWindow.CircleGraphWindow()
        self.donutPlotWindow = donutPlotWindow.DonutPlotWindow()

        self.checkboxCircleGraph.stateChanged.connect(lambda: self.updatedDisplayWindows(btnClicked=self.checkboxCircleGraph))
        self.checkboxScatterPlot.stateChanged.connect(lambda: self.updatedDisplayWindows(btnClicked=self.checkboxScatterPlot))
        self.checkboxAllTrees.stateChanged.connect(lambda: self.updatedDisplayWindows(btnClicked=self.checkboxAllTrees))
        self.checkboxDonutPlot.stateChanged.connect(lambda: self.updatedDisplayWindows(btnClicked=self.checkboxDonutPlot))

        # **************************** Rax Input Page Events ****************************#

        # ensure window is at minimum size when opened
        self.resize(0,0)

        # if input file button is clicked run function -- file_open
        self.inputFileBtn.clicked.connect(self.input_file_open)
        self.actionOpen.triggered.connect(self.input_file_open)

        # set start page to the input page
        self.stackedWidget.setCurrentIndex(0)

        # run
        self.runBtn.clicked.connect(self.run)
        self.progressBar.reset()

        # disable export menu initially
        self.menuExport.setEnabled(False)

        # **************************** Rax Welcome Page Events ****************************#

        self.raxBtn.clicked.connect(lambda: self.setWindow('inputPageRax'))
        self.notRax1Btn.clicked.connect(lambda: self.setWindow('inputPageNotRaxA'))
        self.notRax2Btn.clicked.connect(lambda: self.setWindow('inputPageNotRaxB'))
        self.notRax3Btn.clicked.connect(lambda: self.setWindow('inputPageNotRaxC'))

        self.raxBtn.clicked.connect(lambda: self.ensureSingleModeSelected(self.actionRax))
        self.notRax1Btn.clicked.connect(lambda: self.ensureSingleModeSelected(self.actionNotRaxA))
        self.notRax2Btn.clicked.connect(lambda: self.ensureSingleModeSelected(self.actionNotRaxB))
        self.notRax3Btn.clicked.connect(lambda: self.ensureSingleModeSelected(self.actionNotRaxC))

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

    def getNumberChecked(self):
        """
        returns the number of checkboxes that are checked
        """
        return (self.checkboxScatterPlot.checkState() + self.checkboxCircleGraph.checkState() + self.checkboxDonutPlot.checkState() + self.checkboxAllTrees.checkState()) / 2

    def updatedDisplayWindows(self, btnClicked=None):

        if btnClicked == None or btnClicked.isChecked():
            if self.runComplete == True:
                print 'UPDATEBITCH'
                if self.getNumberChecked() > 0:
                    # User inputs:
                    num = self.topTopologies #
                    # Function calls for plotting inputs:
                    topologies_to_counts = tf.topology_counter()
                    list_of_top_counts, labels, sizes = tf.top_freqs(num, topologies_to_counts)
                    top_topologies_to_counts = tf.top_topologies(num, topologies_to_counts)
                    windows_to_top_topologies, top_topologies_list = tf.windows_to_newick(top_topologies_to_counts) # all trees, scatter, circle, donut
                    topologies_to_colors, scatter_colors, ylist = tf.topology_colors(windows_to_top_topologies, top_topologies_list)  # scatter, circle, (donut?)
                    # print windows_to_top_topologies

                if self.checkboxDonutPlot.isChecked():
                    donut_colors = tf.donut_colors(top_topologies_to_counts, topologies_to_colors) # donut
                    tf.topology_donut(num, list_of_top_counts, labels, sizes, donut_colors)  # donut
                    self.displayResults()

                if self.checkboxScatterPlot.isChecked():
                    tf.topology_scatter(windows_to_top_topologies, scatter_colors, ylist)  # scatter
                    self.displayResults()

                if self.checkboxAllTrees.isChecked():
                    tf.topology_colorizer(topologies_to_colors) # all trees
                    self.displayResults()

                if self.checkboxCircleGraph.isChecked():
                    circleGraphGenerator.generateCircleGraph(self.input_file_name, windows_to_top_topologies, topologies_to_colors, self.window_size, self.window_offset)
                    self.displayResults()

    def setWindow(self, window):
        self.stackedWidget.setCurrentIndex(self.windows[window])
        self.resize(0, 0)

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

    def input_file_open(self):
        # get name of file
        name = QtGui.QFileDialog.getOpenFileName()
        # set name of file to text entry
        self.inputFileEntry.setText(name)

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
                raise ValueError, (2, "Luay does not approve of your filetype.\nPlease enter either a .txt, .fasta, or .phylip file")
        except ValueError, (ErrorNumber, ErrorMessage):
            QtGui.QMessageBox.about(self, "Invalid Input", str(ErrorMessage))
            return

        # Error handling for number of top topologies
        try:
            self.topTopologies = int(self.numberOfTopTopologiesEntry.text())
            if self.topTopologies <= 0 or self.topTopologies > 15:
                raise ValueError, "Please enter an integer between 0 and 15."
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Number of top topologies needs to be an integer between 0 and 15.")
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

        # self.runProgressBar()

        try:
            self.windows_dirs = vp.splittr(self.input_file_name, self.window_size, self.window_offset) # run once - not rerun
            self.RAx_dirs = vp.raxml_windows(self.windows_dirs) # run once - not rerun
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