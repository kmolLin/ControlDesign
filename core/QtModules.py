# -*- coding: utf-8 -*-

"""This module contain all the Qt objects we needed.

Customized class will define below.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from PyQt5.QtCore import (
    pyqtSignal,
    pyqtSlot,
    QCoreApplication,
    QDir,
    QFileInfo,
    QModelIndex,
    QMutex,
    QMutexLocker,
    QObject,
    QPoint,
    QPointF,
    QRectF,
    QSettings,
    QSize,
    QSizeF,
    QStandardPaths,
    QThread,
    QTimer,
    QUrl,
    Qt,
    QRect,
    QEvent,
)
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QAction,
    QApplication,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDial,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
    QProgressDialog,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QSplashScreen,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTableWidgetSelectionRange,
    QTextEdit,
    QToolTip,
    QUndoCommand,
    QUndoStack,
    QUndoView,
    QVBoxLayout,
    QWidget,
    QGraphicsSimpleTextItem, 
    QGraphicsItem, 
    
)
from PyQt5.QtGui import (
    QBrush,
    QColor,
    QCursor,
    QDesktopServices,
    QDoubleValidator,
    QFont,
    QIcon,
    QImage,
    QKeySequence,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QPolygonF,
    QTextCursor,
    QFontMetrics,
    
)
from PyQt5.QtChart import (
    QCategoryAxis,
    QChart,
    QChartView,
    QLineSeries,
    QScatterSeries,
    QValueAxis,
    QSplineSeries
)
from PyQt5.QtCore import qVersion, PYQT_VERSION_STR
from PyQt5.Qsci import (
    QsciScintilla,
    QsciLexerPython,
)

__all__ = [
    'pyqtSignal',
    'pyqtSlot',
    'qVersion',
    'PYQT_VERSION_STR',
    'QAbstractItemView',
    'QAction',
    'QApplication',
    'QBrush',
    'QCategoryAxis',
    'QChart',
    'QChartView',
    'QCheckBox',
    'QColor',
    'QColorDialog',
    'QComboBox',
    'QCoreApplication',
    'QCursor',
    'QDesktopServices',
    'QDial',
    'QDialog',
    'QDialogButtonBox',
    'QDir',
    'QDoubleSpinBox',
    'QDoubleValidator',
    'QFileDialog',
    'QFileInfo',
    'QFont',
    'QGraphicsScene',
    'QGraphicsView',
    'QHBoxLayout',
    'QIcon',
    'QImage',
    'QInputDialog',
    'QKeySequence',
    'QLabel',
    'QLineEdit',
    'QLineSeries',
    'QListWidget',
    'QListWidgetItem',
    'QMainWindow',
    'QMenu',
    'QMessageBox',
    'QModelIndex',
    'QMutex',
    'QMutexLocker',
    'QObject',
    'QPainter',
    'QPainterPath',
    'QPen',
    'QPixmap',
    'QPoint',
    'QPointF',
    'QPolygonF',
    'QProgressDialog',
    'QPushButton',
    'QRectF',
    'QSpacerItem',
    'QScatterSeries',
    'QSettings',
    'QSize',
    'QSizeF',
    'QSizePolicy',
    'QSpinBox',
    'QSplashScreen',
    'QSplineSeries',
    'QStandardPaths',
    'QTabWidget',
    'QTableWidget',
    'QTableWidgetItem',
    'QTableWidgetSelectionRange',
    'QTextCursor',
    'QTextEdit',
    'QThread',
    'QTimer',
    'QToolTip',
    'QUndoCommand',
    'QUndoStack',
    'QUndoView',
    'QUrl',
    'QValueAxis',
    'QVBoxLayout',
    'QWidget',
    'Qt',
    'DataChart',
    'QGraphicsSimpleTextItem',
    'QFontMetrics',
    'QRect',
    'QGraphicsItem',
    'QEvent',
    'QsciScintilla',
    'QsciLexerCustomPython',
]


class DataChart(QChart):
    
    """A axis setted Qt chart widget."""
    
    def __init__(self,
        title: str,
        axis_x: QValueAxis,
        axis_y: QValueAxis
    ):
        """Input title and two axis, QChart class has no parent."""
        super(DataChart, self).__init__()
        self.setTitle(title)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        legend = self.legend()
        legend.setAlignment(Qt.AlignBottom)
        legend.setFont(QFont(legend.font().family(), 12, QFont.Medium))
        self.addAxis(axis_x, Qt.AlignBottom)
        self.addAxis(axis_y, Qt.AlignLeft)


class Callout(QGraphicsItem):
    def __init__(self, chart):
        super(Callout, self).__init__(chart)
        self.chart = chart
        self.m_font = QFont()
        self.m_anchor = QPointF()
        self.m_rect = QRectF()
        self.m_textRect = QRectF()
        self.m_text = ""
        self.leftclick = False
        
    
    def boundingRect(self):
        anchor = self.mapFromParent(self.chart.mapToPosition(self.m_anchor))
        rect = QRectF()
        rect.setLeft(min(self.m_rect.left(), anchor.x()))
        rect.setRight(max(self.m_rect.right(), anchor.x()))
        rect.setTop(min(self.m_rect.top(), anchor.y()))
        rect.setBottom(max(self.m_rect.bottom(), anchor.y()))
        return rect
    
    def paint(self, painter, option, widget):
        path = QPainterPath()
        x, y, w, d = self.m_rect.getRect()
        self.m_rect = QRectF(x, y, w, d)
        path.addRoundedRect(self.m_rect, 5, 5)
        
        anchor = self.mapFromParent(self.chart.mapToPosition(self.m_anchor))
        if not self.m_rect.contains(QPoint(int(anchor.x()), int(anchor.y()))):
            point1 = QPointF()
            point2 = QPointF()
            above = anchor.y() <= self.m_rect.top()
            aboveCenter = anchor.y() > self.m_rect.top() and anchor.y() <= self.m_rect.center().y()
            belowCenter = anchor.y() > self.m_rect.center().y() and anchor.y() <= self.m_rect.bottom()
            below = anchor.y() > self.m_rect.bottom()
            onLeft = anchor.x() <= self.m_rect.left()
            leftOfCenter = anchor.x() > self.m_rect.left() and anchor.x() <= self.m_rect.center().x()
            rightOfCenter = anchor.x() > self.m_rect.center().x() and anchor.x() <= self.m_rect.right()
            onRight = anchor.x() > self.m_rect.right()
            #get the nearest m_rect corner
            x = (onRight + rightOfCenter) * self.m_rect.width()
            y = (below + belowCenter) * self.m_rect.height()
            cornerCase = (above and onLeft) or (above and onRight) or (below and onLeft) or (below and onRight)
            vertical = abs(anchor.x() - x) > abs(anchor.y() - y)
            x1 = x + leftOfCenter * 10 - rightOfCenter * 20 + cornerCase * (not vertical) * (onLeft * 10 - onRight * 20)
            y1 = y + aboveCenter * 10 - belowCenter * 20 + cornerCase * vertical * (above * 10 - below * 20)
            point1.setX(x1)
            point1.setY(y1)
            x2 = x + leftOfCenter * 20 - rightOfCenter * 10 + cornerCase * (not vertical) * (onLeft * 20 - onRight * 10)
            y2 = y + aboveCenter * 20 - belowCenter * 10 + cornerCase * vertical * (above * 20 - below * 10)
            point2.setX(x2)
            point2.setY(y2)
            path.moveTo(point1)
            path.lineTo(anchor)
            path.lineTo(point2)
            path = path.simplified()
        painter.setBrush(QColor(255, 255, 255))
        painter.drawPath(path)
        painter.drawText(self.m_textRect, Qt.AlignLeft , self.m_text)
    
    def mousePressEvent(self, event):
        event.setAccepted(True)
    
    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton):
            self.setPos(self.mapToParent(event.pos() - event.buttonDownPos(Qt.LeftButton)))
            event.setAccepted(True)
        else:
            event.setAccepted(False)

    def setText(self, text):
        self.m_text = text
        metrics = QFontMetrics(self.m_font)
        self.m_textRect = metrics.boundingRect(QRect(0, 0, 150, 150), Qt.AlignLeft, self.m_text)
        self.m_textRect.translate(5, 5)
        self.prepareGeometryChange()
        self.m_rect = self.m_textRect.adjusted(-5, -5, 5, 5)
        
    def setAnchor(self, point):
        self.m_anchor = point
    
    def updateGeometry(self):
        self.prepareGeometryChange()
        self.setPos(self.chart.mapToPosition(self.m_anchor) + QPoint(10, -50))

    
class QView(QGraphicsView):
    
    def __init__(self, parent = None):
        super(QView, self).__init__(QGraphicsScene(), parent)
        self.m_coordX = None
        self.m_coordY = None
        self.m_chart = None
        self.m_tooltip = None
        self.m_callouts = []
        self.setMouseTracking(True)
        self.data = None
        self.__dragged = False
        self.__pos = QPoint(0, 0)
    
    def combinedata(self, data):
        self.data = data
    
    def addQchart(self, chart):
        self.m_chart = chart
        self.scene().addItem(self.m_chart)
        self.m_coordX = QGraphicsSimpleTextItem(self.m_chart)
        self.m_coordX.setPos(self.m_chart.size().width()/2 - 50, self.m_chart.size().height())
        self.m_coordX.setText("X: ")
        self.m_coordY = QGraphicsSimpleTextItem(self.m_chart)
        self.m_coordY.setPos(self.m_chart.size().width()/2 + 50, self.m_chart.size().height())
        self.m_coordY.setText("Y: ")
        for series in self.m_chart.series():
            series.hovered.connect(self.tooltip)
            series.doubleClicked.connect(self.keepCallout)
            
    def resizeEvent(self, event):
        if (self.scene()):
            self.scene().setSceneRect(QRectF(QPoint(0, 0), QSizeF(event.size())))
            self.m_chart.resize(QSizeF(event.size()))
            self.m_coordX.setPos(self.m_chart.size().width()/2 - 50, self.m_chart.size().height() - 20)
            self.m_coordY.setPos(self.m_chart.size().width()/2 + 50, self.m_chart.size().height() - 20)
            for callout in self.m_callouts:
                callout.updateGeometry()
        super(QView, self).resizeEvent(event)
    
    def keyPressEvent(self, event):
        if self.m_chart == None:
            return
        else:
            self.m_chart.setAnimationOptions(QChart.SeriesAnimations)
        if event.key() == Qt.Key_Plus:
            self.m_chart.zoomIn()
        elif event.key() == Qt.Key_Minus:
            self.m_chart.zoomOut()
        elif event.key() == Qt.Key_Up:
            self.m_chart.scroll(0, 10)
        elif event.key() == Qt.Key_Left:
            self.m_chart.scroll(-10, 0)
        elif event.key() == Qt.Key_Right:
            self.m_chart.scroll(10, 0)
        elif event.key() == Qt.Key_Down:
            self.m_chart.scroll(0, -10)
    
    
    def mouseMoveEvent(self, event):
        self.m_coordX.setText("X: {}".format(round(self.m_chart.mapToValue(event.pos()).x(), 3)))
        self.m_coordY.setText("Y: {}".format(round(self.m_chart.mapToValue(event.pos()).y(), 3)))
        
        if event.buttons() == Qt.MidButton:
            value = self.m_chart.mapToValue(event.pos())
            pos = (self.m_chart.mapToValue(self.__pos) - value)
            self.m_chart.scroll(pos.x(), pos.y())
        super(QView, self).mouseMoveEvent(event)
        
    def mousePressEvent(self, event):
        if event.buttons() == Qt.MidButton:
            self.__dragged = True
            self.__pos = event.pos()
            
    def mouseReleaseEvent(self, event):
        self.__dragged = False
        
    def keepCallout(self):
        self.m_callouts.append(self.m_tooltip)
        self.m_tooltip = Callout(self.m_chart)
    
    def cleanTag(self):
        del self.m_callouts[:]
    
    def tooltip(self, point, state):
        
        if self.m_tooltip == None:
            self.m_tooltip = Callout(self.m_chart)
        
        if state:
            self.m_tooltip.setText("X: {} \nY: {} ".format(round(point.x(), 3), round(point.y(), 3)))
            self.m_tooltip.setAnchor(point)
            self.m_tooltip.setZValue(11)
            self.m_tooltip.updateGeometry()
            self.m_tooltip.show()
        else:
            self.m_tooltip.hide()


class QsciLexerCustomPython(QsciLexerPython):
    
    """Custom Python highter."""
    
    def __init__(self, *args):
        super(QsciLexerCustomPython, self).__init__(*args)
        self.setIndentationWarning(QsciLexerPython.Tabs)
    
    def keywords(self, set: int) -> str:
        if set == 2:
            return "self True False"
        else:
            return QsciLexerPython.keywords(self, set)
    
    def setDefaultFont(self, font: QFont):
        super(QsciLexerCustomPython, self).setDefaultFont(font)
        self.setFont(font, QsciLexerPython.Comment)
        self.setFont(font, QsciLexerPython.DoubleQuotedString)
        self.setFont(font, QsciLexerPython.UnclosedString)
        self.setFont(font, QsciLexerPython.SingleQuotedString)
