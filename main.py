# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, random


class Ui_Widget(object):
    def __init__(self):

        app = QApplication(sys.argv)
        self.windows = QWidget()
        # self.windows.setGeometry()
        self.windows.resize(450, 870)
        self.windows.setObjectName("windows")
        self.windows.setWindowTitle("华容道-1.2")
        self.RClist = QGridLayout(self.windows)
        # self.RClist.setContentsMargins(0, 0, 0, 0)
        self.RClist.setSpacing(0)
        # self.RClist.setGeometry(QRect(500, 400, 860, 960))
        self.RClist.setSizeConstraint(3)
        self.RClist.setObjectName("gridLayout")
        for i in range(line):
            for j in range(clumu):
                # print(j,i)
                self.pushButton = QPushButton(self.windows)
                if (i == a) and (j == b):
                    self.pushButton.setEnabled(False)
                    self.disablebtn = self.pushButton
                    self.disablebtn.setStyleSheet("background-image:url('../apple.png');border:none;")
                else:
                    self.pushButton.setEnabled(True)
                    self.pushButton.setStyleSheet("border:none;background-color:green;")
                self.pushButton.setObjectName("btn" + str(j) + str(i))
                sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
                self.pushButton.setSizePolicy(sizePolicy)
                self.pushButton.setMinimumSize(QSize(100, 100))
                self.pushButton.setFlat(True)
                self.RClist.addWidget(self.pushButton, j, i)
                self.pushButton.clicked.connect(self.movebtn)
                # self.pushButton.setText(str(random.randint(0,16)))
                self.pushButton.setText(str(j) + str(i))
                print(self.pushButton.objectName())
                btnObjList.append(self.pushButton)
        self.btninit()  # 按钮号码初始化
        self.windows.show()
        sys.exit(app.exec_())

    def movebtn(self):
        self.disrow = int(self.disablebtn.objectName()[-2])
        self.discol = int(self.disablebtn.objectName()[-1])
        self.row = int(self.pushButton.sender().objectName()[-2])
        self.col = int(self.pushButton.sender().objectName()[-1])
        if self.row == self.disrow:  # 水平移动
            print("触发按钮的坐标：", self.row, self.col)
            print("空地按钮的坐标：", self.disrow, self.discol)
            if (self.discol - self.col) == 1:  # 空地水平向左移动
                self.RClist.addWidget(self.pushButton.sender(), self.row, self.col + 1)
                self.pushButton.sender().setObjectName("btn" + str(self.row) + str(self.col + 1))
                self.RClist.addWidget(self.disablebtn, self.row, self.col)
                self.disablebtn.setObjectName("btn" + str(self.row) + str(self.col))
            elif (self.col - self.discol) == 1:  # 空地水平向右移动
                self.RClist.addWidget(self.pushButton.sender(), self.row, self.col - 1)
                self.pushButton.sender().setObjectName("btn" + str(self.row) + str(self.col - 1))
                self.RClist.addWidget(self.disablebtn, self.row, self.col)
                self.disablebtn.setObjectName("btn" + str(self.row) + str(self.col))
        if self.col == self.discol:  # 垂直移动
            print("触发按钮的坐标：", self.row, self.col)
            print("空地按钮的坐标：", self.disrow, self.discol)
            print(self.row, self.disrow)
            if (self.disrow - self.row) == 1:  # 空地垂直向上移动
                self.RClist.addWidget(self.pushButton.sender(), self.disrow, self.col)
                self.pushButton.sender().setObjectName("btn" + str(self.disrow) + str(self.col))
                self.RClist.addWidget(self.disablebtn, self.row, self.col)
                self.disablebtn.setObjectName("btn" + str(self.row) + str(self.col))
            elif (self.row - self.disrow) == 1:  # 空地垂直向下移动
                self.RClist.addWidget(self.pushButton.sender(), self.row - 1, self.col)
                self.pushButton.sender().setObjectName("btn" + str(self.row - 1) + str(self.col))
                self.RClist.addWidget(self.disablebtn, self.row, self.col)
                self.disablebtn.setObjectName("btn" + str(self.row) + str(self.col))
        self.winner()
        print("96line", btnObjList)

    def winner(self):  # 赢局遍历
        global times_unm
        times_unm = times_unm + 1
        for _ in btnObjList:
            usedict[_.objectName()] = _.text()
        print(usedict)
        print(times_unm)
        if usedict == winnerdict:
            print("your win!! congratulitions")
            print(usedict, "\n", winnerdict)
            tr = QMessageBox.information(self.windows, "congratulitions:", "恭喜你终于赢了，共计走了 " + str(times_unm) + "  次\n\n",
                                         QMessageBox.Yes)

    def btninit(self):
        print("---btnnum---", li)
        for i in range(line * clumu):
            btnObjList[i].setText(str(li[i]))


if __name__ == "__main__":
    line = 3
    clumu = 3
    times_unm = 0
    usedict = {}  # 用户dict与赢家的dict比较，相同就赢了。
    winnerdict = {'btn00': '0', 'btn10': '3',
                  'btn21': '7', 'btn01': '1', 'btn11': '4', 'btn20': '6', 'btn02': '2', 'btn12': '5', 'btn22': '8'}
    a = random.randint(0, line - 1)
    b = random.randint(0, clumu - 1)
    print(a, b)
    li = list(range(line * clumu))
    random.shuffle(li)
    btnObjList = list()  # 按钮对象列表
    print(btnObjList)
    win = Ui_Widget()