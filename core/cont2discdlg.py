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
from pylab import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PyQt5 import QtGui
from .Ui_cont2discdlg import Ui_c2ddlg
from .table_selector import Dialog


class c2ddlg(QDialog, Ui_c2ddlg):

    def __init__(self, calcendBlock, parent=None):
        super(c2ddlg, self).__init__(parent)
        self.setupUi(self)
        self.block = calcendBlock
        self.ts_edit.setValidator(QDoubleValidator(0, 10, 6, self))
        self.numlabel.setPixmap(self.math_tex_to_qpixmap(
            self.init_math_equation(self.block.num,
                                self.block.den), 25))
        self.indcator = ["zoh", "bilinear"]
        self.selector = 'impuse'
        self.outputarray = []

    def init_math_equation(self, n, d):
        test_n = ""
        for i in range(len(n.c)):
            tmp = n.c[i]
            ordere = len(n.c) - 1 - i
            if tmp == 0:
                continue
            if ordere == 0:
                test_n += f"{tmp}"
                break
            test_n += f"{tmp} S^{ordere} +"
        test_d = ""
        for i in range(len(d.c)):
            tmp = d.c[i]
            ordere = len(d.c) - 1 - i
            if tmp == 0:
                continue
            if ordere == 0:
                test_d += f"{tmp}"
                break
            test_d += f"{tmp} S^{ordere} +"
        math_text = "$\\frac{ {" + test_n + "} } { {" + test_d + "} }$"
        return math_text

    def math_tex_to_qpixmap(self, math_tex: str, fs: int):

        # set up a mpl figure instance
        fig = Figure()
        fig.patch.set_facecolor('none')
        fig.set_canvas(FigureCanvasAgg(fig))
        renderer = fig.canvas.get_renderer()

        # plot the math_tex expression
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.patch.set_facecolor('none')
        t = ax.text(0, 0, math_tex, ha='left', va='bottom', fontsize=fs)

        # fit figure size to text artist
        f_width, f_height = fig.get_size_inches()
        fig_bbox = fig.get_window_extent(renderer)
        text_bbox = t.get_window_extent(renderer)
        tight_fwidth = text_bbox.width * f_width / fig_bbox.width
        tight_fheight = text_bbox.height * f_height / fig_bbox.height
        fig.set_size_inches(tight_fwidth, tight_fheight)

        # convert mpl figure to QPixmap
        buf, size = fig.canvas.print_to_buffer()
        qimage = QtGui.QImage.rgbSwapped(QtGui.QImage(buf, size[0], size[1],
                                                      QtGui.QImage.Format_ARGB32))
        qpixmap = QtGui.QPixmap(qimage)

        return qpixmap

    def calcc2d(self, e, num, den, sampletime):
        u = []
        for k, e_k in enumerate(e):
            sum1 = 0
            for i, num_i in enumerate(num):
                if k - i < 0:
                    continue
                else:
                    sum1 += num[i] * e[k - i]
            sum2 = 0
            for io in range(1, len(den)):
                if k == 0:
                    sum2 += 0
                    continue
                if k - io < 0:
                    sum2 += 0
                else:
                    sum2 += den[io] * u[k - io]
            u.append(sum1 - sum2)
        t = np.arange(0, sampletime * (len(e)), sampletime)
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
        file, _ = QFileDialog.getOpenFileName(self, 'open file', '', 'Excel(*.xlsx)')
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