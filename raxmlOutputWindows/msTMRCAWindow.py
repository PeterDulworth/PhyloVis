from standardWindow import Window
from PyQt4 import QtGui
import sys

"""
MS TMRCA Window
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

class MSTMRCAWindow(Window):
    def __init__(self, title1, data1, title2, data2, xLabel1='', yLabel1='', xLabel2='', yLabel2='', groupLabels1=(), groupLabels2=()):
        Window.__init__(self)

        self.show()


if __name__ == '__main__': # only runs if not imported

    # create a new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    a = {0:0, 2:2, 4:3}

    # create window and plot
    form = MSTMRCAWindow(a)

    # execute the app
    sys.exit(app.exec_())
