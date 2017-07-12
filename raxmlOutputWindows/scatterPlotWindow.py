from standardWindow import Window
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
    fileName = '../plots/topologyScatter.png'
else:
    fileName = 'plots/topologyScatter.png'


class ScatterPlotWindow(Window):
    def __init__(self):
        Window.__init__(self, fileName, x=240, y=262, scale=1)


if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = ScatterPlotWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())
