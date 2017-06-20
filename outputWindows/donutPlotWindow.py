from PyQt4 import QtGui, QtCore
import donutPlotLayout
import sys


class DonutPlotWindow(QtGui.QWidget, donutPlotLayout.Ui_donutPlot):
    def __init__(self, parent=None):
        super(DonutPlotWindow, self).__init__(parent)
        self.setupUi(self)

    def display_image(self):
        self.move(0, 600)
        self.donutPixmap = QtGui.QPixmap("topologyDonut.png").scaled(800, 800, QtCore.Qt.KeepAspectRatio)
        self.donutPlotImage.setScaledContents(False)
        self.donutPlotImage.setPixmap(self.donutPixmap)

# if you want to test LOCALLY change the path to ../topologyDonut.png #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == '__main__':  # if we're running file directly and not importing it
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication

    # initialize main input window
    form = DonutPlotWindow()  # We set the form to be our PhyloVisApp (design)
    form.show()  # Show the form
    form.display_image()

    sys.exit(app.exec_())  # and execute the app
