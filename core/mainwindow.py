# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from core.QtModules import (
    pyqtSlot,
    DataChart,
    QMainWindow,
    QFileDialog,
    QDoubleValidator,
    QCategoryAxis,
    QValueAxis,
    QChartView,
    QSizePolicy,
    QLineSeries,
    QPointF,
    QSplineSeries,
    QChart, 
    QView,
    QIcon,
    QPixmap, 
    Qt, 
    QApplication, 
    QInputDialog, 
    QColor,
    QWidget,
)
from .table_selector import Dialog
from .widgets.Ui_mainwindow import Ui_MainWindow
from .filter import FiterDialog
from core.symbolic import SymbolicBlock
from core.serial.serialUI import serialDlg
import time

import numpy as np
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from .ETFE.etfe import ETFE, sys_frq_rep
from .ETFE.bodeplot_module import bode_plot


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.view = None
        self.original_data = []
        self.build_actions()
        self.tabcount = []
        self.symbolic = SymbolicBlock(self)
        self.editorLayout.addWidget(self.symbolic)
        self.symbolic_size = 20
        self.main_splitter.setSizes([0, 200])
    
    def build_actions(self):
        self.toolBar.addAction(QIcon(QPixmap(':/core/icons/open-icon.png')), "Openfile")
        self.toolBar.addAction(QIcon(QPixmap(':/core/icons/save-icon.png')), "Savefile")
        self.toolBar.addAction(QIcon(QPixmap(':/core/icons/Settings-icon.png')), "Setting")
        self.toolBar.addAction(QIcon(QPixmap(':/core/icons/Actions-process-stop-icon.png')), "Stop")

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()

    def addChartFromXY(self, title: str, x, y):
        axisX = QValueAxis()
        axisY = QValueAxis()
        chart = DataChart(title, axisX, axisY)
        chart.setTheme(QChart.ChartThemeBlueNcs)
        line = QSplineSeries()
        #line.setName("test")
        for i in range(len(x)):
            line.append(QPointF(x[i], y[i]))
        chart.addSeries(line)
        line.attachAxis(axisX)
        line.attachAxis(axisY)
        self.view = QView()
        self.view.combinedata(y)
        self.view.addQchart(chart)
        self.tabWidget.addTab(self.view, title)
        self.tabcount.append([title, self.view])
    
    def addChart(self, title, data, fftchose):
        axisX = QValueAxis()
        axisY = QValueAxis()
        chart = DataChart(title, axisX, axisY)
        chart.setTheme(QChart.ChartThemeBlueNcs)
        ffttmp = []
        for col in data:
            line = QSplineSeries()
            line.setName(col[0])
            for row, value in enumerate(col[1:]):
                if fftchose:
                    ffttmp.append(value)
                else:
                    line.append(QPointF(self.sampletime*row, value))
            if fftchose:
                sp = np.fft.fft(ffttmp)
                Ayf = np.abs(sp)
                freq = np.fft.fftfreq(len(ffttmp), d = self.sampletime)
                for i in range(len(Ayf)-1):
                    line.append(QPointF(freq[i], Ayf[i]))
            chart.addSeries(line)
            line.attachAxis(axisX)
            line.attachAxis(axisY)
        self.view = QView()
        self.view.combinedata(data)
        self.view.addQchart(chart)
        self.tabWidget.addTab(self.view, title)
        self.tabcount.append([title, self.view])
    
    @pyqtSlot()
    def on_editor_btn_clicked(self):
        sizes = self.main_splitter.sizes()
        size = sizes[0]
        if size:
            self.symbolic_size = size
            self.main_splitter.setSizes([0, sizes[1]])
        else:
            self.main_splitter.setSizes([self.symbolic_size, sizes[1]])
    
    @pyqtSlot(int)
    def on_tabWidget_tabCloseRequested(self, index):
        self.tabWidget.removeTab(index)
        try:
            self.tabcount.pop(index)
        except:
            pass
    
    @pyqtSlot()
    def on_actionLoad_data_triggered(self):
        """
        Loading data from excel 
        """
        file, _ = QFileDialog.getOpenFileName(self, 'open file','', 'Excel(*.xlsx)')
        if not file:
            return
        dlg = Dialog(file, 'data')
        dlg.show()
        if dlg.exec_():
            self.original_data = dlg.data
            self.sampletime = dlg.time
            if dlg.fftchose:
                tabtitle = "FFT"
            else:
                tabtitle = "Original data"
            self.addChart(tabtitle, self.original_data, dlg.fftchose)
    
    @pyqtSlot()
    def on_actionFilter_Design_triggered(self):
        """
        Design the filter to data
        """
        dlg = FiterDialog(self.tabcount)
        dlg.show()
        if not dlg.exec_():
            return
        calcdata = dlg.outputarray
        if 'filterDseign' in calcdata:
            x, y = calcdata.get('filterDseign')
            self.addChartFromXY("filterDseign", x, y)
        if calcdata.__contains__('filterdata'):
            x, y = calcdata.get('filterdata')
            self.addChartFromXY("filterDseign", x, y)
        if calcdata.__contains__('filerfft'):
            x, y = calcdata.get('filerfft')
            self.addChartFromXY("filterDseign", x, y)
        if calcdata.__contains__('zeroPhase'):
            x, y = calcdata.get('zeroPhase')
            self.addChartFromXY("ZeroPhase", x, y)
    
    @pyqtSlot()
    def on_actionSave_Image_triggered(self):
        """
        Save Image to cilck board
        """
        # TODO: add save image files not on clickboard
        if self.tabWidget.currentWidget():
            QApplication.clipboard().setPixmap(self.tabWidget.currentWidget().grab())
    
    @pyqtSlot()
    def on_merge_btn_clicked(self):
        tmp = []
        for i in range(self.tabWidget.count()):
            if i == self.tabWidget.currentIndex():
                continue
            tmp.append(str(i)+":"+self.tabWidget.tabText(i))
        item, ok = QInputDialog.getItem(self, "Merge", "Select figure", tmp, 0, False)
        if not ok: return
        tabcunt = int(item.split(":")[0])
        view = self.tabWidget.widget(self.tabWidget.currentIndex())
        mer = self.tabWidget.widget(tabcunt)
        for seri in mer.m_chart.series():
            spline = QSplineSeries()
            spline.append(seri.pointsVector())
            view.m_chart.addSeries(spline)
        self.on_tabWidget_tabCloseRequested(tabcunt)
        mer.close()
    
    @pyqtSlot()
    def on_serial_btn_clicked(self):
        title = "serial"
        axisX = QValueAxis()
        axisY = QValueAxis()
        chart = DataChart(title, axisX, axisY)
        chart.setTheme(QChart.ChartThemeBlueNcs)
        line = QSplineSeries()
        line.setName("serial")
        chart.addSeries(line)
        line.attachAxis(axisX)
        line.attachAxis(axisY)
        self.view = QView()
        #self.view.combinedata(y)
        self.view.addQchart(chart)
        self.tabWidget.addTab(self.view, title)
        self.tabcount.append([title, self.view])
        
        def addline(y: float):
            print(line.count()*0.1, y)
            line.append(line.count(), y)
        
        dlg = serialDlg()
        dlg.receive_signal.connect(addline)
        dlg.show()
        if not dlg.exec_():
            return
    
    @pyqtSlot()
    def on_actionBode_triggered(self):
        
        # TODO : testcode for etfe bode draw
        file, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'Excel(*.txt)')
        if not file:
            return
        with open(file, 'r') as f:
            lines = f.readlines()
        timex = []
        input = []
        output = []
        for line in lines:
            timex.append(float(line.split(' ')[0]))
            input.append(float(line.split(' ')[1]))
            output.append(float(line.split(' ')[2]))
        # n = 1024. * 16
        n = 20001
        # t_freq_h: units (Hz)
        # t_mag: units (DB)
        # t_phase: units (Deg)
        tfreq, tfreq_h, tmag_sys, tphase, imag_value, real_value = ETFE(input, 0.0005, n, output)
        mag, phase, r, i = sys_frq_rep(0.01, real_value, imag_value, tfreq, tmag_sys, tphase)

        figure_merge = bode_plot(tfreq_h, mag, phase, False)

        wi = QWidget(self)
        layout = QtWidgets.QVBoxLayout(wi)
        dbplotWidget = FigureCanvas(figure_merge)
        layout.addWidget(dbplotWidget)
        self.addToolBar(NavigationToolbar(dbplotWidget, self))
        self.tabWidget.addTab(wi, "Bode")
