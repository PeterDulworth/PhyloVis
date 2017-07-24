import sys
from standardWindow import Window
from PyQt4 import QtGui

"""
Functions:
    __init__(self)
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""


class ScatterPlotWindow(Window):
    def __init__(self):
        Window.__init__(self, windowTitle='Windows to Top Topologies', x=240, y=262, scale=1)

    def plot(self):
        self.plotter.figureBarPlot([1,2,3,4,5], 'bar plot', 111)


if __name__ == '__main__': # only runs if not imported

    # create a new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    # create window and plot
    form = ScatterPlotWindow()
    form.show()
    form.plot()

    # execute the app
    sys.exit(app.exec_())

