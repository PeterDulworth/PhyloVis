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
# import circleGraphGenerator

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

    def displayResults(self):
        # self.setWindow('outputPage')
        # self.outputTabs.setCurrentIndex(0)

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
            input_file_name = str(self.inputFileEntry.text())
            input_file_extension = os.path.splitext(input_file_name)[1]

            if input_file_name == "":
                raise ValueError, (1, "Please choose a file")
            elif input_file_extension != '.txt' and input_file_extension != '.phylip' and input_file_extension != '.fasta':
                raise ValueError, (2, "Luay does not approve of your filetype.\nPlease enter either a .txt, .fasta, or .phylip file")
        except ValueError, (ErrorNumber, ErrorMessage):
            QtGui.QMessageBox.about(self, "Invalid Input", str(ErrorMessage))
            return

        # Error handling for number of top topologies
        try:
            topTopologies = int(self.numberOfTopTopologiesEntry.text())
            if topTopologies <= 0 or topTopologies > 15:
                raise ValueError, "Please enter an integer between 0 and 15."
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Number of top topologies needs to be an integer between 0 and 15.")
            return

        # Error handling for window size
        try:
            window_size = int(self.windowSizeEntry.text())
            if window_size <= 0:
                raise ValueError, "Positive integers only"
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Window size needs to be a positive integer.")
            return

        # Error handling for window offset
        try:
            window_offset = int(self.windowOffsetEntry.text())
            if window_offset <= 0:
                raise ValueError, "Positive integers only"
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Window offset needs to be a positive integer.")
            return

        # self.runProgressBar()

        try:
            windows_dirs = vp.splittr(input_file_name, window_size, window_offset)
            RAx_dirs = vp.raxml_windows(windows_dirs)
            Tree_dir = vp.tree_display(RAx_dirs)
            num = vp.num_windows(windows_dirs)
            # likelihood = vp.ml(num, RAx_dirs)
            # plot = vp.scatter(num, likelihood)
            # vp.image_combination(Tree_dir, plot)
        except IndexError:
            QtGui.QMessageBox.about(self, "asd", "Invalid file format.\nPlease check your data.")
            return

        #####################################################################



        # User inputs:
        num = topTopologies

        # Function calls for plotting inputs:
        topologies_to_counts = tf.topology_counter()

        list_of_top_counts, labels, sizes = tf.top_freqs(num, topologies_to_counts)

        top_topologies_to_counts = tf.top_topologies(num, topologies_to_counts)

        windows_to_top_topologies, top_topologies_list = tf.windows_to_newick(top_topologies_to_counts)
        print windows_to_top_topologies
        topologies_to_colors, scatter_colors, ylist = tf.topology_colors(windows_to_top_topologies, top_topologies_list)
        print topologies_to_colors

        # donut_colors = tf.donut_colors(top_topologies_to_counts, topologies_to_colors)

        # Functions for creating plots
        # tf.topology_scatter(windows_to_top_topologies, scatter_colors, ylist)
        # tf.topology_donut(num, list_of_top_counts, labels, sizes, donut_colors)
        # tf.topology_colorizer(topologies_to_colors)

        #####################################################################

        # open images in gui
        standardSize = Image.open("Final.png").size

        self.standardImage.setScaledContents(True)
        self.standardImage.setPixmap(QtGui.QPixmap("Final.png"))

        self.bootstrapImage.setScaledContents(True)
        self.bootstrapImage.setPixmap(QtGui.QPixmap("FinalBootstraps.png"))

        self.displayResults()
        self.menuExport.setEnabled(True)
        # self.resize(int(standardSize[0]), int(standardSize[1]))

if __name__ == '__main__':  # if we're running file directly and not importing it
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication

    # initialize main input window
    form = PhyloVisApp()  # We set the form to be our PhyloVisApp (design)
    form.show()  # Show the form

    sys.exit(app.exec_())  # and execute the app