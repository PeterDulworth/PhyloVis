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


class DonutPlotWindow(Window):
    def __init__(self):
        Window.__init__(self, windowTitle='Top Topology Frequency Donut')


if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = DonutPlotWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())
