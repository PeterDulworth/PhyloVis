import sys, os
from module import plotter
import matplotlib
matplotlib.use('Qt4Agg')  # necessary for mac pls don't remove -- needs to be before pyplot is imported but after matplotlib is imported
from matplotlib import pyplot as plt
from matplotlibCustomBackend.customToolbar import CustomToolbar
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.qt_compat import QtCore, QtGui


class Window(QtGui.QMainWindow):
    def __init__(self, windowTitle='Window', x=0, y=0, parent=None):
        super(Window, self).__init__(parent)

        # layout
        self.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(0)
        self.setCentralWidget(self.centralwidget)
        self.setBackgroundColor(QtCore.Qt.white)

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

        # get arguments
        self.windowTitle = windowTitle

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # set window title
        self.setWindowTitle(self.windowTitle)

        self.initCanvas()

        self.toolbar = CustomToolbar(self.canvas, self)
        self.verticalLayout.addWidget(self.toolbar)

        self.setWindowPosition(x, y)

        # bind export actions
        self.actionSaveAs.triggered.connect(self.toolbar.save_figure)

        # create instance of Plotter class
        self.plotter = plotter.Plotter()

    def initCanvas(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.verticalLayout.addWidget(self.canvas)

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
    form = Window(windowTitle='Standard Window')
    form.show()
    form.setWindowSize(600, 600)

    # and execute the app
    sys.exit(app.exec_())
