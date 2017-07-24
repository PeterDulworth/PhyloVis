from standardWindow import Window
from PyQt4 import QtGui
import sys

"""
    P(gene tree | species tree)
    ~
    Chabrielle Allen
    Travis Benedict
Peter Dulworth
"""


class PGTSTWindow(Window):
    def __init__(self, windowsToPGTST, title, xLabel='', yLabel=''):
        Window.__init__(self, windowTitle='P(gene tree | species tree)')

        self.plotter.stat_scatter(windowsToPGTST, title, xLabel, yLabel)
        self.show()


if __name__ == '__main__': # only runs if not imported

    # create a new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    a = ['8', '2']
    b = [80.0, 20.0]
    c = ['#ff0000', '#0000ff']

    # create window and plot
    form = PGTSTWindow(windowsToPGTST, "p(gt|st)", "Windows", "Probability")
    form.show()
    form.plot()

    # execute the app
    sys.exit(app.exec_())
