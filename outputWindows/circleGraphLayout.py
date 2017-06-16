# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'circleGraphLayout.ui'
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

class Ui_circleGraph(object):
    def setupUi(self, circleGraph):
        circleGraph.setObjectName(_fromUtf8("circleGraph"))
        circleGraph.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(circleGraph)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.circleGraphImage = QtGui.QLabel(circleGraph)
        self.circleGraphImage.setText(_fromUtf8(""))
        self.circleGraphImage.setObjectName(_fromUtf8("circleGraphImage"))
        self.horizontalLayout.addWidget(self.circleGraphImage)

        self.retranslateUi(circleGraph)
        QtCore.QMetaObject.connectSlotsByName(circleGraph)

    def retranslateUi(self, circleGraph):
        circleGraph.setWindowTitle(_translate("circleGraph", "Circle Track Graph", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    circleGraph = QtGui.QWidget()
    ui = Ui_circleGraph()
    ui.setupUi(circleGraph)
    circleGraph.show()
    sys.exit(app.exec_())

