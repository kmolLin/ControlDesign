# -*- coding: utf-8 -*-

"""
Module implementing serialDlg.
"""

from PyQt5.QtCore import pyqtSlot, QIODevice
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtGui import QTextCursor
import platform
from .Ui_serialUI import Ui_serialDlg


class serialDlg(QDialog, Ui_serialDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Serial Dlg Using QtSerialPort function to do
        """
        super(serialDlg, self).__init__(parent)
        self.setupUi(self)
        self.initForms()
        self.serialport = QSerialPort(self)
        self.serialport.readyRead.connect(self.readData)

    
    def initForms(self):
        
        if platform.system() == "Windows":
            ports = list()
            for i in range(8):
                ports.append("COM%d" %((i+1)))    
            self.comboBoxPort.addItems(ports)
        else:
            #todo:scan system serial port
            self.__scanSerialPorts__()
        
        bauds = ["50","75","134","110","150","200","300","600","1200","2400","4800","9600","14400","19200","38400","56000","57600",
            "115200"]
        self.comboBoxBaud.addItems(bauds)
        self.comboBoxBaud.setCurrentIndex(len(bauds) - 1)
        
        checks = ["None","Odd","Even","Zero","One"]
        self.comboBoxCheckSum.addItems(checks)
        self.comboBoxCheckSum.setCurrentIndex(len(checks) - 1)
        
        bits = ["4 Bits", "5 Bits","6 Bits", "7 Bits", "8 Bits"]
        self.comboBoxBits.addItems(bits)
        self.comboBoxBits.setCurrentIndex(len(bits) - 1)
        
        stopbits = ["1 Bit","1.5 Bits","2 Bits"];
        self.comboBoxStopBits.addItems(stopbits)
        self.comboBoxStopBits.setCurrentIndex(0)
        
        port = self.comboBoxPort.currentText()
        baud = int("%s" % self.comboBoxBaud.currentText(), 10)
    
    def writeData(self, data):
        self.serialport.write(data)
        
    def readData(self):
        if self.serialport.canReadLine():
            data = self.serialport.readAll()
            self.textEditReceived.insertPlainText(data.data().decode())
            self.textEditReceived.moveCursor(QTextCursor.End)
    
    @pyqtSlot()
    def on_pushButtonOpenSerial_clicked(self):
        if self.serialport.isOpen():
            self.serialport.close()
            self.pushButtonOpenSerial.setText("Open")
            return
        self.serialport.setPortName(self.comboBoxPort.currentText())
        self.serialport.setBaudRate(int("%s" % self.comboBoxBaud.currentText(), 10))
        if self.serialport.open(QIODevice.ReadWrite):
            self.pushButtonOpenSerial.setText("Close")
            print("sucess")
        else:
            QMessageBox.critical(self, "Error", self.serialport.errorString())
            
    
    @pyqtSlot()
    def on_pushButtonSendData_clicked(self):
        data = self.textEditSent.toPlainText()
        byt = data.encode("utf-8")
        self.writeData(byt)