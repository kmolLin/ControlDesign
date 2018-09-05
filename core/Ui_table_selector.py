# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\kmol\fft_project\core\table_selector.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(533, 409)
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.ts_edit = QtWidgets.QLineEdit(Dialog)
        self.ts_edit.setInputMask("")
        self.ts_edit.setObjectName("ts_edit")
        self.horizontalLayout_3.addWidget(self.ts_edit)
        self.ts_select = QtWidgets.QComboBox(Dialog)
        self.ts_select.setObjectName("ts_select")
        self.ts_select.addItem("")
        self.ts_select.addItem("")
        self.horizontalLayout_3.addWidget(self.ts_select)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)
        self.fft_btn = QtWidgets.QCheckBox(Dialog)
        self.fft_btn.setObjectName("fft_btn")
        self.horizontalLayout_2.addWidget(self.fft_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.select_all = QtWidgets.QPushButton(Dialog)
        self.select_all.setObjectName("select_all")
        self.horizontalLayout_2.addWidget(self.select_all)
        self.select_clear = QtWidgets.QPushButton(Dialog)
        self.select_clear.setObjectName("select_clear")
        self.horizontalLayout_2.addWidget(self.select_clear)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)
        self.tableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.select_all.clicked.connect(self.tableWidget.selectAll)
        self.select_clear.clicked.connect(self.tableWidget.clearSelection)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Sample Time"))
        self.ts_select.setItemText(0, _translate("Dialog", "Sec"))
        self.ts_select.setItemText(1, _translate("Dialog", "Msec"))
        self.fft_btn.setText(_translate("Dialog", "Fast fouir"))
        self.select_all.setText(_translate("Dialog", "Select All"))
        self.select_clear.setText(_translate("Dialog", "Clear Selection"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

