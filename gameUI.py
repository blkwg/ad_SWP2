from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGroupBox, QLineEdit
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QImage, QBrush
import game
import time
import traceback


class variables():
    def __init__(self):
        self.status = None
        self.Hscore = 0
        self.score = 0
        self.length = 0
        self.com_dataList = [0, 1, 2]
        self.values = [None, 0, 0, 0, [0, 1, 2], None]
        #stat, Hscore, score, length, com_dataList, com

    def changeVar(self, valueList):
        self.status = valueList[0]
        self.Hscore = valueList[1]
        self.score = valueList[2]
        self.length = valueList[3]
        self.com_dataList = valueList[4]

        if self.Hscore < self.score:
            self.Hscore = self.score




def ErrorLog(error: str):
    current_time = time.strftime("%Y.%m.%d/%H:%M:%S", time.localtime(time.time()))
    with open("Log.txt", "a") as f:
        f.write(f"[{current_time}] - {error}\n")


class QPushButton(QPushButton):
    def __init__(self, text, height, width, callback):
        super().__init__()
        self.setText(text)
        self.clicked.connect(callback)

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
    # 묵찌빠 함수 내에서 쓰일 변수 정의
    



    def __init__(self, parent=None):
        super().__init__(parent)




        # layout 설정
        self.mainLayout = QGridLayout()
        self.row1Layout = QGridLayout()
        self.row2Layout = QGridLayout()
        self.row3Layout = QGridLayout()
        self.setLayout(self.mainLayout)


        # 배경화면 설정
        # wallpaper = QImage("wallpaper.jpg")
        # wallpaper.scaled(QSize())
        # palette = QPalette()
        # palette.setBrush(10, QBrush(wallpaper))
        # self.setPalette(palette)

        


        # row1

        # 공격/수비 표시
        self.OffOrDef = QLabelBox(['공격'], 60, 90)

        # 현재 상태 표시
        self.display = QLineEdit(self) # 현재 상태 표시
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setReadOnly(True)
        self.display.setMaximumHeight(100)

        # 나가기 버튼
        self.exit = QPushButton("나가기", 50, 70, self.exitButtonClicked)

        # Layout
        self.row1Layout.addWidget(self.OffOrDef, 0, 0)
        self.row1Layout.addWidget(self.display, 0, 1)
        self.row1Layout.addWidget(self.exit, 0, 2)

        self.mainLayout.addLayout(self.row1Layout, 0, 0)


        # row 2

        # 컴퓨터가 이전 턴에 낸 모양
        self.comLastShape = self.shapeShowGroupBox("computer", "white.png", 160, 160)
        # 플레이어가 이전 턴에 낸 모양
        self.playerLastShape = self.shapeShowGroupBox("player", "white.png", 160, 160)

        self.lastShapeLayout = QGridLayout()
        self.lastShapeLayout.addWidget(self.comLastShape, 0, 0)
        self.lastShapeLayout.addWidget(self.playerLastShape, 2, 0)

        # 컴퓨터가 현재 턴에 낸 모양
        self.comShape = self.shapeShowGroupBox("", "white.png", 300, 300)

        # high score / score / game streak 표시
        self.informationLayout = self.informationGroupBoxs()

        # Layout
        self.row2Layout.addLayout(self.lastShapeLayout, 0, 0, 3, 1)
        self.row2Layout.addWidget(self.comShape, 0, 1, 2, 1)
        self.row2Layout.addLayout(self.informationLayout, 0, 5, 2, 1)

        self.mainLayout.addLayout(self.row2Layout, 1, 0)


        # row 3

        # 묵찌빠 select 버튼
        self.muk = self.shapeSelectButton("묵.png", 150, 150, self.mukButtonClicked)
        self.jji = self.shapeSelectButton("찌.png", 150, 150, self.jjiButtonClicked)
        self.ppa = self.shapeSelectButton("빠.png", 150, 150, self.ppaButtonClicked)

        # Layout
        self.row3Layout.addWidget(self.muk, 0, 0)
        self.row3Layout.addWidget(self.jji, 0, 1)
        self.row3Layout.addWidget(self.ppa, 0, 2)

        self.mainLayout.addLayout(self.row3Layout, 2, 0)


        self.setWindowTitle('묵찌빠 게임')
        self.setGeometry(500, 150, 800, 800)


    # 묵찌빠 모양을 표시하는 groupbox
    def shapeShowGroupBox(self, title, image, height, width):
        self.showGroupBox = QGroupBox(title, height, width)
        self.vbox = QVBoxLayout()
        self.pixmapLabel = QPixmapLabel(image, height - 20, width - 20)
        self.vbox.addWidget(self.pixmapLabel)
        self.showGroupBox.setLayout(self.vbox)

        return self.showGroupBox

    # 정보들을 표시하는 'groupbox의 집합' layout
    def informationGroupBoxs(self):
        gameVars = variables()
        self.groupBoxLayout = QGridLayout()

        groupboxList = [["High Score", "%d" %(gameVars.Hscore)], ["Score", "%d" %(gameVars.score)], ["Game Streak", "%d" %(gameVars.length)]]
        for content in groupboxList:
            self.groupbox = QLabelBox(content, 130, 150)
            self.groupBoxLayout.addWidget(self.groupbox, groupboxList.index(content), 0)

        return self.groupBoxLayout

    # 묵찌빠 선택 button
    def shapeSelectButton(self, image, height, width, buttonClicked):
        self.button = QPushButton("", height, width, buttonClicked)
        self.button.setIcon(QIcon(image))
        self.button.setIconSize(QSize(130, 130))

        return self.button

    # buttonClicke funtions

    # 나가기 button 클릭했을 때
    def exitButtonClicked(self):

        button = self.sender()
        key = button.text()
        self.display.setText(key)

    # 묵 button 클릭
    def mukButtonClicked(self):
        gameVars = variables()
        try:

            button = self.sender()
            shape = 0
            muk = game.mukjjippa()
