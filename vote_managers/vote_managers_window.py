# -*- encoding:utf-8 -*-
# ==============================================
# Created on 
# Author: 王高亮
# Description: 投票器管理设置
# Time: 2023/09/21 15:00
# ==============================================

import os
from PyQt5 import QtCore, QtWidgets
from functools import partial
from common_module.datalogic.misc import getCCAppDataPath
from common_module.datalogic.common_download import CommonDownload
from common_module.common_ui.uicontrols.x_web_image import XWebImage
from common_module.common_ui.scroll_area.scroll_area import ScrollArea

ROW, COLUMN = 2, 5


class Protocols():
    SID = 43773
    END_CID = 6


class VoteManagersWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(VoteManagersWindow, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)

        self._downloader = CommonDownload(self, None)
        self._rankListStyleButton = {}
        self._urlToStyleButton = {}

        # 初始化鼠标按下的坐标（相对于QWidget的左上角）
        self.mousePressPos = None
        # 初始化QWidget的位置（相对于parent）
        self.position = None

        self.resultStyleSheetDict = {} # 保存主题对应的id

        self.setFixedSize(560, 545)

        self.bg = QtWidgets.QWidget(self)
        self.bg.setObjectName("bg")
        self.bg.setFixedSize(self.size())

        title = QtWidgets.QLabel(self.bg)
        title.setObjectName("title")
        title.setGeometry(15, 15, 220, 20)
        title.setText("记票器设置")

        closeButton = XWebImage(self.bg)
        closeButton.setGeometry(self.bg.width() - 30, 15, 15, 15)
        closeButton.setClickable(True)
        closeButton.setFilePath("z/gamelive/vote_managers/close.png")
        closeButton.clicked.connect(self.close)

        messageTitle = QtWidgets.QLabel(self.bg)
        messageTitle.setObjectName("outlineTitle")
        messageTitle.setGeometry(60, 55, 82, 18)
        messageTitle.setText("添加信息")

        voteMotifTitle = QtWidgets.QLabel(self.bg)
        voteMotifTitle.setObjectName("mainBodyTitle")
        voteMotifTitle.setGeometry(68, 112, 82, 18)
        voteMotifTitle.setText("投票主题：")

        self.voteMotifComboBox = QtWidgets.QComboBox(self.bg)
        self.voteMotifComboBox.setView(QtWidgets.QListView())
        self.voteMotifComboBox.setObjectName("motifComboBox")
        self.voteMotifComboBox.setGeometry(279, 102, 226, 36)
        self.voteMotifComboBox.setMaxVisibleItems(10)
        self.voteMotifComboBox.addItem("选中的主题 1")
        self.voteMotifComboBox.addItem("选中的主题 2")
        self.voteMotifComboBox.addItem("选中的主题 3")

        voteRuleTitle = QtWidgets.QLabel(self.bg)
        voteRuleTitle.setObjectName("mainBodyTitle")
        voteRuleTitle.setGeometry(68, 162, 132, 18)
        voteRuleTitle.setText("投票规则（单选）:")

        self.multipleChoiceButton = QtWidgets.QRadioButton("1人1票", self.bg)
        self.multipleChoiceButton.setGeometry(279, 165, 132, 18)
        self.multipleChoiceButton.setChecked(True)

        radioButton = QtWidgets.QRadioButton("不限制", self.bg)
        radioButton.setGeometry(279 + 132, 165, 132, 18)

        voteTimeTitle = QtWidgets.QLabel(self.bg)
        voteTimeTitle.setObjectName("mainBodyTitle")
        voteTimeTitle.setGeometry(68, 212, 80, 18)
        voteTimeTitle.setText("计票时间：")

        self.voteTimeComboBox = QtWidgets.QComboBox(self.bg)
        self.voteTimeComboBox.setView(QtWidgets.QListView())
        self.voteTimeComboBox.setObjectName("motifComboBox")
        self.voteTimeComboBox.setGeometry(279, 202, 93, 36)
        self.voteTimeComboBox.setMaxVisibleItems(10)
        self.voteTimeComboBox.addItems(["1", "5", "10", "15", "30", "60", "自定义"])
        self.voteTimeComboBox.currentIndexChanged.connect(self.handleCurrentIndexChanged)

        voteTimeTitle2 = QtWidgets.QLabel(self.bg)
        voteTimeTitle2.setGeometry(384, 212, 80, 18)
        voteTimeTitle2.setText("分钟后封盘")
        voteTimeTitle2.setStyleSheet("font-family: 'Microsoft YaHei';color: #18181A; font-size: 16px;")

        styleSheetTitle = QtWidgets.QLabel(self.bg)
        styleSheetTitle.setObjectName("outlineTitle")
        styleSheetTitle.setGeometry(60, 278, 82, 18)
        styleSheetTitle.setText("选择样式")

        self.styleSheetBg = QtWidgets.QWidget(self.bg)
        self.styleSheetBg.setObjectName("styleSheetBg")
        self.styleSheetBg.setGeometry(60, 316, 438, 145)

        styleSheetWindow = QtWidgets.QWidget(self.styleSheetBg)
        styleSheetWindow.setObjectName("styleSheetWindow")

        self.styleSheetPLayout = QtWidgets.QGridLayout(self.bg)
        self.styleSheetGroup = QtWidgets.QButtonGroup(self.bg)
        for i in range(3):
            for j in range(4):
                button = QtWidgets.QPushButton("名字{}".format(i))
                button.setFixedSize(90, 105)
                self.styleSheetPLayout.addWidget(button, i, j)
                self.styleSheetGroup.addButton(button)

        self.styleSheetGroup.setExclusive(True)
        styleSheetWindow.setLayout(self.styleSheetPLayout)

        scrollArea = ScrollArea()
        scrollArea.setObjectName("styleSheetScrollArea")
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(styleSheetWindow)
        scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)

        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addWidget(scrollArea)

        self.styleSheetBg.setLayout(mainLayout)

        restoreButton = QtWidgets.QPushButton(self.bg)
        restoreButton.setObjectName("restoreButton")
        restoreButton.setGeometry(55, 481, 204, 44)
        restoreButton.setText("恢复默认")
        restoreButton.setCursor(QtCore.Qt.PointingHandCursor)
        restoreButton.clicked.connect(self._restoreClicked)

        accomplishButton = QtWidgets.QPushButton(self.bg)
        accomplishButton.setObjectName("accomplishButton")
        accomplishButton.setGeometry(301, 481, 204, 44)
        accomplishButton.setText("完成设置")
        accomplishButton.setCursor(QtCore.Qt.PointingHandCursor)
        accomplishButton.clicked.connect(self._accomplishClicked)

        self.initQss()


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # 记录鼠标按下的坐标和QWidget的位置
            self.mousePressPos = event.globalPos()
            self.position = self.pos()

    def mouseMoveEvent(self, event):
        if self.mousePressPos is not None:
            # 计算QWidget的移动距离
            delta = event.globalPos() - self.mousePressPos
            # 更新QWidget的位置
            self.move(self.position + delta)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # 清空鼠标按下的坐标和QWidget的位置
            self.mousePressPos = None
            self.position = None

    def handleCurrentIndexChanged(self, index):
        if self.voteTimeComboBox.currentIndex() == self.voteTimeComboBox.count() - 1:
            self.voteTimeComboBox.setEditable(True)
            self.voteTimeComboBox.setCurrentText("")
        else:
            self.voteTimeComboBox.setEditable(False)

    def initQss(self):
        self.setStyleSheet("""
           QWidget#bg
           {
               image: url(z/gamelive/vote_managers/vote_managers_bg.png);
           }
           QLabel#title
           {
                font: 12px "Microsoft Yahei";
                color: #18181A;
           }
           QLabel#outlineTitle
           {
                font-family: 'Microsoft YaHei'; font-weight: bold;
                color: #333333;
                border-top: none;
                border-right: none;
                border-left: 3px solid #0069FF;
                border-bottom: none;
                font-size: 18px;
           }
           QLabel#mainBodyTitle
           {
                font-family: 'Microsoft YaHei';
                color: #616166;
                font-size: 16px;
           }
            QComboBox#motifComboBox {
                border-radius: 5px;
                border: 1px solid #CCCCCC;
                min-width: 6em;
            }
            QComboBox#motifComboBox:hover {
                border-color: #0069FF;
            } 
            QComboBox#motifComboBox::drop-down{
                border-style: none;
            }
            QComboBox#motifComboBox::down-arrow, QComboBox#motifComboBox::down-arrow:off {
                image: url(z/gamelive/vote_managers/down_arrow.png);
                padding-right: 5px;
            }
            
            QComboBox#motifComboBox::down-arrow:on {
                image: url(z/gamelive/vote_managers/up_arrow.png); 
                padding-right: 5px;
            }
            QComboBox#motifComboBox QAbstractItemView {
                outline: none;
                border-radius: 5px;
                background-color: #FFFFFF;
                border: 1px solid gray;
                color: #616166;
                font-family: 'Microsoft YaHei';
                font-size: 16px;
                padding: 2px;
            }
            QComboBox#motifComboBox QAbstractItemView::item { 
                min-height: 36; min-width: 226; 
            }
            QComboBox#motifComboBox QAbstractItemView::item:hover { 
                border-radius: 5px;
                background-color: #F2F3F5;
                color: #18181A;
            }
            QComboBox QAbstractItemView::item::selected {
                border-radius: 5px;
                background-color: #F2F3F5;
                color: #18181A;
            }
            QWidget#styleSheetBg
           {
               background-color: #fafafa; 
               border-radius: 5px;
           }
           QWidget#styleSheetWindow
           {
               background-color: rgba(0, 0, 0, 0);
           }
           QPushButton#restoreButton
           {
                font-family: 'Microsoft YaHei';
                color: #0069FF;
                font-size: 16px;
                border-radius: 20px;
                border: 1px solid #0069FF;
           }
           QPushButton#accomplishButton
           {
                font-family: 'Microsoft YaHei';
                color: #FFFFFF;
                font-size: 16px;
                border-radius: 20px;
                background-color: #0069FF;
           }
           QScrollArea#styleSheetScrollArea
           {
                background-color: transparent;
           }
        """)

    def setStyleSheetWindow(self, msg):
        theme = msg.get("theme", [])
        self.resultStyleSheetDict = {item['name']: item['id'] for item in theme}

        resultStyleSheetList = [item['name'] for item in theme]
        self.voteMotifComboBox.clear()
        self.voteMotifComboBox.addItems(resultStyleSheetList)

    def setStyleSheetButton(self, rankListStyle):
        # 清空布局
        self._rankListStyleButton = {}
        self._urlToStyleButton = {}
        for i in reversed(range(self.styleSheetPLayout.count())):
            item = self.styleSheetPLayout.itemAt(i)

            if isinstance(item.widget(), QtWidgets.QPushButton):
                self.styleSheetPLayout.takeAt(i)
                item.widget().deleteLater()

        # 从按钮组中删除所有按钮
        for button in self.styleSheetGroup.buttons():
            self.styleSheetGroup.removeButton(button)

        n = 4
        for i in range(0, len(rankListStyle), n):
            subList = rankListStyle[i:i + n]
            for j, val in enumerate(subList):
                styleId = val.get("style_id", "")
                thumbnailUrl = val.get("thumbnail", "")
                path = os.path.join(getCCAppDataPath(), "images", "VoteManagersWindow", str(styleId))
                self._downloader.addDownTask(thumbnailUrl, path, False, self._onDownloadFinished)

                button = QtWidgets.QPushButton()
                button.setFixedSize(90, 105)
                button.setFlat(True)
                button.setCheckable(True)
                if i == 0 and j == 0:
                    button.setChecked(True) # 默认设置第一个为选中状态
                self.styleSheetPLayout.addWidget(button, i, j)
                self.styleSheetGroup.addButton(button)
                self._rankListStyleButton[button] = button
                self._urlToStyleButton[path] = button

    def _onDownloadFinished(self, result, url, filePath):
        if not result:
            return
        button = self._urlToStyleButton.get(filePath, None)
        if not button:
            return
        path = filePath.replace("\\", "/") # 换反斜杠 兼容
        setStylPushButtonPath = f"QPushButton {{ background-image: url({path});}} QPushButton:pressed, QPushButton:checked {{ background-image: url({path}); border: 2px solid #73ADFF;}}"
        button.setStyleSheet(setStylPushButtonPath)


    def _restoreClicked(self):
        self.voteMotifComboBox.setCurrentIndex(0)
        self.voteTimeComboBox.setCurrentIndex(0)
        self.multipleChoiceButton.setChecked(True)
        button = list(self._rankListStyleButton.keys())[0]
        if button:
            button.setChecked(True)

    def _accomplishClicked(self):
        pass


if __name__ == "__main__":
    import sys

    from common_module.datalogic import misc
    res = misc.loadResForDebug()

    app = QtWidgets.QApplication(sys.argv)
    model = VoteManagersWindow()
    model.show()
    sys.exit(app.exec_())
