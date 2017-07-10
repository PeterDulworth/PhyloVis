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
    fileName = '../plots/ContractedGraph.png'
else:
    fileName = 'plots/ContractedGraph.png'


class BootstrapContractionWindow(Window):
    def __init__(self):
        Window.__init__(self, fileName, x=40, y=62, scale=3)


if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = BootstrapContractionWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())
