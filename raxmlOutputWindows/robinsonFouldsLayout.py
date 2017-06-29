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

class Ui_robinsonFoulds(object):
    def setupUi(self, robinsonFoulds):
        robinsonFoulds.setObjectName(_fromUtf8("robinsonFoulds"))
        robinsonFoulds.resize(359, 247)
        robinsonFoulds.setAutoFillBackground(True)
        self.centralwidget = QtGui.QWidget(robinsonFoulds)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
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
        robinsonFoulds.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(robinsonFoulds)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 359, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        self.menuUnweighted = QtGui.QMenu(self.menuExport)
        self.menuUnweighted.setObjectName(_fromUtf8("menuUnweighted"))
        self.menuWeighted = QtGui.QMenu(self.menuExport)
        self.menuWeighted.setObjectName(_fromUtf8("menuWeighted"))
        robinsonFoulds.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(robinsonFoulds)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        robinsonFoulds.setStatusBar(self.statusbar)
        self.actionPNG = QtGui.QAction(robinsonFoulds)
        self.actionPNG.setObjectName(_fromUtf8("actionPNG"))
        self.actionPDF = QtGui.QAction(robinsonFoulds)
        self.actionPDF.setObjectName(_fromUtf8("actionPDF"))
        self.actionUnweightedPNG = QtGui.QAction(robinsonFoulds)
        self.actionUnweightedPNG.setObjectName(_fromUtf8("actionUnweightedPNG"))
        self.actionWeightedPNG = QtGui.QAction(robinsonFoulds)
        self.actionWeightedPNG.setObjectName(_fromUtf8("actionWeightedPNG"))
        self.actionWeightedPDF = QtGui.QAction(robinsonFoulds)
        self.actionWeightedPDF.setObjectName(_fromUtf8("actionWeightedPDF"))
        self.actionUnweightedPDF = QtGui.QAction(robinsonFoulds)
        self.actionUnweightedPDF.setObjectName(_fromUtf8("actionUnweightedPDF"))
        self.menuUnweighted.addAction(self.actionUnweightedPNG)
        self.menuUnweighted.addAction(self.actionUnweightedPDF)
        self.menuWeighted.addAction(self.actionWeightedPNG)
        self.menuWeighted.addAction(self.actionWeightedPDF)
        self.menuExport.addAction(self.menuUnweighted.menuAction())
        self.menuExport.addAction(self.menuWeighted.menuAction())
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(robinsonFoulds)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(robinsonFoulds)

    def retranslateUi(self, robinsonFoulds):
        robinsonFoulds.setWindowTitle(_translate("robinsonFoulds", "Robinson Foulds", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.unweightedTab), _translate("robinsonFoulds", "Unweighted", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.weightedTab), _translate("robinsonFoulds", "Weighted", None))
        self.menuFile.setTitle(_translate("robinsonFoulds", "File", None))
        self.menuExport.setTitle(_translate("robinsonFoulds", "Export...", None))
        self.menuUnweighted.setTitle(_translate("robinsonFoulds", "Unweighted", None))
        self.menuWeighted.setTitle(_translate("robinsonFoulds", "Weighted", None))
        self.actionPNG.setText(_translate("robinsonFoulds", "PNG", None))
        self.actionPDF.setText(_translate("robinsonFoulds", "PDF", None))
        self.actionUnweightedPNG.setText(_translate("robinsonFoulds", "PNG", None))
        self.actionWeightedPNG.setText(_translate("robinsonFoulds", "PNG", None))
        self.actionWeightedPDF.setText(_translate("robinsonFoulds", "PDF", None))
        self.actionUnweightedPDF.setText(_translate("robinsonFoulds", "PDF", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    robinsonFoulds = QtGui.QMainWindow()
    ui = Ui_robinsonFoulds()
    ui.setupUi(robinsonFoulds)
    robinsonFoulds.show()
    sys.exit(app.exec_())

