from PyQt4 import QtGui, QtCore
import tabLayout
from PIL import Image
import sys, os
from shutil import copyfile

class TabWindow(QtGui.QMainWindow, tabLayout.Ui_tabLayout):
    def __init__(self, unweightedFileName, weightedFileName, x=0, y=0, scale=1, parent=None):
        super(TabWindow, self).__init__(parent)
        self.setupUi(self)

        self.unweightedFileName = unweightedFileName
        self.weightedFileName = weightedFileName
        self.lowQualUnweightedFileName = os.path.splitext(self.unweightedFileName)[0] + '.lowQual.png'
        self.lowQualWeightedFileName = os.path.splitext(self.weightedFileName)[0] + '.lowQual.png'
        self.x = x
        self.y = y
        self.scale = scale

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # set window title
        self.setWindowTitle(self.unweightedFileName)

        # bind export actions
        self.actionUnweightedPNG.triggered.connect(lambda: self.exportFile(self.unweightedFileName))
        self.actionUnweightedPDF.triggered.connect(lambda: self.exportFile(self.unweightedFileName))

        self.actionWeightedPNG.triggered.connect(lambda: self.exportFile(self.weightedFileName))
        self.actionWeightedPDF.triggered.connect(lambda: self.exportFile(self.weightedFileName))

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

    def setImageQuality(self, fileName, scale):
        """
            creates a lower quality version of the image to display
        """
        image = Image.open(fileName)
        size = image.size
        image = image.resize((int(size[0] / scale), int(size[1] / scale)), Image.ANTIALIAS)
        image.save(os.path.splitext(fileName)[0] + '.lowQual.png', 'PNG', quality=200)

    def setImage(self, fileName, image):
        """
            displays the lower quality version of the image
        """
        self.imagePixmap = QtGui.QPixmap(fileName)
        image.setScaledContents(False)
        image.setPixmap(self.imagePixmap)

    def displayImages(self):
        self.setBackgroundColor(QtCore.Qt.white)
        self.setImageQuality(self.unweightedFileName, self.scale)
        self.setImageQuality(self.weightedFileName, self.scale)
        self.setWindowPosition(self.x, self.y)
        self.setImage(self.lowQualUnweightedFileName, self.unweightedImage)
        self.setImage(self.lowQualWeightedFileName, self.weightedImage)

    def displayUnweightedImage(self):
        self.setBackgroundColor(QtCore.Qt.white)
        self.actionWeightedPNG.setEnabled(False)
        self.actionWeightedPDF.setEnabled(False)

        self.setImageQuality(self.unweightedFileName, self.scale)
        self.setWindowPosition(self.x, self.y)
        self.setImage(self.lowQualUnweightedFileName, self.unweightedImage)

        self.tabWidget.removeTab(1)

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

if __name__ == '__main__':
    """
        code is executed if file is run directly -- i.e. not imported
    """

    # A new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    # initialize main input window
    form = TabWindow()
    form.show()
    form.display_image()

    # and execute the app
    sys.exit(app.exec_())

