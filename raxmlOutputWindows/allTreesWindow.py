from PyQt4 import QtGui, QtCore
import allTreesLayout
from PIL import Image
import sys, os
from shutil import copyfile


class AllTreesWindow(QtGui.QMainWindow, allTreesLayout.Ui_allTrees):
    def __init__(self, parent=None):
        super(AllTreesWindow, self).__init__(parent)
        self.setupUi(self)

        self.fileName = 'TopTopologies.png'
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
        self.move(800, 0)

        # displays the lower quality version of the image
        self.allTreesPixmap = QtGui.QPixmap(self.lowQualFileName)
        self.allTreesImage.setScaledContents(False)
        self.allTreesImage.setPixmap(self.allTreesPixmap)

    def exportFile(self, fileName):
        extension = os.path.splitext(fileName)[1]
        name = QtGui.QFileDialog.getSaveFileName(self, 'Export ' + extension[1:]) + extension
        copyfile(fileName, name)

# if you want to test LOCALLY change the path to ../Topology0.png #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == '__main__':  # if we're running file directly and not importing it
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication

    # initialize main input window
    form = AllTreesWindow()  # We set the form to be our PhyloVisApp (design)
    form.show()  # Show the form
    form.display_image()

    sys.exit(app.exec_())  # and execute the app