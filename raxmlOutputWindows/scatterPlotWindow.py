import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent dir to path
from standardWindow import Window
import matplotlib
matplotlib.use('Qt4Agg')  # necessary for mac pls don't remove -- needs to be before pyplot is imported but after matplotlib is imported
from matplotlib import pyplot as plt
from PyQt4 import QtGui, QtCore
import numpy as np

"""
Functions:
    __init__(self)
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

if __name__ == '__main__':
    fileName = '../plots/topologyScatter.png'
else:
    fileName = 'plots/topologyScatter.png'


class ScatterPlotWindow(Window):
    def __init__(self):
        Window.__init__(self, windowTitle='Windows to Top Topologies', x=240, y=262, scale=1)

    def plot(self):
        self.plotter.figureBarPlot([1,2,3,4,5], 'bar plot', 111)


if __name__ == '__main__': # test window if running locally

    # A new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    # initialize main input window
    form = ScatterPlotWindow()
    form.show()
    form.plot()
    form.setBackgroundColor(QtCore.Qt.white)

    # and execute the app
    sys.exit(app.exec_())

