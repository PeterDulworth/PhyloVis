from standardWindow import Window
from PyQt4 import QtGui
import sys
import matplotlib
matplotlib.use('Qt4Agg')  # necessary for mac pls don't remove -- needs to be before pyplot is imported but after matplotlib is imported
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

"""
All Trees Window
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""


class AllTreesWindow(Window):
    def __init__(self, title, colorScheme, rooted=False, outGroup=False):
        Window.__init__(self, windowTitle='All Trees Window')

        self.plotter.topologyColorizer(title, colorScheme, rooted=rooted, outgroup=outGroup)
        self.show()

    def initCanvas(self):
        plt.axis('off')
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.verticalLayout.addWidget(self.canvas)


if __name__ == '__main__': # only runs if not imported

    # create a new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    a = {'((C,G),O,H);': '#0000ff', '(C,(G,O),H);': '#ff0000', '((C,G),(O,H));': '#00ff00'}

    # create window and plot
    form = AllTreesWindow('', a, rooted=False, outGroup=False)
    form.show()
    form.plot()

    # execute the app
    sys.exit(app.exec_())
