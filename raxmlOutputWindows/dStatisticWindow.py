from standardWindow import Window
from PyQt4 import QtGui
import sys

"""
D-Statistic Window
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

class DStatisticWindow(Window):
    def __init__(self):
        Window.__init__(self, windowTitle='D-Statistic Window')


if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = DStatisticWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())
