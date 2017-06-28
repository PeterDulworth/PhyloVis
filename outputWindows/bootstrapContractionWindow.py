from PyQt4 import QtGui, QtCore
import bootstrapContractionLayout
from PIL import Image
import sys, os
from shutil import copyfile


class BootstrapContractionWindow(QtGui.QMainWindow, bootstrapContractionLayout.Ui_bootstrapContraction):
    def __init__(self, parent=None):
        super(BootstrapContractionWindow, self).__init__(parent)
        self.setupUi(self)

        self.fileName = 'ContractedGraph.png'
        self.lowQualFileName = os.path.splitext(self.fileName)[0] + '.lowQual.png'

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # bind export actions
        self.actionPNG.triggered.connect(lambda: self.exportFile(self.fileName))
        self.actionPDF.triggered.connect(lambda: self.exportFile(self.fileName))

    def display_image(self):
        # change background color to white
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(p)

        # creates a lower quality version of the heatmap to display
        image = Image.open(self.fileName)
        size = image.size
        image = image.resize((size[0] / 3, size[1] / 3), Image.ANTIALIAS)
        image.save(os.path.splitext(self.fileName)[0] + '.lowQual.png', 'PNG', quality=200)

        # positions the window relative to the top left corner of the screen (px)
        self.move(0, 600)

        # displays the lower quality version of the image
        self.bootstrapContractionPixmap = QtGui.QPixmap(self.lowQualFileName)
        self.bootstrapContractionImage.setScaledContents(False)
        self.bootstrapContractionImage.setPixmap(self.bootstrapContractionPixmap)

    def exportFile(self, fileName):
        """
                    input: fileName -- a string representing the name of the file to be saved

                    * pops up a window asking for an output path

                    output: saves file 'fileName' to new location inputted by the user
        """

        extension = os.path.splitext(fileName)[1]
        windowTitle = 'Export ' + extension[1:]
        name = QtGui.QFileDialog.getSaveFileName(self, windowTitle) + extension
        copyfile(fileName, name)

# if you want to test LOCALLY change the path to ../topologyDonut.png #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == '__main__':  # if we're running file directly and not importing it
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication

    # initialize main input window
    form = BootstrapContractionWindow()  # We set the form to be our PhyloVisApp (design)
    form.show()  # Show the form
    form.display_image()

    sys.exit(app.exec_())  # and execute the app
