# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'donutPlotLayout.ui'
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

class Ui_donutPlot(object):
    def setupUi(self, donutPlot):
        donutPlot.setObjectName(_fromUtf8("donutPlot"))
        donutPlot.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(donutPlot)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.donutPlotImage = QtGui.QLabel(donutPlot)
        self.donutPlotImage.setText(_fromUtf8(""))
        self.donutPlotImage.setObjectName(_fromUtf8("donutPlotImage"))
        self.horizontalLayout.addWidget(self.donutPlotImage)

        self.retranslateUi(donutPlot)
        QtCore.QMetaObject.connectSlotsByName(donutPlot)

    def retranslateUi(self, donutPlot):
        donutPlot.setWindowTitle(_translate("donutPlot", "Top Topologies Donut Plot", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    donutPlot = QtGui.QWidget()
    ui = Ui_donutPlot()
    ui.setupUi(donutPlot)
    donutPlot.show()
    sys.exit(app.exec_())

