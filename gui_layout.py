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
        PhylogeneticVisualization.resize(581, 432)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PhylogeneticVisualization.sizePolicy().hasHeightForWidth())
        PhylogeneticVisualization.setSizePolicy(sizePolicy)
        PhylogeneticVisualization.setMinimumSize(QtCore.QSize(433, 201))
        self.centralwidget = QtGui.QWidget(PhylogeneticVisualization)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.inputMainHorizontalLayout = QtGui.QHBoxLayout()
        self.inputMainHorizontalLayout.setObjectName(_fromUtf8("inputMainHorizontalLayout"))
        self.stackedWidget = QtGui.QStackedWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.inputPage = QtGui.QWidget()
        self.inputPage.setObjectName(_fromUtf8("inputPage"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.inputPage)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.inputFileBtn = QtGui.QPushButton(self.inputPage)
        self.inputFileBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.inputFileBtn.setObjectName(_fromUtf8("inputFileBtn"))
        self.horizontalLayout_7.addWidget(self.inputFileBtn)
        self.inputFileEntry = QtGui.QLineEdit(self.inputPage)
        self.inputFileEntry.setMinimumSize(QtCore.QSize(0, 21))
        self.inputFileEntry.setMouseTracking(True)
        self.inputFileEntry.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.inputFileEntry.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.inputFileEntry.setObjectName(_fromUtf8("inputFileEntry"))
        self.horizontalLayout_7.addWidget(self.inputFileEntry)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.windowSizeLabel = QtGui.QLabel(self.inputPage)
        self.windowSizeLabel.setObjectName(_fromUtf8("windowSizeLabel"))
        self.horizontalLayout_8.addWidget(self.windowSizeLabel)
        self.windowSizeEntry = QtGui.QLineEdit(self.inputPage)
        self.windowSizeEntry.setMinimumSize(QtCore.QSize(40, 21))
        self.windowSizeEntry.setMaximumSize(QtCore.QSize(80, 16777215))
        self.windowSizeEntry.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.windowSizeEntry.setObjectName(_fromUtf8("windowSizeEntry"))
        self.horizontalLayout_8.addWidget(self.windowSizeEntry)
        self.windowOffsetLabel = QtGui.QLabel(self.inputPage)
        self.windowOffsetLabel.setObjectName(_fromUtf8("windowOffsetLabel"))
        self.horizontalLayout_8.addWidget(self.windowOffsetLabel)
        self.windowOffsetEntry = QtGui.QLineEdit(self.inputPage)
        self.windowOffsetEntry.setMinimumSize(QtCore.QSize(40, 21))
        self.windowOffsetEntry.setMaximumSize(QtCore.QSize(80, 16777215))
        self.windowOffsetEntry.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.windowOffsetEntry.setObjectName(_fromUtf8("windowOffsetEntry"))
        self.horizontalLayout_8.addWidget(self.windowOffsetEntry)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.outputDirBtn = QtGui.QPushButton(self.inputPage)
        self.outputDirBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.outputDirBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.outputDirBtn.setAcceptDrops(False)
        self.outputDirBtn.setAutoFillBackground(False)
        self.outputDirBtn.setObjectName(_fromUtf8("outputDirBtn"))
        self.horizontalLayout_9.addWidget(self.outputDirBtn)
        self.outputDirEntry = QtGui.QLineEdit(self.inputPage)
        self.outputDirEntry.setMinimumSize(QtCore.QSize(0, 21))
        self.outputDirEntry.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.outputDirEntry.setObjectName(_fromUtf8("outputDirEntry"))
        self.horizontalLayout_9.addWidget(self.outputDirEntry)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.runBtn = QtGui.QPushButton(self.inputPage)
        self.runBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.runBtn.setObjectName(_fromUtf8("runBtn"))
        self.horizontalLayout_10.addWidget(self.runBtn)
        self.progressBar = QtGui.QProgressBar(self.inputPage)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout_10.addWidget(self.progressBar)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.stackedWidget.addWidget(self.inputPage)
        self.outputPage = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputPage.sizePolicy().hasHeightForWidth())
        self.outputPage.setSizePolicy(sizePolicy)
        self.outputPage.setObjectName(_fromUtf8("outputPage"))
        self.gridLayout_5 = QtGui.QGridLayout(self.outputPage)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.outputTabs = QtGui.QTabWidget(self.outputPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputTabs.sizePolicy().hasHeightForWidth())
        self.outputTabs.setSizePolicy(sizePolicy)
        self.outputTabs.setObjectName(_fromUtf8("outputTabs"))
        self.standard = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.standard.sizePolicy().hasHeightForWidth())
        self.standard.setSizePolicy(sizePolicy)
        self.standard.setObjectName(_fromUtf8("standard"))
        self.gridLayout_4 = QtGui.QGridLayout(self.standard)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.standardImage = QtGui.QLabel(self.standard)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.standardImage.sizePolicy().hasHeightForWidth())
        self.standardImage.setSizePolicy(sizePolicy)
        self.standardImage.setText(_fromUtf8(""))
        self.standardImage.setObjectName(_fromUtf8("standardImage"))
        self.gridLayout_4.addWidget(self.standardImage, 0, 0, 1, 1)
        self.outputTabs.addTab(self.standard, _fromUtf8(""))
        self.bootstrap = QtGui.QWidget()
        self.bootstrap.setObjectName(_fromUtf8("bootstrap"))
        self.gridLayout_2 = QtGui.QGridLayout(self.bootstrap)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.bootstrapImage = QtGui.QLabel(self.bootstrap)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bootstrapImage.sizePolicy().hasHeightForWidth())
        self.bootstrapImage.setSizePolicy(sizePolicy)
        self.bootstrapImage.setText(_fromUtf8(""))
        self.bootstrapImage.setObjectName(_fromUtf8("bootstrapImage"))
        self.gridLayout_2.addWidget(self.bootstrapImage, 0, 0, 1, 1)
        self.outputTabs.addTab(self.bootstrap, _fromUtf8(""))
        self.summary = QtGui.QWidget()
        self.summary.setObjectName(_fromUtf8("summary"))
        self.gridLayout_3 = QtGui.QGridLayout(self.summary)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.pushButton_2 = QtGui.QPushButton(self.summary)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_3.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.outputTabs.addTab(self.summary, _fromUtf8(""))
        self.gridLayout_5.addWidget(self.outputTabs, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.outputPage)
        self.inputMainHorizontalLayout.addWidget(self.stackedWidget)
        self.gridLayout.addLayout(self.inputMainHorizontalLayout, 0, 0, 1, 1)
        PhylogeneticVisualization.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PhylogeneticVisualization)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 581, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        PhylogeneticVisualization.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(PhylogeneticVisualization)
        self.stackedWidget.setCurrentIndex(1)
        self.outputTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PhylogeneticVisualization)

    def retranslateUi(self, PhylogeneticVisualization):
        PhylogeneticVisualization.setWindowTitle(_translate("PhylogeneticVisualization", "Phylogenetic Visualization", None))
        self.inputFileBtn.setText(_translate("PhylogeneticVisualization", "Select Input File", None))
        self.windowSizeLabel.setText(_translate("PhylogeneticVisualization", "Window Size:", None))
        self.windowOffsetLabel.setText(_translate("PhylogeneticVisualization", "Window Offset:", None))
        self.outputDirBtn.setText(_translate("PhylogeneticVisualization", "Select Output Directory", None))
        self.runBtn.setText(_translate("PhylogeneticVisualization", "Run", None))
        self.outputTabs.setTabText(self.outputTabs.indexOf(self.standard), _translate("PhylogeneticVisualization", "Standard", None))
        self.outputTabs.setTabText(self.outputTabs.indexOf(self.bootstrap), _translate("PhylogeneticVisualization", "Boostrap", None))
        self.pushButton_2.setText(_translate("PhylogeneticVisualization", "PushButton", None))
        self.outputTabs.setTabText(self.outputTabs.indexOf(self.summary), _translate("PhylogeneticVisualization", "Summary", None))
        self.menuFile.setTitle(_translate("PhylogeneticVisualization", "File", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PhylogeneticVisualization = QtGui.QMainWindow()
    ui = Ui_PhylogeneticVisualization()
    ui.setupUi(PhylogeneticVisualization)
    PhylogeneticVisualization.show()
    sys.exit(app.exec_())

