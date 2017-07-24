from standardWindow import Window
from PyQt4 import QtGui
import sys

"""
Informative Sites Heatmap
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""


class HeatMapWindow(Window):
    def __init__(self, title, sitesToInformative):
        Window.__init__(self, windowTitle='Informative Sites Heatmap')

        self.plotter.heatMap(title, sitesToInformative)
        self.show()

if __name__ == '__main__': # only runs if not imported

    # create a new instance of QApplication
    app = QtGui.QApplication(sys.argv)

    a = {0: '(C,(G,O),H);', 1: '((C,G),O,H);', 2: '(C,(G,O),H);', 3: '(C,(G,O),H);', 4: '(C,(G,O),H);', 5: '(C,(G,O),H);', 6: '(C,(G,O),H);', 7: '(C,(G,O),H);', 8: '((C,G),O,H);', 9: '(C,(G,O),H);'}

    # create window and plot
    form = HeatMapWindow()
    form.show()

    # execute the app
    sys.exit(app.exec_())

