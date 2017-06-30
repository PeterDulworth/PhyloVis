from window import Window
from PyQt4 import QtGui
import sys


if __name__ == '__main__':
    fileName = '../plots/genomeAtlas.png'
else:
    fileName = 'plots/genomeAtlas.png'


class CircleGraphWindow(Window):
    def __init__(self):
        Window.__init__(self, fileName, x=80, y=102, scale=1)


if __name__ == '__main__':
    # test window if running locally
    app = QtGui.QApplication(sys.argv)
    form = CircleGraphWindow()
    form.show()
    form.display_image()
    sys.exit(app.exec_())