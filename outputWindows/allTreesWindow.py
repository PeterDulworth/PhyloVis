from PyQt4 import QtGui, QtCore
import allTreesLayout
from PIL import Image


class AllTreesWindow(QtGui.QWidget, allTreesLayout.Ui_Form):
    def __init__(self, parent=None):
        super(AllTreesWindow, self).__init__(parent)
        self.setupUi(self)

        standardSize = Image.open("Topology0.png").size

        self.move(800, 0)
        self.allTreesImage.setScaledContents(True)
        self.allTreesImage.setPixmap(QtGui.QPixmap("Topology0.png"))
        self.resize(int(standardSize[0]), int(standardSize[1]))