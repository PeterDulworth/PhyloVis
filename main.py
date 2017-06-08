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

class PhyloVisApp(QtGui.QMainWindow, gui.Ui_PhylogeneticVisualization):
    def __init__(self, parent=None):
        super(PhyloVisApp, self).__init__(parent)
        self.setupUi(self)

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # gui icon
        self.setWindowIcon(QtGui.QIcon('Luay.jpg'))

        # windows dictionary
        self.windows = {'inputPageRax': 0, 'inputPageNotRaxA': 1, 'inputPageNotRaxB': 2, 'inputPageNotRaxC': 3,
                        'outputPage': 4}

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

        self.allTreesWindow = allTreesWindow.AllTreesWindow()
        self.scatterPlotWindow = scatterPlotWindow.ScatterPlotWindow()
        self.circleGraphWindow = circleGraphWindow.CircleGraphWindow()
        self.donutPlotWindow = donutPlotWindow.DonutPlotWindow()

        # **************************** Rax Input Page Events ****************************#

        # ensure window is at minimum size when opened
        self.resize(0,0)

        # if input file button is clicked run function -- file_open
        self.inputFileBtn.clicked.connect(self.input_file_open)

        # set start page to the input page
        self.stackedWidget.setCurrentIndex(0)

        # run
        self.runBtn.clicked.connect(self.run)
        self.progressBar.reset()

        # disable export menu initially
        # self.menuExport.setEnabled(False)

    ################################# Handlers #################################

    def displayResults(self):
        """
            dynamically display output windows
        """

        # self.setWindow('outputPage')
        # self.outputTabs.setCurrentIndex(0)

        if self.checkboxAllTrees.isChecked():
            self.allTreesWindow.show()

        if self.checkboxCircleGraph.isChecked():
            self.circleGraphWindow.show()

        if self.checkboxDonutPlot.isChecked():
            self.donutPlotWindow.show()

        if self.checkboxScatterPlot.isChecked():
            self.scatterPlotWindow.show()




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
            print input_file_extension

            if input_file_name == "":
                raise ValueError, (1, "Please choose a file")
            elif input_file_extension != '.txt' and input_file_extension != '.phylip' and input_file_extension != '.fasta':
                raise ValueError, (2, "Invalid File Type\nPlease enter either a .txt, .fasta, or .phylip file")
            print 'Input File Name:', input_file_name
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

        # # Error handling for output directory
        # try:
        #     output_dir_name = str(self.outputDirEntry.text())
        #
        #     if output_dir_name == "":
        #         raise ValueError, (1, "Please choose a directory")
        #     print 'Output Directory Name:', output_dir_name
        # except ValueError, (ErrorNumber, ErrorMessage):
        #     QtGui.QMessageBox.about(self, "Invalid Input", str(ErrorMessage))
        #     return

        # Error handling for window size
        try:
            window_size = int(self.windowSizeEntry.text())
            if window_size <= 0:
                raise ValueError, "Positive integers only"
            print 'Window Size:', window_size
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Window size needs to be a positive integer.")
            return

        # Error handling for window offset
        try:
            window_offset = int(self.windowOffsetEntry.text())
            if window_offset <= 0:
                raise ValueError, "Positive integers only"
            print 'Window Offset:', window_offset
        except ValueError:
            QtGui.QMessageBox.about(self, "Invalid Input", "Window offset needs to be a positive integer.")
            return

        # self.runProgressBar()

        windows_dirs = vp.splittr(input_file_name, window_size, window_offset)
        RAx_dirs = vp.raxml_windows(windows_dirs)
        Tree_dir = vp.tree_display(RAx_dirs)
        num = vp.num_windows(windows_dirs)
        likelihood = vp.ml(num, RAx_dirs)
        plot = vp.scatter(num, likelihood)
        vp.image_combination(Tree_dir, plot)

        # open images in gui
        standardSize = Image.open("Final.jpg").size

        self.standardImage.setScaledContents(True)
        self.standardImage.setPixmap(QtGui.QPixmap("Final.jpg"))

        self.bootstrapImage.setScaledContents(True)
        self.bootstrapImage.setPixmap(QtGui.QPixmap("FinalBootstraps.jpg"))

        self.displayResults()
        self.menuExport.setEnabled(True)
        # self.resize(int(standardSize[0]), int(standardSize[1]))

if __name__ == '__main__':  # if we're running file directly and not importing it
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication

    # initialize main input window
    form = PhyloVisApp()  # We set the form to be our PhyloVisApp (design)
    form.show()  # Show the form

    sys.exit(app.exec_())  # and execute the app