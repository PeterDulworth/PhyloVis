import sys, os
import gui_layout as gui
import time
import visualizationPrototype as vp
from PyQt4 import QtGui


class PhyloVisApp(QtGui.QMainWindow, gui.Ui_PhylogeneticVisualization):
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
        self.progressBar.reset()

    ################################# Handlers #################################

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
        # input_file_name = "/Users/Peter/PycharmProjects/Evolutionary-Diversity-Visualization-Python/phylip.txt"
        # output_dir_name = "/Users/Peter/PycharmProjects/Evolutionary-Diversity-Visualization-Python/windows"
        # window_size = 10
        # window_offset = 10
        # vp.image_combination(vp.tree_display(vp.RAxML_windows(vp.splittr(input_file_name, window_size, window_offset, output_dir_name)), "Trees"),vp.scatter(vp.num_windows(output_dir_name), vp.ml(vp.num_windows(output_dir_name), 'RAx_Files')))

        try:
            input_file_name = str(self.inputFileEntry.text())
            print 'Input File Name:', input_file_name
        except ValueError:
            QtGui.QMessageBox.warning(self, "Invalid Input", "Input filename needs to be a string.", "Ok")
            return
        try:
            output_dir_name = str(self.outputDirEntry.text())
            print 'Output Directory Name:', output_dir_name
        except ValueError:
            QtGui.QMessageBox.warning(self, "Invalid Input", "Output directory needs to be a string.", "Ok")
            return
        try:
            window_size = int(self.windowSizeEntry.text())
            print 'Window Size:', window_size
        except ValueError:
            QtGui.QMessageBox.warning(self, "Invalid Input", "Window size needs to be an integer.", "Ok")
            return
        try:
            window_offset = int(self.windowOffsetEntry.text())
            print 'Window Offset:', window_offset
        except ValueError:
            QtGui.QMessageBox.warning(self, "Invalid Input", "Window offset needs to be an integer.", "Ok")
            return

        # with open(input_file_name) as f:
        #     self.numberOfSequences = int(f.readline())
        # f.close()


        self.runProgressBar()
        output_dir_name = output_dir_name.replace("\\", "/")
        vp.image_combination(vp.tree_display(vp.RAxML_windows(vp.splittr(input_file_name, window_size, window_offset, output_dir_name)),"Trees"),vp.scatter(vp.num_windows(output_dir_name), vp.ml(vp.num_windows(output_dir_name), 'RAx_Files')))

        # while True:
        #     time.sleep(0.05)
        #     self.progressBar.setValue(int(vp.count * (100.0 / self.numberOfSequences)))
        #     QtGui.qApp.processEvents()
            # if vp.count >= self.numberOfSequences:
            #     break


def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = PhyloVisApp()                # We set the form to be our PhyloVisApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function