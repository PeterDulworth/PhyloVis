# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pgtstLayout.ui'
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

class Ui_pgtst(object):
    def setupUi(self, pgtst):
        pgtst.setObjectName(_fromUtf8("pgtst"))
        pgtst.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(pgtst)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pgtstImage = QtGui.QLabel(pgtst)
        self.pgtstImage.setText(_fromUtf8(""))
        self.pgtstImage.setObjectName(_fromUtf8("pgtstImage"))
        self.horizontalLayout.addWidget(self.pgtstImage)

        self.retranslateUi(pgtst)
        QtCore.QMetaObject.connectSlotsByName(pgtst)

    def retranslateUi(self, pgtst):
        pgtst.setWindowTitle(_translate("pgtst", "P(GT | ST)", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    pgtst = QtGui.QWidget()
    ui = Ui_pgtst()
    ui.setupUi(pgtst)
    pgtst.show()
    sys.exit(app.exec_())

