from window import Window
from PyQt4 import QtGui
import sys


if __name__ == '__main__':
    fileName = '../TopTopologies.png'
else:
    fileName = 'TopTopologies.png'


class AllTreesWindow(Window):
    def __init__(self):
        Window.__init__(self, fileName, x=0, y=22, scale=3)

if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = AllTreesWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())