from standardWindow import Window
from PyQt4 import QtGui
import sys

"""
MS Robinson Foulds Window
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

class MSRobinsonFouldsWindow(Window):
    def __init__(self, title1, data1, title2, data2, xLabel1='', yLabel1='', xLabel2='', yLabel2='', groupLabels1=(), groupLabels2=()):
        Window.__init__(self)

        self.plotter.barPlot(title1, data1, xLabel=xLabel1, yLabel=yLabel1, groupLabels=groupLabels1, subplotPosition=211)
        self.plotter.barPlot(title2, data2, xLabel=xLabel2, yLabel=yLabel2, groupLabels=groupLabels2, subplotPosition=212)

        self.show()


if __name__ == '__main__': # only runs if not imported

    # create a new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    a = {0:0, 2:2, 4:3}

    # create window and plot
    form = MSRobinsonFouldsWindow(a)

    # execute the app
    sys.exit(app.exec_())
