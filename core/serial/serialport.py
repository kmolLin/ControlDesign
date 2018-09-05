# -*- coding: utf-8 -*-

"""
Module implementing Serialport.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_serialUI import Ui_serialDlg


class Serialport(QDialog, Ui_serialDlg):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Serialport, self).__init__(parent)
        self.setupUi(self)
