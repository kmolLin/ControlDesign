# -*- coding: utf-8 -*-
from sys import exit
from .QtModules import (
    QApplication,
)
from .mainwindow import MainWindow

__all__ = ['main']

def main():
    app = QApplication([])
    run = MainWindow()
    run.show()
    exit(app.exec_())
