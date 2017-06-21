from PyQt4 import QtGui, QtCore
import donutPlotLayout
from PIL import Image
import sys, os
from shutil import copyfile


class DonutPlotWindow(QtGui.QMainWindow, donutPlotLayout.Ui_donutPlot):
    def __init__(self, parent=None):
        super(DonutPlotWindow, self).__init__(parent)
        self.setupUi(self)

        self.fileName = 'topologyDonut.png'

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # bind export actions
        self.actionPNG.triggered.connect(lambda: self.exportFile(self.fileName))
        self.actionPDF.triggered.connect(lambda: self.exportFile(self.fileName))

    def display_image(self):
        # image = Image.open('../topologyDonut.png')
        # size = image.size
        # image = image.resize((size[0]/2, size[1]/2), Image.ANTIALIAS)
        # print size
        # image.save('../test.png', 'PNG', quality=200)

        # change background color to white
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(p)

        # get size of image

        self.move(0, 600)
        self.donutPixmap = QtGui.QPixmap(self.fileName).scaled(600, 600, QtCore.Qt.KeepAspectRatio)
        self.donutPlotImage.setScaledContents(False)
        self.donutPlotImage.setPixmap(self.donutPixmap)

    def exportFile(self, fileName):
        extension = os.path.splitext(fileName)[1]
        name = QtGui.QFileDialog.getSaveFileName(self, 'Export ' + extension[1:]) + extension
        copyfile(fileName, name)

# if you want to test LOCALLY change the path to ../topologyDonut.png #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == '__main__':  # if we're running file directly and not importing it
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication

    # initialize main input window
    form = DonutPlotWindow()  # We set the form to be our PhyloVisApp (design)
    form.show()  # Show the form
    form.display_image()

    sys.exit(app.exec_())  # and execute the app
