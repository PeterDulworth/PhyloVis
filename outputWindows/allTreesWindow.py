from PyQt4 import QtGui, QtCore
import allTreesLayout


class AllTreesWindow(QtGui.QWidget, allTreesLayout.Ui_Form):
    def __init__(self, parent=None):
        super(AllTreesWindow, self).__init__(parent)
        self.setupUi(self)
        self.move(0,0)