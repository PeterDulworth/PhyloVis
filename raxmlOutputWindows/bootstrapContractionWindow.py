from standardWindow import Window
from PyQt4 import QtGui
import sys

"""
Bootstrap Contraction Window
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""


class BootstrapContractionWindow(Window):
    def __init__(self):
        Window.__init__(self, windowTitle='Bootstrap Contraction Window')


if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = BootstrapContractionWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())
