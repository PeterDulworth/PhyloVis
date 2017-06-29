from PyQt4 import QtGui, QtCore
import msRobinsonFouldsLayout
from PIL import Image
import sys, os
from shutil import copyfile


class MSRobinsonFouldsWindow(QtGui.QMainWindow, msRobinsonFouldsLayout.Ui_msRobinsonFoulds):
    def __init__(self, parent=None):
        super(MSRobinsonFouldsWindow, self).__init__(parent)
        self.setupUi(self)

        self.unweightedFileName = 'UWRFdifference.png'
        self.weightedFileName = 'WRFdifference.png'

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # bind export actions
        self.actionUnweightedPNG.triggered.connect(lambda: self.exportFile(self.unweightedFileName))
        self.actionUnweightedPDF.triggered.connect(lambda: self.exportFile(self.unweightedFileName))

        self.actionWeightedPNG.triggered.connect(lambda: self.exportFile(self.weightedFileName))
        self.actionWeightedPDF.triggered.connect(lambda: self.exportFile(self.weightedFileName))


    def displayImages(self):
        robinsonFouldsPlotSize = Image.open(self.weightedFileName).size

        self.move(900, 150)
        print self.pos()

        self.msRobinsonFouldsUnweightedImage.setScaledContents(True)
        self.msRobinsonFouldsUnweightedImage.setPixmap(QtGui.QPixmap(self.unweightedFileName))

        self.msRobinsonFouldsWeightedImage.setScaledContents(True)
        self.msRobinsonFouldsWeightedImage.setPixmap(QtGui.QPixmap(self.weightedFileName))

        self.resize(int(robinsonFouldsPlotSize[0]), int(robinsonFouldsPlotSize[1]))

    def exportFile(self, fileName):
        extension = os.path.splitext(fileName)[1]
        name = QtGui.QFileDialog.getSaveFileName(self, 'Export ' + extension[1:]) + extension
        copyfile(fileName, name)

    def toggleEnabled(self, object):
        enabled = object.isEnabled()
        object.setEnabled(not enabled)

    def moveEvent(self, QMoveEvent):
        print self.pos()

# if you want to test LOCALLY change the path to ../topologyDonut.png #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == '__main__':  # if we're running file directly and not importing it
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication

    # initialize main input window
    form = MSRobinsonFouldsWindow()  # We set the form to be our PhyloVisApp (design)
    form.show()  # Show the form
    form.displayWeightedAndUnweightedImages()

    sys.exit(app.exec_())  # and execute the app
