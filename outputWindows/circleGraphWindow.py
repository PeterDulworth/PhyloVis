from PyQt4 import QtGui
import circleGraphLayout


class CircleGraphWindow(QtGui.QMainWindow, circleGraphLayout.Ui_Form):
    def __init__(self, parent=None):
        super(CircleGraphWindow, self).__init__(parent)
        self.setupUi(self)
