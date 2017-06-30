from window import Window
from PyQt4 import QtGui
import sys


if __name__ == '__main__':
    fileName = '../plots/HeatMapInfSites.png'
else:
    fileName = 'plots/HeatMapInfSites.png'


class HeatMapWindow(Window):
    def __init__(self):
        Window.__init__(self, fileName, x=120, y=142, scale=3)


if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = HeatMapWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())