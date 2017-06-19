from PyQt4 import QtGui
import circleGraphLayout
from PIL import Image


class CircleGraphWindow(QtGui.QWidget, circleGraphLayout.Ui_circleGraph):
    def __init__(self, parent=None):
        super(CircleGraphWindow, self).__init__(parent)
        self.setupUi(self)

    def display_image(self):
        standardSize = Image.open("genomeAtlas.png").size

        self.move(0, 0)
        self.circleGraphImage.setScaledContents(True)
        self.circleGraphImage.setPixmap(QtGui.QPixmap("genomeAtlas.png"))
        self.resize(int(standardSize[0]), int(standardSize[1]))
