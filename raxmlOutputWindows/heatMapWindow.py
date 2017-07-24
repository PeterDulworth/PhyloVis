from standardWindow import Window
from PyQt4 import QtGui
import sys

"""
Informative Sites Heatmap
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""


class HeatMapWindow(Window):
    def __init__(self):
        Window.__init__(self, windowTitle='Informative Sites Heatmap')


if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = HeatMapWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())
