import sys, os
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')  # necessary for mac pls don't remove -- needs to be before pyplot is imported but after matplotlib is imported
from matplotlib import pyplot as plt
from matplotlibCustomBackend.customToolbar import CustomToolbar
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.qt_compat import QtCore, QtGui


class Window(QtGui.QMainWindow):
    def __init__(self, windowTitle='Window', x=0, y=0, scale=1, parent=None):
        super(Window, self).__init__(parent)

        self.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(0)
        self.setCentralWidget(self.centralwidget)

        # menubar
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 340, 22))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.actionPNG = QtGui.QAction(self)
        self.actionPDF = QtGui.QAction(self)
        self.actionSaveAs = QtGui.QAction(self)
        self.menuFile.addAction(self.actionSaveAs)
        self.menubar.addAction(self.menuFile.menuAction())

        self.menuFile.setTitle("File")
        self.actionSaveAs.setText("Save As...")

        QtCore.QMetaObject.connectSlotsByName(self)

        self.windowTitle = windowTitle
        self.x = x
        self.y = y
        self.scale = scale

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # set window title
        self.setWindowTitle(self.windowTitle)

        self.initCanvas()

        self.toolbar = CustomToolbar(self.canvas, self)
        self.verticalLayout.addWidget(self.toolbar)

        # bind export actions
        self.actionSaveAs.triggered.connect(self.toolbar.save_figure)

    def initCanvas(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.verticalLayout.addWidget(self.canvas)

    def figureBarPlot(self, data, name, title):
        """
            generates bar chart
        """

        # create a new subplot in a 1x1 coordinate system at position 1
        ax = plt.subplot(111)
        ax.set_title(title)
        numberOfBars = len(data)
        ind = np.arange(numberOfBars)  # the x locations for the groups
        width = .667  # the width of the bars
        colors = [(43.0 / 255.0, 130.0 / 255.0, 188.0 / 255.0), (141.0 / 255.0, 186.0 / 255.0, 87.0 / 255.0), (26.0 / 255.0, 168.0 / 255.0, 192.0 / 255.0), (83.5 / 255.0, 116.5 / 255.0, 44.5 / 255.0)]

        ax.bar(ind, data, width, color=colors)

    def plot(self):
        pass

    def setBackgroundColor(self, color):
        """
            change background color to white
        """
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

    def setWindowPosition(self, x, y):
        """
            positions the window relative to the top left corner of the screen (px)
        """
        self.move(x, y)

    def setWindowSize(self, x, y):
        """
            sets size of window
        """
        self.resize(x, y)

    def closeEvent(self, QCloseEvent):
        self.emit(QtCore.SIGNAL("WINDOW_CLOSED"))

        # def moveEvent(self, QMoveEvent):
        #     print self.fileName, self.pos()


if __name__ == '__main__':
    """
        code is executed if file is run directly -- i.e. not imported
    """

    # A new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    # initialize main input window
    form = Window(windowTitle='Standard Window', scale=5)
    form.show()
    form.setWindowSize(600, 600)
    form.figureBarPlot([1, 2, 3, 4], 'henlo', 'henlo')
    form.setBackgroundColor(QtCore.Qt.white)

    # and execute the app
    sys.exit(app.exec_())
