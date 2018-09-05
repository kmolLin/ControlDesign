# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\kmol\ControlDesign\core\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(870, 698)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.main_splitter = QtWidgets.QSplitter(self.centralWidget)
        self.main_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.main_splitter.setObjectName("main_splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.main_splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.editorLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.editorLayout.setContentsMargins(0, 0, 0, 0)
        self.editorLayout.setObjectName("editorLayout")
        self.layoutWidget = QtWidgets.QWidget(self.main_splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.editor_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.editor_btn.setObjectName("editor_btn")
        self.horizontalLayout_2.addWidget(self.editor_btn)
        self.merge_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.merge_btn.setObjectName("merge_btn")
        self.horizontalLayout_2.addWidget(self.merge_btn)
        self.serial_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.serial_btn.setObjectName("serial_btn")
        self.horizontalLayout_2.addWidget(self.serial_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.layoutWidget)
        self.tabWidget.setToolTip("")
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout.addWidget(self.main_splitter)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 870, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuFiliter = QtWidgets.QMenu(self.menuBar)
        self.menuFiliter.setObjectName("menuFiliter")
        MainWindow.setMenuBar(self.menuBar)
        self.actionLoad_data = QtWidgets.QAction(MainWindow)
        self.actionLoad_data.setObjectName("actionLoad_data")
        self.actionFilter_Design = QtWidgets.QAction(MainWindow)
        self.actionFilter_Design.setObjectName("actionFilter_Design")
        self.actionSave_Image = QtWidgets.QAction(MainWindow)
        self.actionSave_Image.setObjectName("actionSave_Image")
        self.actionExport_data = QtWidgets.QAction(MainWindow)
        self.actionExport_data.setObjectName("actionExport_data")
        self.menuFiliter.addAction(self.actionLoad_data)
        self.menuFiliter.addAction(self.actionFilter_Design)
        self.menuFiliter.addAction(self.actionSave_Image)
        self.menuFiliter.addAction(self.actionExport_data)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuFiliter.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.editor_btn.setText(_translate("MainWindow", "Tool editor"))
        self.merge_btn.setText(_translate("MainWindow", "Merge Plot"))
        self.serial_btn.setText(_translate("MainWindow", "Serial port"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuFiliter.setTitle(_translate("MainWindow", "Filiter"))
        self.actionLoad_data.setText(_translate("MainWindow", "Load Data"))
        self.actionFilter_Design.setText(_translate("MainWindow", "Filter Design"))
        self.actionSave_Image.setText(_translate("MainWindow", "Save Image"))
        self.actionExport_data.setText(_translate("MainWindow", "Export data"))

import icon_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

