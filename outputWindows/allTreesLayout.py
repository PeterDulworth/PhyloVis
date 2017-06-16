# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'allTreesLayout.ui'
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

class Ui_allTrees(object):
    def setupUi(self, allTrees):
        allTrees.setObjectName(_fromUtf8("allTrees"))
        allTrees.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(allTrees)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.allTreesImage = QtGui.QLabel(allTrees)
        self.allTreesImage.setText(_fromUtf8(""))
        self.allTreesImage.setObjectName(_fromUtf8("allTreesImage"))
        self.horizontalLayout.addWidget(self.allTreesImage)

        self.retranslateUi(allTrees)
        QtCore.QMetaObject.connectSlotsByName(allTrees)

    def retranslateUi(self, allTrees):
        allTrees.setWindowTitle(_translate("allTrees", "All Trees", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    allTrees = QtGui.QWidget()
    ui = Ui_allTrees()
    ui.setupUi(allTrees)
    allTrees.show()
    sys.exit(app.exec_())

