from PyQt4 import QtGui, QtCore
import standardLayout
from PIL import Image
import sys, os
from shutil import copyfile


class Window(QtGui.QMainWindow, standardLayout.Ui_mainWindow):
    def __init__(self, fileName, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)

        self.fileName = fileName
        self.lowQualFileName = os.path.splitext(self.fileName)[0] + '.lowQual.png'

        # moves menu bar into application -- mac only windows sux
        self.menubar.setNativeMenuBar(False)

        # bind export actions
        self.actionPNG.triggered.connect(lambda: self.exportFile(self.fileName))
        self.actionPDF.triggered.connect(lambda: self.exportFile(self.fileName))

    def setBackgroundColor(self):
        """
            change background color to white
        """
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(p)

    def setImagePosition(self):
        """
            positions the window relative to the top left corner of the screen (px)
        """
        self.move(0, 0)

    def setImageQuality(self):
        """
            creates a lower quality version of the image to display
        """
        image = Image.open(self.fileName)
        size = image.size
        image = image.resize((size[0] / 3, size[1] / 3), Image.ANTIALIAS)
        image.save(os.path.splitext(self.fileName)[0] + '.lowQual.png', 'PNG', quality=200)

    def setImage(self):
        """
            displays the lower quality version of the image
        """
        self.imagePixmap = QtGui.QPixmap(self.lowQualFileName)
        self.image.setScaledContents(False)
        self.image.setPixmap(self.imagePixmap)

    def display_image(self):
        self.setBackgroundColor()
        self.setImageQuality()
        self.setImagePosition()
        self.setImage()

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

if __name__ == '__main__':
    """
        code is executed if file is run directly -- i.e. not imported
    """

    # A new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    # initialize main input window
    form = Window()
    form.show()
    form.display_image()

    # and execute the app
    sys.exit(app.exec_())

