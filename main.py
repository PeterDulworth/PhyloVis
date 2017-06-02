import sys, os
import gui_layout as gui
import time
import visualizationPrototype as vp
from PIL import Image
from PyQt4 import QtGui

standardSize = Image.open("Final.jpg").size
bootstrapSize = Image.open("FinalBootstraps.jpg").size
print standardSize, bootstrapSize

class PhyloVisApp(QtGui.QMainWindow, gui.Ui_PhylogeneticVisualization):

    def __init__(self, parent=None):
        super(PhyloVisApp, self).__init__(parent)
        self.setupUi(self)

        ############################# Link Events ##############################

        # if input file button is clicked run function -- file_open
        self.inputFileBtn.clicked.connect(self.input_file_open)

        # if output dir button is clicked run function -- file_open
        self.outputDirBtn.clicked.connect(self.output_dir_open)

        # set start page to the input page
        self.stackedWidget.setCurrentIndex(0)

        # run
        self.runBtn.clicked.connect(self.run)
        self.progressBar.reset()

    ################################# Handlers #################################

    def changeWindow(self):
        """
            switch windows
        """
        if self.stackedWidget.currentIndex() == 0:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)

    def setProgressBarVal(self, val):
        self.progressBar.setValue(val)

    def input_file_open(self):
        # get name of file
        name = QtGui.QFileDialog.getOpenFileName()
        # set name of file to text entry
        self.inputFileEntry.setText(name)

    def output_dir_open(self):
        # get name of file
        name = QtGui.QFileDialog.getExistingDirectory()
        # set name of file to text entry
        self.outputDirEntry.setText(name)

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

        # Error handling for output directory
        try:
            output_dir_name = str(self.outputDirEntry.text())

            if output_dir_name == "":
                raise ValueError, (1, "Please choose a directory")
            print 'Output Directory Name:', output_dir_name
        except ValueError, (ErrorNumber, ErrorMessage):
            QtGui.QMessageBox.about(self, "Invalid Input", str(ErrorMessage))
            return

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

        output_dir_name = output_dir_name.replace("\\", "/")
        windows_dirs = vp.splittr(input_file_name
                                  , window_size, window_offset, output_dir_name)
        RAx_dirs = vp.raxml_windows(windows_dirs)
        Tree_dir = vp.tree_display(RAx_dirs)
        num = vp.num_windows(windows_dirs[0])
        likelihood = vp.ml(num, RAx_dirs[0])
        plot = vp.scatter(num, likelihood, output_dir_name)
        vp.image_combination(Tree_dir, plot, output_dir_name)
        self.standardImage.setPixmap(QtGui.QPixmap("Final.jpg"))
        self.bootstrapImage.setPixmap(QtGui.QPixmap("FinalBootstraps.jpg"))
        self.changeWindow()


def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = PhyloVisApp()                # We set the form to be our PhyloVisApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function