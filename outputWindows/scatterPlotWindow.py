from PyQt4 import QtGui
import scatterPlotLayout
from PIL import Image


class ScatterPlotWindow(QtGui.QWidget, scatterPlotLayout.Ui_scatterPlot):
    def __init__(self, parent=None):
        super(ScatterPlotWindow, self).__init__(parent)
        self.setupUi(self)

    def display_image(self):
        standardSize = Image.open("topologyScatter.png").size

        self.move(800, 600)
        self.scatterPlotImage.setScaledContents(True)
        self.scatterPlotImage.setPixmap(QtGui.QPixmap("topologyScatter.png"))
        self.resize(int(standardSize[0]), int(standardSize[1]))
