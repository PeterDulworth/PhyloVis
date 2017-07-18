from PyQt4 import QtGui, QtCore
import standardLayout
from PIL import Image
import sys, os
from shutil import copyfile
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
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

        self.canvas = MplCanvas()
        self.toolBar = NavigationToolbar(self.canvas, self)
        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.toolBar)

        # bind export actions
        self.actionPNG.triggered.connect(lambda: self.exportFile(self.fileName))
        self.actionPDF.triggered.connect(lambda: self.exportFile(self.fileName))



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
    form.displayImage()

    # and execute the app
    sys.exit(app.exec_())

