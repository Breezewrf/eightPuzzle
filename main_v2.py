import sys
import random
from enum import IntEnum
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGridLayout, QMessageBox
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import Qt


# 用枚举类表示方向
class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class NumberHuaRong(QWidget):
    """ 华容道主体 """

    def __init__(self):
        super().__init__()
        self.blocks = []
        self.zero_row = 0
        self.zero_column = 0
        self.gltMain = QGridLayout()

        self.initUI()

    def initUI(self):
        # 设置方块间隔
        self.gltMain.setSpacing(10)

        self.onInit()

        # 设置布局
        self.setLayout(self.gltMain)
        # 设置宽和高
        self.setFixedSize(400, 400)
        # 设置标题
        self.setWindowTitle('wx数字华容道')
        # 设置背景颜色
        l1 = QtWidgets.QLabel(self)
        # self.setStyleSheet("background-color:yellow;")
        png = QtGui.QPixmap('C:\\Users\\Breeze\\Desktop\\shopBoard_detection\\AdvancedEAST-master\\demo\\001.png')
        l1.setPixmap(png)
        l1.move(100, 40)
        l1.setGeometry(10, 10, 120, 120)
        self.show()

    # 初始化布局
    def onInit(self):
        # 产生顺序数组
        self.numbers = list(range(0, 9))
        self.numbers.append(0)
        print(self.numbers)
        # 将数字添加到二维数组
        for row in range(3):
            self.blocks.append([])
            for column in range(3):
                temp = self.numbers[row * 3 + column]
                # print("temp:{}".format(temp))
                if temp == 0:
                    self.zero_row = row
                    self.zero_column = column
                self.blocks[row].append(temp)
        print("self.blocks:{}".format(self.blocks))
        print(self.zero_column,self.zero_row)
        # 打乱数组
        for i in range(500):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))

        self.updatePanel()

    # 检测按键
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up or key == Qt.Key_W:
            self.move(Direction.UP)
        if key == Qt.Key_Down or key == Qt.Key_S:
            self.move(Direction.DOWN)
        if key == Qt.Key_Left or key == Qt.Key_A:
            self.move(Direction.LEFT)
        if key == Qt.Key_Right or key == Qt.Key_D:
            self.move(Direction.RIGHT)
        self.updatePanel()
        if self.checkResult():
            if QMessageBox.Ok == QMessageBox.information(self, '挑战结果', '恭喜您完成挑战！'):
                self.onInit()

    # 方块移动算法
    def move(self, direction):
        if direction == Direction.UP:  # 上
            if self.zero_row != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1
        if direction == Direction.DOWN:  # 下
            if self.zero_row != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
        if direction == Direction.LEFT:  # 左
            if self.zero_column != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1
        if direction == Direction.RIGHT:  # 右
            if self.zero_column != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column - 1]
                self.blocks[self.zero_row][self.zero_column - 1] = 0
                self.zero_column -= 1

    def updatePanel(self):
        for row in range(3):
            for column in range(3):
                self.gltMain.addWidget(Block(self.blocks[row][column]), row, column)

        self.setLayout(self.gltMain)

    # 检测是否完成
    def checkResult(self):
        # 先检测最右下角是否为0
        if self.blocks[2][2] != 0:
            return False

        for row in range(3):
            for column in range(3):
                # 运行到此处说名最右下角已经为0，pass即可
                if row == 2 and column == 2:
                    pass
                # 值是否对应
                elif self.blocks[row][column] != row * 3 + column + 1:
                    return False

        return True


class Block(QLabel):
    """ 数字方块 """

    def __init__(self, number):
        super().__init__()

        self.number = number
        self.setFixedSize(80, 80)

        # 设置字体
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.setFont(font)

        # 设置字体颜色
        pa = QPalette()
        pa.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(pa)

        # 设置文字位置
        self.setAlignment(Qt.AlignCenter)

        # 设置背景颜色
        if self.number == 0:
            self.setStyleSheet("background-color:white;border-radius: 20%;")
        else:
            self.setStyleSheet("background-color:blue;border-radius: 20%;")
            self.setText(str(self.number))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = NumberHuaRong()
    sys.exit(app.exec_())


