# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

__author__ = "You Sheng Lin"
__copyright__ = "Copyright (C) 2018"
__license__ = "AGPL"
__email__ = "pyquino@gmail.com"

from core.QtModules import (
            pyqtSlot,
            QDialog,
            QTableWidgetItem, 
            QDoubleValidator, 
)

from .Ui_table_selector import Ui_Dialog
from xlrd import open_workbook

class Dialog(QDialog, Ui_Dialog):
    
    """
    Class documentation goes here.
    """
    def __init__(self, filename, tag, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.tag = tag
        if tag == 'signal':
            self.sigform()
        wb = open_workbook(filename)
        table = wb.sheet_by_index(0)
        self.ts_edit.setValidator(QDoubleValidator(0, 10, 6, self))
        self.tableWidget.setColumnCount(table.ncols)
        self.tableWidget.setRowCount(table.nrows)
        
        for row in range(table.nrows):
            for col in range(table.ncols):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(table.cell(row,col).value)))
        
        self.data = []
        self.fftchose = False
    
    def sigform(self):
        self.fft_btn.setVisible(False)
        self.ts_edit.setVisible(False)
        self.ts_select.setVisible(False)
        self.label.setVisible(False)
        self.select_all.setVisible(False)
    
    def accept(self):
        """
        self.data = [['title', d0, d1, ...], ...]
        """
        if self.tag =='data':
            self.fftchose = self.fft_btn.isChecked()
            cols = []
            self.time = float(self.ts_edit.text())
            for cell_range in self.tableWidget.selectedRanges():
                cols.extend(range(cell_range.leftColumn(), cell_range.rightColumn() + 1))
            for col in cols:
                d_col = []
                for row in range(self.tableWidget.rowCount()):
                    text = self.tableWidget.item(row, col).text()
                    if row == 0:
                        d_col.append(text)
                        continue
                    try:
                        d_col.append(float(text))
                    except ValueError:
                        pass
                self.data.append(d_col)
            super(Dialog, self).accept()
        elif self.tag == 'signal':
            cols = []
            for cell_range in self.tableWidget.selectedRanges():
                cols.extend(range(cell_range.leftColumn(), cell_range.rightColumn() + 1))
            for col in cols:
                d_col = []
                for row in range(self.tableWidget.rowCount()):
                    text = self.tableWidget.item(row, col).text()
                    if row == 0:
                        d_col.append(text)
                        continue
                    try:
                        d_col.append(float(text))
                    except ValueError:
                        pass
                self.data.append(d_col)
            super(Dialog, self).accept()
