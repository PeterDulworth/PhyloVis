from PyQt4 import QtGui
import circleGraphLayout
from PIL import Image


class CircleGraphWindow(QtGui.QWidget, circleGraphLayout.Ui_Form):
    def __init__(self, parent=None):
        super(CircleGraphWindow, self).__init__(parent)
        self.setupUi(self)
        self.move(0,0)