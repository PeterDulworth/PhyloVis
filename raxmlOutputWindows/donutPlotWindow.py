from window import Window
from PyQt4 import QtGui
import sys

"""
Functions:
    __init__(self)
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

if __name__ == '__main__':
    fileName = '../plots/topologyDonut.png'
else:
    fileName = 'plots/topologyDonut.png'


class DonutPlotWindow(Window):
    def __init__(self):
        Window.__init__(self, fileName, x=200, y=222, scale=3) #!!! add ../ before file name to test locally


if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = DonutPlotWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())
