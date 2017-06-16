from PyQt4 import QtGui, QtCore
import robinsonFouldsLayout
from PIL import Image


class RobinsonFouldsWindow(QtGui.QWidget, robinsonFouldsLayout.Ui_robinsonFoulds):
    def __init__(self, parent=None):
        super(RobinsonFouldsWindow, self).__init__(parent)
        self.setupUi(self)

    def displayUnweightedImage(self):
        robinsonFouldsPlotSize = Image.open("UnweightedFouldsPlot.png").size

        self.move(1000, 600)

        self.robinsonFouldsUnweightedImage.setScaledContents(True)
        self.robinsonFouldsUnweightedImage.setPixmap(QtGui.QPixmap("UnweightedFouldsPlot.png"))

        self.tabWidget.removeTab(1)
        self.resize(int(robinsonFouldsPlotSize[0]), int(robinsonFouldsPlotSize[1]))

    def displayWeightedAndUnweightedImages(self):
        robinsonFouldsPlotSize = Image.open("WeightedFouldsPlot.png").size

        self.move(1000, 600)

        self.robinsonFouldsUnweightedImage.setScaledContents(True)
        self.robinsonFouldsUnweightedImage.setPixmap(QtGui.QPixmap("UnweightedFouldsPlot.png"))

        self.robinsonFouldsWeightedImage.setScaledContents(True)
        self.robinsonFouldsWeightedImage.setPixmap(QtGui.QPixmap("WeightedFouldsPlot.png"))

        self.resize(int(robinsonFouldsPlotSize[0]), int(robinsonFouldsPlotSize[1]))