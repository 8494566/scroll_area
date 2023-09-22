# -*- encoding:utf-8 -*-
# ==============================================
# Created on
# Author: 王高亮
# Description: 自适应半透明滚动条
# Time: 2023/9/22 14:50
# ==============================================


from PyQt5 import QtWidgets, QtCore

class SuspendedScrollBar(QtWidgets.QScrollBar):
    def __init__(self, t, parent=None):
        super().__init__(t, parent)
        self.setOrientation(t)

        styleFile = QtCore.QFile("./scrollbar-vertical.qss")
        if styleFile.open(QtCore.QFile.ReadOnly):
            style = str(styleFile.readAll(), encoding='utf-8')
            self.setStyleSheet(style)
        styleFile.close()

        self.setRange(0, 0)
        self.hide()

    def sltRangeChanged(self, min_val, max_val):
        self.setMinimum(min_val)
        self.setRange(0, max_val)
        self.setPageStep(0.75 * (self.height() + max_val))
        if max_val <= 0:
            self.hide()

    def sltValueChangeScrollBar(self, value):
        self.setValue(value)
