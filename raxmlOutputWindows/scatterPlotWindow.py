import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent dir to path
from standardWindow import Window
import matplotlib
matplotlib.use('Qt4Agg')  # necessary for mac pls don't remove -- needs to be before pyplot is imported but after matplotlib is imported
from matplotlib import pyplot as plt
from PyQt4 import QtGui, QtCore
from module import plotter
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
        Window.__init__(self, 'asdf', x=240, y=262, scale=1)


    def plot(self):
        windows_to_w_rf = {0:0, 1:1, 2:2, 3:3, 4:4}
        self.plotter = plotter.Plotter()
        plot = self.plotter.stat_scatter(windows_to_w_rf, "plots/WeightedFouldsPlot.png", "Weighted Robinson-Foulds Distance", "Windows", "RF Distance")
        plot = self.plotter.figureBarPlot([1,2,3,4,5], '', '')
        print plot



    def figureBarPlot(self, data, name, title):
        """
            generates bar chart
        """

        numberOfBars = len(data)
        ind = np.arange(numberOfBars)  # the x locations for the groups
        width = .667  # the width of the bars
        ax = self.figure.add_subplot(111)
        colors = [(43.0 / 255.0, 130.0 / 255.0, 188.0 / 255.0), (141.0 / 255.0, 186.0 / 255.0, 87.0 / 255.0), (26.0 / 255.0, 168.0 / 255.0, 192.0 / 255.0), (83.5 / 255.0, 116.5 / 255.0, 44.5 / 255.0)]

        ax.bar(ind, data, width, color=colors)

        plt.title(title, fontsize=15)
        # plt.savefig(name)
        # plt.show()

        self.canvas.draw()

if __name__ == '__main__': # test window if running locally

    # A new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    # initialize main input window
    form = ScatterPlotWindow()
    form.show()
    form.setWindowSize(600, 600)
    form.plot()
    form.setBackgroundColor(QtCore.Qt.white)

    # and execute the app
    sys.exit(app.exec_())

