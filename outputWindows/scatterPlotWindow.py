from PyQt4 import QtGui
import scatterPlotLayout


class ScatterPlotWindow(QtGui.QMainWindow, scatterPlotLayout.Ui_Form):
    def __init__(self, parent=None):
        super(ScatterPlotWindow, self).__init__(parent)
        self.setupUi(self)
        self.move(800,600)
