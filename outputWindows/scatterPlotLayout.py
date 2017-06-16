# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scatterPlotLayout.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_scatterPlot(object):
    def setupUi(self, scatterPlot):
        scatterPlot.setObjectName(_fromUtf8("scatterPlot"))
        scatterPlot.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(scatterPlot)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.scatterPlotImage = QtGui.QLabel(scatterPlot)
        self.scatterPlotImage.setText(_fromUtf8(""))
        self.scatterPlotImage.setObjectName(_fromUtf8("scatterPlotImage"))
        self.horizontalLayout.addWidget(self.scatterPlotImage)

        self.retranslateUi(scatterPlot)
        QtCore.QMetaObject.connectSlotsByName(scatterPlot)

    def retranslateUi(self, scatterPlot):
        scatterPlot.setWindowTitle(_translate("scatterPlot", "Scatter Plot", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    scatterPlot = QtGui.QWidget()
    ui = Ui_scatterPlot()
    ui.setupUi(scatterPlot)
    scatterPlot.show()
    sys.exit(app.exec_())

