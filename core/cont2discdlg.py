# -*- coding: utf-8 -*-

"""
Module implementing c2ddlg.
"""
from core.QtModules import (
    pyqtSlot, 
    QDialog, 
    QDoubleValidator, 
    QFileDialog, 
)
import numpy as np
from scipy.signal import cont2discrete, impulse, step
from .Ui_cont2discdlg import Ui_c2ddlg
from .table_selector import Dialog


class c2ddlg(QDialog, Ui_c2ddlg):
    
    def __init__(self, calcendBlock, parent=None):
        super(c2ddlg, self).__init__(parent)
        self.setupUi(self)
        self.block = calcendBlock
        self.ts_edit.setValidator(QDoubleValidator(0, 10, 6, self))
        n = self.block.num
        d = self.block.den
        self.numlabel.setText(f"{n}")
        self.denlabel.setText(f"{d}")
        self.indcator = ["zoh", "bilinear"]
        self.selector = 'impuse'
        self.outputarray = []
        
    def calcc2d(self, e, num, den, sampletime):
        u = []
        for k, e_k in enumerate(e):
            sum1 = 0
            for i, num_i in enumerate(num):
                if k - i < 0:
                    continue
                else:
                    sum1 += num[i]*e[k-i]
            sum2 = 0
            for io in range(1, len(den)):
                if k == 0:
                    sum2 += 0
                    continue
                if k-io < 0:
                    sum2 += 0
                else:
                    sum2 += den[io] * u[k-io]
            u.append(sum1 - sum2)
        t = np.arange(0, sampletime*(len(e)), sampletime)
        return t, u
        
    def setMaskonui(self, check):
        self.sampletime_label.setEnabled(check)
        self.ts_edit.setEnabled(check)
        self.sec_label.setEnabled(check)
        self.method_label.setEnabled(check)
        self.methodbox.setEnabled(check)
        self.loadfile.setEnabled(check)
    
    @pyqtSlot()
    def on_custom_radio_clicked(self):
        self.setMaskonui(True)
        self.selector = 'custom'
    
    @pyqtSlot()
    def on_impuse_radio_clicked(self):
        self.setMaskonui(False)
        self.selector = 'impuse'
    
    @pyqtSlot()
    def on_step_radio_clicked(self):
        self.setMaskonui(False)
        self.selector = 'step'
        
    def accept(self):
        print(self.selector)
        if self.selector == 'impuse':
            t, u = impulse((self.block.num, self.block.den))
            self.get = [t, u]
        if self.selector == 'step':
            t, u = step((self.block.num, self.block.den))
            self.get = [t, u]
        if self.selector == 'custom':
            time = float(self.ts_edit.text())
            count = self.methodbox.currentIndex()
            dd, d1, d3d = cont2discrete((self.block.num, self.block.den), time, self.indcator[count])
            if self.sigtmp:
                t, u = self.calcc2d(self.sigtmp, dd[0], d1, d3d)
            self.get = [t, u]
        super(c2ddlg, self).accept()
    
    @pyqtSlot()
    def on_loadfile_clicked(self):
        file, _ = QFileDialog.getOpenFileName(self, 'open file','', 'Excel(*.xlsx)')
        if not file:
            return
        dlg = Dialog(file, 'signal')
        dlg.show()
        if dlg.exec_():
            dlg.data
            self.sigtmp = []
            for col in dlg.data:
                for row, value in enumerate(col[1:]):
                    self.sigtmp.append(value)
