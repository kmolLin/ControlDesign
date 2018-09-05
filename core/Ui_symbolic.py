# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\kmol\fft_project\core/symbolic.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(574, 458)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main_splitter = QtWidgets.QSplitter(Dialog)
        self.main_splitter.setOrientation(QtCore.Qt.Vertical)
        self.main_splitter.setObjectName("main_splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.main_splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.editor_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.editor_layout.setContentsMargins(0, 0, 0, 0)
        self.editor_layout.setObjectName("editor_layout")
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setObjectName("button_layout")
        self.loadfile_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.loadfile_btn.setObjectName("loadfile_btn")
        self.button_layout.addWidget(self.loadfile_btn)
        self.savefile_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.savefile_btn.setObjectName("savefile_btn")
        self.button_layout.addWidget(self.savefile_btn)
        self.signal_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.signal_btn.setObjectName("signal_btn")
        self.button_layout.addWidget(self.signal_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.button_layout.addItem(spacerItem)
        self.calcblock_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.calcblock_btn.setObjectName("calcblock_btn")
        self.button_layout.addWidget(self.calcblock_btn)
        self.editor_layout.addLayout(self.button_layout)
        self.console = QtWidgets.QTextBrowser(self.main_splitter)
        self.console.setObjectName("console")
        self.verticalLayout.addWidget(self.main_splitter)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.loadfile_btn.setText(_translate("Dialog", "Load file"))
        self.savefile_btn.setText(_translate("Dialog", "Save File"))
        self.signal_btn.setText(_translate("Dialog", "signal test"))
        self.calcblock_btn.setText(_translate("Dialog", "Run"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QWidget()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

