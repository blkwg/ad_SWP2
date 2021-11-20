from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGroupBox, QTextEdit
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap

class QPushButton(QPushButton):
    def __init__(self, text, height, width):
        super().__init__()
        self.setText(text)

        # QPushButton 크기설정
        self.setMaximumHeight(height)
        self.setMaximumWidth(width)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

class QLabelBox(QGroupBox): # Label들로만 이루어진 GroupBox
    def __init__(self, textList, height, width):
        super().__init__()

        # GroupBox에 Label들 추가
        self.vbox = QVBoxLayout()
        for text in textList:
            self.show = QLabel(text)
            self.vbox.addWidget(self.show)

        self.setLayout(self.vbox)

        # LabelBox 크기설정
        self.setMaximumHeight(height)
        self.setMaximumWidth(width)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

class QGroupBox(QGroupBox):
    def __init__(self, title, height, width):
        super().__init__()
        self.setTitle(title)

        # GroupBox 크기설정
        self.setMaximumHeight(height)
        self.setMaximumWidth(width)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

class QPixmapLabel(QLabel): # image 크기만 조정가능. PixmapLabel 크기는 class 밖에서 따로 조정.
    def __init__(self, image, image_height, image_width):
        super().__init__()
        self.comLastShape = QLabel(self)

        # image 크기설정
        pixmap = QPixmap(image)
        pixmap = pixmap.scaledToHeight(image_height)
        pixmap = pixmap.scaledToWidth(image_width)

        self.setPixmap(QPixmap(pixmap))

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


class Game(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.mainLayout = QGridLayout()
        self.row1Layout = QGridLayout()
        self.row2Layout = QGridLayout()
        self.row3Layout = QGridLayout()
        self.setLayout(self.mainLayout)


        # row1

        # 공격/수비 표시
        self.OffOrDef = QLabelBox(['공격'], 60, 90)

        # 현재 상태 표시
        self.display = QTextEdit(self) # 현재 상태 표시
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaximumHeight(90)

        # 나가기 버튼
        self.exit = QPushButton("나가기", 50, 70)

        # Layout
        self.row1Layout.addWidget(self.OffOrDef, 0, 0)
        self.row1Layout.addWidget(self.display, 0, 1)
        self.row1Layout.addWidget(self.exit, 0, 2)

        self.mainLayout.addLayout(self.row1Layout, 0, 0)


        # row 2

        # 컴퓨터가 이전 턴에 낸 모양
        self.comLastShape = self.shapeShowGroupBox("computer", "묵.png", 160, 160)
        # 플레이어가 이전 턴에 낸 모양
        self.playerLastShape = self.shapeShowGroupBox("player", "찌.png", 160, 160)

        self.lastShapeLayout = QGridLayout()
        self.lastShapeLayout.addWidget(self.comLastShape, 0, 0)
        self.lastShapeLayout.addWidget(self.playerLastShape, 2, 0)

        # 컴퓨터가 현재 턴에 낸 모양
        self.comShape = self.shapeShowGroupBox("", "빠.png", 300, 300)

        # high score / score / game streak 표시
        self.informationLayout = self.informationGroupBoxs()

        # Layout
        self.row2Layout.addLayout(self.lastShapeLayout, 0, 0, 3, 1)
        self.row2Layout.addWidget(self.comShape, 0, 1, 2, 1)
        self.row2Layout.addLayout(self.informationLayout, 0, 5, 2, 1)

        self.mainLayout.addLayout(self.row2Layout, 1, 0)


        # row 3

        # 묵찌빠 select 버튼
        self.묵 = self.shapeSelectButton("묵.png", 150, 150)
        self.찌 = self.shapeSelectButton("찌.png", 150, 150)
        self.빠 = self.shapeSelectButton("빠.png", 150, 150)

        # Layout
        self.row3Layout.addWidget(self.묵, 0, 0)
        self.row3Layout.addWidget(self.찌, 0, 1)
        self.row3Layout.addWidget(self.빠, 0, 2)

        self.mainLayout.addLayout(self.row3Layout, 2, 0)


        self.setWindowTitle('묵찌빠 게임')
        self.setGeometry(500, 150, 800, 800)


    # 묵찌빠 모양을 표시하는 groupbox
    def shapeShowGroupBox(self, title, image, height, width):
        self.showGroupBox = QGroupBox(title, height, width)
        self.vbox = QVBoxLayout()
        self.pixmapLabel = QPixmapLabel(image, height - 10, width - 10)
        self.vbox.addWidget(self.pixmapLabel)
        self.showGroupBox.setLayout(self.vbox)

        return self.showGroupBox

    # 정보들을 표시하는 'groupbox의 집합' layout
    def informationGroupBoxs(self):
        self.groupBoxLayout = QGridLayout()

        groupboxList = [["High Score", '0'], ["Score", '0'], ["Game Streak", '0']]
        for content in groupboxList:
            self.groupbox = QLabelBox(content, 130, 150)
            self.groupBoxLayout.addWidget(self.groupbox, groupboxList.index(content), 0)

        return self.groupBoxLayout

    # 묵찌빠 선택 button
    def shapeSelectButton(self, image, height, width):
        self.button = QPushButton("", height, width)
        # self.button.setStyleSheet("background-image : url({0});".format(image))
        self.button.setIcon(QtGui.QIcon(image))
        self.button.setIconSize(QSize(130, 130))

        return self.button


    def buttonClicked(self):

        if self.display.text() == 'Error!':
            self.display.setText("")

        button = self.sender()
        key = button.text()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())