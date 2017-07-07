from window import Window
from PyQt4 import QtGui
import sys


if __name__ == '__main__':
    fileName = '../plots/PGTSTPlot.png'
else:
    fileName = 'plots/PGTSTPlot.png'


class PGTSTWindow(Window):
    def __init__(self):
        Window.__init__(self, fileName, x=160, y=182, scale=1)

if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = PGTSTWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())