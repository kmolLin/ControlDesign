# -*- coding: utf-8 -*-

"""
Module implementing text_editor.
"""

from core.QtModules import (
    pyqtSlot,
    QDialog,
    QTextCursor,
    QFileDialog,
    QWidget,
)
from core.text_editor import TextEditor
from core.loggingHandler import XStream
from core.cont2discdlg import c2ddlg
from .Ui_symbolic import Ui_Dialog
from .rpsymbolic.dialogBlock import DialogBlock


class SymbolicBlock(QWidget, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        super(SymbolicBlock, self).__init__(parent)
        self.setupUi(self)
        self.text_editor = TextEditor(self)
        self.editor_layout.insertWidget(1, self.text_editor)
        # self.ma = parent.XXX
        self.addch = parent.addChartFromXY
        
        #Console
        self.console.setFont(self.text_editor.font)
        XStream.stdout().messageWritten.connect(self.__appendToConsole)
        XStream.stderr().messageWritten.connect(self.__appendToConsole)
        self.destroyed.connect(XStream.back)
    
    @pyqtSlot(str)
    def __appendToConsole(self, log):
        """After inserted the text, move cursor to end."""
        self.console.moveCursor(QTextCursor.End)
        self.console.insertPlainText(log)
        self.console.moveCursor(QTextCursor.End)
    
    def getanswer(self, block):
        print(block)
        self.calcendBlock = block
    
    def modelname(self, name):
        self.modeln = name
    
    def impuseplot(self):
        print(type(self.calcendBlock))
    
    def stepplot(self):
        pass
    
    @pyqtSlot()
    def on_calcblock_btn_clicked(self):
        script = self.text_editor.text()
        
        def run():
            block = DialogBlock
            answer = self.getanswer
            model = self.modelname
            exec(script)
        from threading import Thread
        Thread(target=run).start()
    
    @pyqtSlot()
    def on_loadfile_btn_clicked(self):
        file, _ = QFileDialog.getOpenFileName(self, 'open file','', 'Python Script(*.py)')
        if not file :
            return
        with open(file, "r") as f:
            self.text_editor.setText(f.read())
    
    @pyqtSlot()
    def on_savefile_btn_clicked(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save file', '', 'Python Script(*.py)')
        if not filename:
            return
        with open(filename, 'w') as f:
            f.write(self.text_editor.text())
    
    @pyqtSlot()
    def on_signal_btn_clicked(self):
        dlg = c2ddlg(self.calcendBlock)
        dlg.show()
        if not dlg.exec_():
            return
        getdata = dlg.get
        self.addch(self.modeln, getdata[0], getdata[1])
