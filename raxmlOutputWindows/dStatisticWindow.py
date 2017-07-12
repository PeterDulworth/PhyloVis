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
    fileName = '../plots/WindowsToD.png'
else:
    fileName = 'plots/WindowsToD.png'


class DStatisticWindow(Window):
    def __init__(self):
        Window.__init__(self, fileName, x=120, y=142, scale=1)


if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = DStatisticWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())
