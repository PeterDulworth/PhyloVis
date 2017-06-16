from PyQt4 import QtGui, QtCore
import pgtstLayout
from PIL import Image


class PGTSTWindow(QtGui.QWidget, pgtstLayout.Ui_Form):
    def __init__(self, parent=None):
        super(PGTSTWindow, self).__init__(parent)
        self.setupUi(self)

    def display_image(self):
        pgtstPlotSize = Image.open("PGTSTPlot.png").size

        self.move(1000, 0)
        self.pgtstImage.setScaledContents(True)
        self.pgtstImage.setPixmap(QtGui.QPixmap("PGTSTPlot.png"))
        self.resize(int(pgtstPlotSize[0]), int(pgtstPlotSize[1]))