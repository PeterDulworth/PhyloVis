from PyQt4 import QtGui
import sys
import gui_layout as gui
import os


class PhyloVisApp(QtGui.QMainWindow, gui.Ui_PhylogenicVisualization):
    def __init__(self, parent=None):
        super(PhyloVisApp, self).__init__(parent)
        self.setupUi(self)

        ############################# Link Events ##############################

        # if input file button is clicked run function -- file_open
        self.inputFileBtn.clicked.connect(self.input_file_open)

        # if output dir button is clicked run function -- file_open
        self.outputDirBtn.clicked.connect(self.output_dir_open)

        # run
        self.runBtn.clicked.connect(self.run)

    ################################# Handlers #################################

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

    def run(self):
        input_file_name = self.inputFileEntry.text()
        output_dir_name = self.outputDirEntry.text()
        window_size = self.windowSizeEntry.text()
        window_offset = self.windowOffsetEntry.text()

        print 'Input File Name:', input_file_name
        print 'Output Directory Name:', output_dir_name
        print 'Window Size:', window_size
        print 'Window Offset:', window_offset

def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = PhyloVisApp()                # We set the form to be our PhyloVisApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function