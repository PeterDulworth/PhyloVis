from window import Window
from PyQt4 import QtGui, QtCore
import donutPlotLayout
from PIL import Image
import sys, os
from shutil import copyfile


class DonutPlotWindow(Window):
    def __init__(self):
        Window.__init__(self, '../topologyDonut.png') #!!! add ../ before file name to test locally

    def setImagePosition(self):
        self.move(600, 600)

if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = DonutPlotWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())

