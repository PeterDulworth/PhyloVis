from PyQt4 import QtGui, QtCore
import standardLayout
from PIL import Image
import sys, os
from shutil import copyfile
import matplotlib
matplotlib.use('Qt4Agg')  # necessary for mac pls don't remove -- needs to be before pyplot is imported but after matplotlib is imported
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5 import SubplotToolQt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import random


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



class MplCanvas(FigureCanvas):
    def __init__(self, figure):
        self.fig = figure
        self.ax = self.fig.add_subplot(222)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class Window(QtGui.QMainWindow, standardLayout.Ui_mainWindow):
    def __init__(self, fileName, x=0, y=0, scale=1, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)

        self.fileName = fileName
        self.lowQualFileName = os.path.splitext(self.fileName)[0] + '.lowQual.png'
        self.x = x
        self.y = y
        self.scale = scale

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # set window title
        self.setWindowTitle(self.fileName)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.pushButton.clicked.connect(self.figureBarPlot)

        # fig = plt.figure()
        # fig.subplots_adjust(top=0.8)
        # ax1 = fig.add_subplot(211)
        # ax1.set_ylabel('volts')
        # ax1.set_title('a sine wave')

        # t = np.arange(0.0, 1.0, 0.01)
        # s = np.sin(2 * np.pi * t)
        # line, = ax1.plot(t, s, color='blue', lw=2)

        self.figureBarPlot([1, 2, 3, 4], 'henlo', 'henlo')

        # self.canvas = MplCanvas()
        # self.toolBar = NavigationToolbar(self.canvas, self)
        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.toolbar)

        # bind export actions
        self.actionPNG.triggered.connect(lambda: self.exportFile(self.fileName))
        self.actionPDF.triggered.connect(lambda: self.exportFile(self.fileName))

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

    def setImagePosition(self, x, y):
        """
            positions the window relative to the top left corner of the screen (px)
        """
        self.move(x, y)

    def setImageQuality(self, scale):
        """
            creates a lower quality version of the image to display
        """
        image = Image.open(self.fileName)
        size = image.size
        image = image.resize((int(size[0] / scale), int(size[1] / scale)), Image.ANTIALIAS)
        image.save(os.path.splitext(self.fileName)[0] + '.lowQual.png', 'PNG', quality=200)

    def setImage(self, fileName):
        """
            displays the lower quality version of the image
        """
        self.imagePixmap = QtGui.QPixmap(fileName)
        self.image.setScaledContents(False)
        self.image.setPixmap(self.imagePixmap)

    def displayImage(self):
        self.setBackgroundColor(QtCore.Qt.white)
        self.setImageQuality(self.scale)
        self.setImagePosition(self.x, self.y)
        self.setImage(self.lowQualFileName)

    def exportFile(self, fileName):
        """
            input: fileName -- a string representing the name of the file to be saved
            * pops up a window asking for an output path
            output: saves file 'fileName' to new location inputted by the user
        """

        extension = os.path.splitext(fileName)[1]
        windowTitle = 'Export ' + extension[1:]
        name = QtGui.QFileDialog.getSaveFileName(self, windowTitle) + extension
        copyfile(fileName, name)

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
    # form.displayImage()

    # and execute the app
    sys.exit(app.exec_())

