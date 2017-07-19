from PyQt4 import QtGui, QtCore
import standardLayout
import sys, os
import matplotlib
matplotlib.use('Qt4Agg')  # necessary for mac pls don't remove -- needs to be before pyplot is imported but after matplotlib is imported
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5 import SubplotToolQt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np


# class CustomToolbar(NavigationToolbar):
#     def __init__(self, canvas_, parent_):
#         self.toolitems = (
#             ('Home', 'Lorem ipsum dolor sit amet', 'home', 'home'),
#             ('Back', 'consectetuer adipiscing elit', 'back', 'back'),
#             ('Forward', 'sed diam nonummy nibh euismod', 'forward', 'forward'),
#             (None, None, None, None),
#             ('Pan', 'tincidunt ut laoreet', 'move', 'pan'),
#             ('Zoom', 'dolore magna aliquam', 'zoom_to_rect', 'zoom'),
#             (None, None, None, None),
#             ('Subplots', 'putamus parum claram', 'subplots', 'configure_subplots'),
#             ('Save', 'sollemnes in futurum', 'filesave', 'save_figure'),
#             ('Custom Button', 'custom btn hover txt', 'warning', 'configure_subplots'),
#             )
#         # self.toolitems = [t for t in self.toolitems if
#         #              t[0] in ('Home', 'Pan', 'Zoom', 'Save')]
#         NavigationToolbar.__init__(self, canvas_, parent_)
#
#     def _icon(self, name):
#         print name
#         pm = QtGui.QPixmap(os.path.join(self.basedir, name))
#         if hasattr(pm, 'setDevicePixelRatio'):
#             pm.setDevicePixelRatio(self.canvas._dpi_ratio)
#         return QtGui.QIcon(pm)
#
#     def pan(self):
#         NavigationToolbar.pan(self)
#         self.mode = "henlo!"  # <--- whatever you want to replace "pan/zoom" goes here
#         self.set_message(self.mode)


class Window(QtGui.QMainWindow):
    def __init__(self, fileName, x=0, y=0, scale=1, parent=None):
        super(Window, self).__init__(parent)

        # self.setObjectName("self")
        self.resize(340, 286)
        self.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.setCentralWidget(self.centralwidget)

        # menubar
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 340, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.setMenuBar(self.menubar)
        self.actionPNG = QtGui.QAction(self)
        self.actionPNG.setObjectName("actionPNG")
        self.actionPDF = QtGui.QAction(self)
        self.actionPDF.setObjectName("actionPDF")
        self.actionSaveAs = QtGui.QAction(self)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.menuFile.addAction(self.actionSaveAs)
        self.menubar.addAction(self.menuFile.menuAction())

        self.setWindowTitle("Main Window")
        self.menuFile.setTitle("File")
        self.actionSaveAs.setText("Save As...")

        QtCore.QMetaObject.connectSlotsByName(self)

        self.fileName = fileName
        self.x = x
        self.y = y
        self.scale = scale

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # set window title
        self.setWindowTitle(self.fileName)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.toolbar)

        # bind export actions
        self.actionSaveAs.triggered.connect(self.toolbar.save_figure)

    def box(self):
        dia = SubplotToolQt(self.canvas.figure, self.parent)
        # dia.setWindowIcon(QtGui.QIcon(image))
        dia.exec_()

    def figureBarPlot(self, data, name, title):
        """
            generates bar chart
        """


        numberOfBars = len(data)
        ind = np.arange(numberOfBars)  # the x locations for the groups
        width = .667  # the width of the bars
        ax = self.figure.add_subplot(111)
        colors = [(43.0/255.0, 130.0/255.0, 188.0/255.0), (141.0/255.0, 186.0/255.0, 87.0/255.0), (26.0/255.0, 168.0/255.0, 192.0/255.0), (83.5/255.0, 116.5/255.0, 44.5/255.0)]

        ax.bar(ind, data, width, color=colors)

        plt.title(title, fontsize=15)
        # plt.savefig(name)
        # plt.show()

        self.canvas.draw()

    def plot(self):
        ''' plot some random stuff '''
        # random data
        # data = [random.random() for i in range(10)]

        # create an axis
        # ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False)

        # plot data
        # ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

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
    form = Window('../imgs/tree.png', scale=5)
    form.show()
    form.setWindowSize(600,600)
    form.figureBarPlot([1, 2, 3, 4], 'henlo', 'henlo')
    form.setBackgroundColor(QtCore.Qt.white)

    # and execute the app
    sys.exit(app.exec_())

