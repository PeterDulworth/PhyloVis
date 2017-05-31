from PyQt4 import QtGui
import sys
import gui_layout as gui
import os


class PhyloVisApp(QtGui.QMainWindow, gui.Ui_PhylogenicVisualization):
    def __init__(self, parent=None):
        super(PhyloVisApp, self).__init__(parent)
        self.setupUi(self)

        # if input file button is clicked run function -- file_open
        self.inputFileBtn.clicked.connect(self.input_file_open)

        # if output dir button is clicked run function -- file_open
        self.outputDirBtn.clicked.connect(self.output_file_open)

        # run
        self.runBtn.clicked.connect(self.run)


    # def browse_folder(self):
    #     self.listWidget.clear()
    #     directory = QtGui.QFileDialog.getExistingDirectory(self,
    #                                                        "Pick a folder")
    #
    #     if directory:
    #         for file_name in os.listdir(directory):
    #             self.listWidget.addItem(file_name)

    def selectFile(self):
        self.input_file_entry.setText(QtGui.QFileDialog.getOpenFileName())

    def input_file_open(self):
        # get name of file
        name = QtGui.QFileDialog.getOpenFileName()
        # set name of file to text entry
        self.input_file_entry.setText(name)

        # file = open(name, 'r')
        # with file:
        #     text = file.read()
        #     print text

    def output_file_open(self):
        # get name of file
        name = QtGui.QFileDialog.getOpenFileName()
        # set name of file to text entry
        self.output_dir_entry.setText(name)

        # file = open(name, 'r')
        # with file:
        #     text = file.read()
        #     print text

    def run(self):
        input_file_name = self.input_file_entry.text()
        output_dir_name = self.output_dir_entry.text()
        window_size = self.window_size_entry.text()
        window_offset = self.window_offset_entry.text()

        print 'Input File Name:', input_file_name
        print 'Output Directory Name:', output_dir_name
        print 'Window Size:', window_size
        print 'Window Offset:', window_offset

def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = PhyloVisApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function