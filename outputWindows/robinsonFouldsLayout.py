# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'robinsonFouldsLayout.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.unweightedTab = QtGui.QWidget()
        self.unweightedTab.setObjectName(_fromUtf8("unweightedTab"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.unweightedTab)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.robinsonFouldsUnweightedImage = QtGui.QLabel(self.unweightedTab)
        self.robinsonFouldsUnweightedImage.setText(_fromUtf8(""))
        self.robinsonFouldsUnweightedImage.setObjectName(_fromUtf8("robinsonFouldsUnweightedImage"))
        self.horizontalLayout_3.addWidget(self.robinsonFouldsUnweightedImage)
        self.tabWidget.addTab(self.unweightedTab, _fromUtf8(""))
        self.weightedTab = QtGui.QWidget()
        self.weightedTab.setObjectName(_fromUtf8("weightedTab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.weightedTab)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.robinsonFouldsWeightedImage = QtGui.QLabel(self.weightedTab)
        self.robinsonFouldsWeightedImage.setText(_fromUtf8(""))
        self.robinsonFouldsWeightedImage.setObjectName(_fromUtf8("robinsonFouldsWeightedImage"))
        self.horizontalLayout_2.addWidget(self.robinsonFouldsWeightedImage)
        self.tabWidget.addTab(self.weightedTab, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.unweightedTab), _translate("Form", "Unweighted", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.weightedTab), _translate("Form", "Weighted", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

