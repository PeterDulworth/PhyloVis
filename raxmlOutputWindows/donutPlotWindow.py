from standardWindow import Window
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


class DonutPlotWindow(Window):
    def __init__(self, labels, sizes, donutColors):
        Window.__init__(self, windowTitle='Top Topology Frequency Donut')

        self.labels = labels
        self.sizes = sizes
        self.donutColors = donutColors

    def plot(self):
        self.plotter.topologyDonut('title', self.labels, self.sizes, self.donutColors)

if __name__ == '__main__': # only runs if not imported

    # create a new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    a = ['8', '2']
    b = [80.0, 20.0]
    c = ['#ff0000', '#0000ff']

    # create window and plot
    form = DonutPlotWindow(a, b, c)
    form.show()
    form.plot()

    # execute the app
    sys.exit(app.exec_())
