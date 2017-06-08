from PyQt4 import QtGui
import donutPlotLayout


class DonutPlotWindow(QtGui.QMainWindow, donutPlotLayout.Ui_Form):
    def __init__(self, parent=None):
        super(DonutPlotWindow, self).__init__(parent)
        self.setupUi(self)
