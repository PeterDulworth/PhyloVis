from standardWindow import Window
from PyQt4 import QtGui
import sys

"""
    P(gene tree | species tree)
    ~
    Chabrielle Allen
    Travis Benedict
Peter Dulworth
"""


class PGTSTWindow(Window):
    def __init__(self):
        Window.__init__(self, windowTitle='P(gene tree | species tree)')


if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = PGTSTWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())
