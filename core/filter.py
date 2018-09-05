# -*- coding: utf-8 -*-

"""
Module implementing FiterDialog.
"""

from core.QtModules import (QDialog, pyqtSlot, QDoubleValidator, 
)
from .Ui_filter import Ui_Dialog
from scipy.signal import butter, lfilter, filtfilt

import numpy as np
from scipy.signal import freqz


class FiterDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, tabcount, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(FiterDialog, self).__init__(parent)
        self.setupUi(self)
        self.samplerate.setValidator(QDoubleValidator(0, 2000, 4, self))
        self.lowcut_edit.setValidator(QDoubleValidator(0, 2000, 4, self))
        self.highcut_edit.setValidator(QDoubleValidator(0, 2000, 4, self))
        self.order_edit.setValidator(QDoubleValidator(0, 10, 0, self))
        self.tabcount = tabcount
        self.outputarray = {}
        
        if tabcount == []:
            pass
        else:
            print(len(tabcount))
            for i, value in enumerate(tabcount):
                self.combodata.insertItem(i, value[0])
                
        
            
    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a


    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        Ts = 1/fs
        Nall = len(data)
        t = np.arange(0.0,(Nall-1)*Ts,Ts)
        return t, y
        
    def filterDesign(self):
        b, a = self.butter_bandpass(self.lowcut, self.highcut, self.fs, self.order)
        w, h = freqz(b, a, worN=1000)
        return (self.fs * 0.5 / np.pi) * w, abs(h)
    
    def proessfft(self, signal, T):
        sp = np.fft.fft(signal)
        Ayf = abs(sp)
        freq = np.fft.fftfreq(len(Ayf), d = T)
        return freq, Ayf
        
    def zeroPhase(self, data):
        b, a = self.butter_bandpass(self.lowcut, self.highcut, self.fs, self.order)
        y = filtfilt(b, a, data)
        Ts = 1/self.fs
        Nall = len(data)
        t = np.arange(0.0,(Nall-1)*Ts,Ts)
        return t, y
        
        
    
    def accept(self):
        
        self.fs = float(self.samplerate.text())
        self.lowcut = float(self.lowcut_edit.text())
        self.highcut = float(self.highcut_edit.text())
        self.order = int(self.order_edit.text())
        #self.fs = 100.0
        #self.lowcut = 8.0
        #self.highcut = 10.5
        #self.order = 5
        coun  = self.tabcount[self.combodata.currentIndex()][1]
        for data in coun.data:
            tmplist = []
            for row, value in enumerate(data[1:]):
                tmplist.append(value)   
        if self.filtercbox.isChecked():
            a, b = self.filterDesign()
            self.outputarray["filterDseign"] = [a, b]
        if self.filteredcbox.isChecked() :
            # TODO : add method to chose another line to filter
            a, b = self.butter_bandpass_filter(tmplist, self.lowcut, self.highcut, self.fs, self.order)
            self.outputarray["filterdata"] = [a, b]
        if self.firteredFftcbox.isChecked():
            a, b = self.proessfft(self.outputarray['filterdata'][1], 1/self.fs)
            self.outputarray["filerfft"] = [a, b]
        if self.zeroctbox.isChecked():
            a, b = self.zeroPhase(tmplist)
            self.outputarray["zeroPhase"] = [a, b]
        super(FiterDialog, self).accept()
        
        

    
    
