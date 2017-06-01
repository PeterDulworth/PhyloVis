# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_layout.ui'
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

class Ui_PhylogeneticVisualization(object):
    def setupUi(self, PhylogeneticVisualization):
        PhylogeneticVisualization.setObjectName(_fromUtf8("PhylogeneticVisualization"))
        PhylogeneticVisualization.resize(433, 201)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PhylogeneticVisualization.sizePolicy().hasHeightForWidth())
        PhylogeneticVisualization.setSizePolicy(sizePolicy)
        PhylogeneticVisualization.setMinimumSize(QtCore.QSize(433, 201))
        self.centralwidget = QtGui.QWidget(PhylogeneticVisualization)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.inputFileBtn = QtGui.QPushButton(self.centralwidget)
        self.inputFileBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.inputFileBtn.setObjectName(_fromUtf8("inputFileBtn"))
        self.horizontalLayout_5.addWidget(self.inputFileBtn)
        self.inputFileEntry = QtGui.QLineEdit(self.centralwidget)
        self.inputFileEntry.setMinimumSize(QtCore.QSize(0, 21))
        self.inputFileEntry.setMouseTracking(True)
        self.inputFileEntry.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.inputFileEntry.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.inputFileEntry.setObjectName(_fromUtf8("inputFileEntry"))
        self.horizontalLayout_5.addWidget(self.inputFileEntry)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.windowSizeLabel = QtGui.QLabel(self.centralwidget)
        self.windowSizeLabel.setObjectName(_fromUtf8("windowSizeLabel"))
        self.horizontalLayout_3.addWidget(self.windowSizeLabel)
        self.windowSizeEntry = QtGui.QLineEdit(self.centralwidget)
        self.windowSizeEntry.setMinimumSize(QtCore.QSize(40, 21))
        self.windowSizeEntry.setMaximumSize(QtCore.QSize(80, 16777215))
        self.windowSizeEntry.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.windowSizeEntry.setObjectName(_fromUtf8("windowSizeEntry"))
        self.horizontalLayout_3.addWidget(self.windowSizeEntry)
        self.windowOffsetLabel = QtGui.QLabel(self.centralwidget)
        self.windowOffsetLabel.setObjectName(_fromUtf8("windowOffsetLabel"))
        self.horizontalLayout_3.addWidget(self.windowOffsetLabel)
        self.windowOffsetEntry = QtGui.QLineEdit(self.centralwidget)
        self.windowOffsetEntry.setMinimumSize(QtCore.QSize(40, 21))
        self.windowOffsetEntry.setMaximumSize(QtCore.QSize(80, 16777215))
        self.windowOffsetEntry.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.windowOffsetEntry.setObjectName(_fromUtf8("windowOffsetEntry"))
        self.horizontalLayout_3.addWidget(self.windowOffsetEntry)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.outputDirBtn = QtGui.QPushButton(self.centralwidget)
        self.outputDirBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.outputDirBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.outputDirBtn.setAcceptDrops(False)
        self.outputDirBtn.setAutoFillBackground(False)
        self.outputDirBtn.setObjectName(_fromUtf8("outputDirBtn"))
        self.horizontalLayout_4.addWidget(self.outputDirBtn)
        self.outputDirEntry = QtGui.QLineEdit(self.centralwidget)
        self.outputDirEntry.setMinimumSize(QtCore.QSize(0, 21))
        self.outputDirEntry.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.outputDirEntry.setObjectName(_fromUtf8("outputDirEntry"))
        self.horizontalLayout_4.addWidget(self.outputDirEntry)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.runBtn = QtGui.QPushButton(self.centralwidget)
        self.runBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.runBtn.setObjectName(_fromUtf8("runBtn"))
        self.horizontalLayout_6.addWidget(self.runBtn)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout_6.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        PhylogeneticVisualization.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PhylogeneticVisualization)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 433, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        PhylogeneticVisualization.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PhylogeneticVisualization)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PhylogeneticVisualization.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(PhylogeneticVisualization)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_As = QtGui.QAction(PhylogeneticVisualization)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(PhylogeneticVisualization)
        QtCore.QMetaObject.connectSlotsByName(PhylogeneticVisualization)

    def retranslateUi(self, PhylogeneticVisualization):
        PhylogeneticVisualization.setWindowTitle(_translate("PhylogeneticVisualization", "Phylogenetic Visualization", None))
        self.inputFileBtn.setText(_translate("PhylogeneticVisualization", "Select Input File", None))
        self.windowSizeLabel.setText(_translate("PhylogeneticVisualization", "Window Size:", None))
        self.windowOffsetLabel.setText(_translate("PhylogeneticVisualization", "Window Offset:", None))
        self.outputDirBtn.setText(_translate("PhylogeneticVisualization", "Select Output Directory", None))
        self.runBtn.setText(_translate("PhylogeneticVisualization", "Run", None))
        self.menuFile.setTitle(_translate("PhylogeneticVisualization", "File", None))
        self.actionSave.setText(_translate("PhylogeneticVisualization", "Save", None))
        self.actionSave_As.setText(_translate("PhylogeneticVisualization", "Save As", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PhylogeneticVisualization = QtGui.QMainWindow()
    ui = Ui_PhylogeneticVisualization()
    ui.setupUi(PhylogeneticVisualization)
    PhylogeneticVisualization.show()
    sys.exit(app.exec_())

