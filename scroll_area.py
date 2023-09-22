# -*- encoding:utf-8 -*-
# ==============================================
# Created on
# Author: 王高亮
# Description: 自适应半透明滚动条
# Time: 2023/9/22 14:50
# ==============================================

from PyQt5 import QtWidgets, QtCore
from common_module.common_ui.scroll_area.suspended_scroll_bar import SuspendedScrollBar


class ScrollArea(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pVertScrollBar = None
        self.init()

    def init(self):
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.pVertScrollBar = SuspendedScrollBar(QtCore.Qt.Vertical, self)

        self.verticalScrollBar().valueChanged.connect(self.pVertScrollBar.sltValueChangeScrollBar)
        self.pVertScrollBar.valueChanged.connect(self.sltValueChangeWidget)
        self.verticalScrollBar().rangeChanged.connect(self.pVertScrollBar.sltRangeChanged)

    def resizeEvent(self, e):
        iX = self.width() - 10
        self.pVertScrollBar.setGeometry(iX, 0, 10, self.height() - 2)
        if not self.pVertScrollBar.maximum():
            self.pVertScrollBar.setMinimum(1)
        return super().resizeEvent(e)

    def enterEvent(self, e):
        if self.pVertScrollBar.maximum() > 0:
            self.pVertScrollBar.show()
        return super().enterEvent(e)

    def leaveEvent(self, e):
        self.pVertScrollBar.hide()
        return super().leaveEvent(e)

    def sltValueChangeWidget(self, value):
        self.verticalScrollBar().setValue(value)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QWidget()

    window = QtWidgets.QMainWindow()

    pLayout = QtWidgets.QGridLayout()
    for i in range(30):
        button = QtWidgets.QPushButton("名字{}".format(i))
        button.setFixedSize(200, 30)
        pLayout.addWidget(button)

    widget.setLayout(pLayout)

    scrollArea = ScrollArea(window)
    scrollArea.setWidget(widget)

    window.setCentralWidget(scrollArea)

    window.show()

    sys.exit(app.exec_())
