# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\kmol\fft_project\core/filter.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.firteredFftcbox = QtWidgets.QCheckBox(Dialog)
        self.firteredFftcbox.setObjectName("firteredFftcbox")
        self.gridLayout.addWidget(self.firteredFftcbox, 0, 1, 1, 1)
        self.filteredcbox = QtWidgets.QCheckBox(Dialog)
        self.filteredcbox.setObjectName("filteredcbox")
        self.gridLayout.addWidget(self.filteredcbox, 1, 0, 1, 1)
        self.filtercbox = QtWidgets.QCheckBox(Dialog)
        self.filtercbox.setObjectName("filtercbox")
        self.gridLayout.addWidget(self.filtercbox, 0, 0, 1, 1)
        self.zeroctbox = QtWidgets.QCheckBox(Dialog)
        self.zeroctbox.setObjectName("zeroctbox")
        self.gridLayout.addWidget(self.zeroctbox, 1, 1, 1, 1)
        self.combodata = QtWidgets.QComboBox(Dialog)
        self.combodata.setObjectName("combodata")
        self.gridLayout.addWidget(self.combodata, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.samplerate = QtWidgets.QLineEdit(Dialog)
        self.samplerate.setObjectName("samplerate")
        self.horizontalLayout.addWidget(self.samplerate)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lowcut_edit = QtWidgets.QLineEdit(Dialog)
        self.lowcut_edit.setObjectName("lowcut_edit")
        self.horizontalLayout_2.addWidget(self.lowcut_edit)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.highcut_edit = QtWidgets.QLineEdit(Dialog)
        self.highcut_edit.setObjectName("highcut_edit")
        self.horizontalLayout_3.addWidget(self.highcut_edit)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.order_edit = QtWidgets.QLineEdit(Dialog)
        self.order_edit.setObjectName("order_edit")
        self.horizontalLayout_5.addWidget(self.order_edit)
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_4.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Filter Design"))
        self.firteredFftcbox.setText(_translate("Dialog", "Filtered data FFT"))
        self.filteredcbox.setText(_translate("Dialog", "Filtered data"))
        self.filtercbox.setText(_translate("Dialog", "Filter Design"))
        self.zeroctbox.setText(_translate("Dialog", "ZeroPhase"))
        self.label.setText(_translate("Dialog", "Sample Rate"))
        self.label_2.setText(_translate("Dialog", "Hz"))
        self.label_3.setText(_translate("Dialog", "Low Cut"))
        self.label_5.setText(_translate("Dialog", "Hz"))
        self.label_4.setText(_translate("Dialog", "High Cut"))
        self.label_6.setText(_translate("Dialog", "Hz"))
        self.label_7.setText(_translate("Dialog", "Order"))
        self.label_8.setText(_translate("Dialog", "N"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