#def ingame(self, ad_status, hand_signal, score, now, com_dataList):
            result = muk.ingame(gameVars.values[0], shape, gameVars.values[1], gameVars.values[3], gameVars.values[4])
            gameVars.score = result[0]
            self.comLastShape = self.comShape
            self.playerLastShape = self.shapeShowGroupBox("player", "찌.png", 160, 160)
            if result[1] == 0:
                self.comShape = self.shapeShowGroupBox("", "묵.png", 300, 300)
            elif result[1] == 1:
                self.comShape = self.shapeShowGroupBox("", "찌.png", 300, 300)
            elif result[1] == 2:
                self.comShape = self.shapeShowGroupBox("", "빠.png", 300, 300)
            print(result)


            # key = button.text()

        except Exception:
            err = traceback.format_exc()
            ErrorLog(str(err))


    # 찌 button 클릭
    def jjiButtonClicked(self):
        gameVars = variables()
        try:
            button = self.sender()
            shape = 1
            jji = game.mukjjippa()
            result = jji.ingame(gameVars.values[0], shape, gameVars.values[1], gameVars.values[3], gameVars.values[4])
            gameVars.score = result[0]
            self.comLastShape = self.comShape
            self.playerLastShape = self.shapeShowGroupBox("player", "찌.png", 160, 160)
            if result[1] == 0:
                self.comShape = self.shapeShowGroupBox("", "묵.png", 300, 300)
            elif result[1] == 1:
                self.comShape = self.shapeShowGroupBox("", "찌.png", 300, 300)
            elif result[1] == 2:
                self.comShape = self.shapeShowGroupBox("", "빠.png", 300, 300)
            print(result)

            # key = button.text()

        except Exception:
            err = traceback.format_exc()
            ErrorLog(str(err))


    # 빠 button 클릭
    def ppaButtonClicked(self):
        gameVars = variables()
        try:
            button = self.sender()
            shape = 2
            ppa = game.mukjjippa()
            result = ppa.ingame(gameVars.values[0], shape, gameVars.values[1], gameVars.values[3], gameVars.values[4])
            gameVars.score = result[0]
            self.comLastShape = self.comShape
            self.playerLastShape = self.shapeShowGroupBox("player", "빠.png", 160, 160)
            if result[1] == 0:
                self.comShape = self.shapeShowGroupBox("", "묵.png", 300, 300)
            elif result[1] == 1:
                self.comShape = self.shapeShowGroupBox("", "찌.png", 300, 300)
            elif result[1] == 2:
                self.comShape = self.shapeShowGroupBox("", "빠.png", 300, 300)
            print(result)

            # key = button.text()
        except Exception:
            err = traceback.format_exc()
            ErrorLog(str(err))



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mjpGame = Game()
    mjpGame.show()
    sys.exit(app.exec_())
