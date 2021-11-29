from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGroupBox, QLineEdit
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QImage, QBrush
import time
import sys
import game
from main import ScoreDB
import traceback


def ErrorLog(error: str):
    current_time = time.strftime("%Y.%m.%d/%H:%M:%S", time.localtime(time.time()))
    with open("Log.txt", "a") as f:
        f.write(f"[{current_time}] - {error}\n")

class QPushButton(QPushButton):
    def __init__(self, text, image, height, width, callback):
        super().__init__()
        self.setText(text)

        # QPushButton image setting
        self.setIcon(QIcon(image))
        self.setIconSize(QSize(height - 15, width - 15))

        # QPushButton size setting
        self.setMaximumHeight(height)
        self.setMaximumWidth(width)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.clicked.connect(callback)

class QLabelBox(QGroupBox): # Label들로만 이루어진 GroupBox
    def __init__(self, textList, height, width):
        super().__init__()

        # GroupBox에 Label들 추가
        self.vbox = QVBoxLayout()
        for num in range(len(textList)):
            self.show = QLabel(textList[num])
            self.vbox.addWidget(self.show)

        self.setLayout(self.vbox)

        # LabelBox 크기설정
        self.setMaximumHeight(height)
        self.setMaximumWidth(width)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

class QInformationGroupBox(QGroupBox): # information 표시하는 GroupBox는 아예 class로 만듦
    def __init__(self, textList, height, width):
        super().__init__()

        # GroupBox에 Label들 추가
        self.vbox = QVBoxLayout()
        for num in range(len(textList)):
            self.show = QLabel(textList[num])
            self.vbox.addWidget(self.show)

            if num == 0:
                font = self.show.font()
                font.setPointSize(font.pointSize() + 2)
                self.show.setFont(font)
            else:
                font = self.show.font()
                font.setPointSize(font.pointSize() + 6)
                self.show.setFont(font)

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

        self.setWindowTitle('묵찌빠 게임')
        self.setGeometry(500, 150, 800, 750)

        # layout setting
        self.mainLayout = QGridLayout()
        self.row1Layout = QGridLayout()
        self.row2Layout = QGridLayout()
        self.row3Layout = QHBoxLayout()
        self.row3Layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.mainLayout)

        #game values
        self.ad_status = None
        self.score = 0
        self.now = 0
        self.com_dataList = [0, 1, 2]
        self.current_score = 0


        # images
        self.mukImage = "image/mjp/묵.png"
        self.jjiImage = "image/mjp/찌.png"
        self.ppaImage = "image/mjp/빠.png"

        self.offenceImage = "image/OfforDef/공격.png"
        self.defenceImage = "image/OfforDef/방어.png"

        newGameImage = "image/재시작.png"
        exitImage = "image/종료.png"
        self.initialImage = "image/투명.png" # 처음 시작할 때 나오는 투명 배경
        questionImage = "image/물음표.png"
        # wallpaperImage = "image/wallpaper.jpg"

        # wallpaper setting
        # wallpaper = QImage("wallpaper.jpg")
        # wallpaper.scaled(QSize())
        # palette = QPalette()
        # palette.setBrush(10, QBrush(wallpaper))
        # self.setPalette(palette)


        # row1

        # 공격/수비 표시
        self.OffOrDef = self.showImageGroupBox("", self.offenceImage, 90, 90)

        # 현재 상태 표시
        self.display = QLineEdit("게임을 시작합니다. 가위바위보 중 하나를 선택하세요.")
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setReadOnly(True)
        self.display.setMaximumHeight(80)

        font = self.display.font()
        font.setPointSize(font.pointSize() + 2)
        self.display.setFont(font)

        # 새로운 게임
        self.newGame = QPushButton("", newGameImage, 70, 70, self.newGameButtonClicked)

        # 나가기 버튼
        self.exit = QPushButton("", exitImage, 70, 70, self.exitButtonClicked)

        # Layout
        self.row1Layout.addWidget(self.OffOrDef, 0, 0)
        self.row1Layout.addWidget(self.display, 0, 1)
        self.row1Layout.addWidget(self.newGame, 0, 2)
        self.row1Layout.addWidget(self.exit, 0, 3)

        self.mainLayout.addLayout(self.row1Layout, 0, 0)


        # row 2

        # 컴퓨터가 이전 턴에 낸 모양
        self.comLastShape = self.showImageGroupBox("computer", self.initialImage, 160, 160)

        # 플레이어가 이전 턴에 낸 모양
        self.playerLastShape = self.showImageGroupBox("player", self.initialImage, 160, 160)

        self.lastShapeLayout = QGridLayout()
        self.lastShapeLayout.addWidget(self.comLastShape, 0, 0)
        self.lastShapeLayout.addWidget(self.playerLastShape, 2, 0)

        # 컴퓨터의 현재 턴
        self.comShape = self.showImageGroupBox("", questionImage, 300, 300)

        # high score / score / game streak 표시
        self.informationLayout = QGridLayout()

        groupboxList = [["High Score", '%d' % self.score], ["Score", '%d' % self.current_score], ["Game Streak", '%d' % self.now]]
        for content in groupboxList:
            self.groupbox = QInformationGroupBox(content, 130, 150)
            self.informationLayout.addWidget(self.groupbox, groupboxList.index(content), 0)

        # Layout
        self.row2Layout.addLayout(self.lastShapeLayout, 0, 0, 3, 1)
        self.row2Layout.addWidget(self.comShape, 0, 1, 2, 1)
        self.row2Layout.addLayout(self.informationLayout, 0, 5, 2, 1)

        self.mainLayout.addLayout(self.row2Layout, 1, 0)


        # row 3

        # 묵찌빠 선택 버튼
        self.muk = QPushButton("", self.mukImage, 150, 150, self.mukButtonClicked)
        self.jji = QPushButton("", self.jjiImage, 150, 150, self.jjiButtonClicked)
        self.ppa = QPushButton("", self.ppaImage, 150, 150, self.ppaButtonClicked)

        self.shapeGroupBox = QGroupBox("", 170, 550)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.muk)
        self.hbox.addStretch(2)
        self.hbox.addWidget(self.jji)
        self.hbox.addStretch(2)
        self.hbox.addWidget(self.ppa)

        self.shapeGroupBox.setLayout(self.hbox)

        # Layout
        self.row3Layout.addWidget(self.shapeGroupBox)
        self.mainLayout.addLayout(self.row3Layout,2,0)


    # image를 보여주는 groupbox
    def showImageGroupBox(self, title, image, height, width):
        self.showGroupBox = QGroupBox(title, height, width)
        self.vbox = QVBoxLayout()
        self.pixmapLabel = QPixmapLabel(image, height - 20, width - 20)
        self.vbox.addWidget(self.pixmapLabel)
        self.showGroupBox.setLayout(self.vbox)

        return self.showGroupBox




    # buttonClicked funtions
    def changeVals(self, update):
        self.ad_status = update["ad_status"]
        self.score = update["Hscore"]
        self.now = update["now"]
        self.com_dataList = update["com_dataList"]
        self.current_score = update["current_score"]

        groupboxList = [["High Score", '%d' % self.score], ["Score", '%d' % self.current_score],
                        ["Game Streak", '%d' % self.now]]
        for content in groupboxList:
            self.groupbox = QInformationGroupBox(content, 130, 150)




    def changeImages(self, update):
        if update["ad_status"] == 0:
            self.OffOrDef = self.showImageGroupBox("", self.offenceImage, 90, 90)
        elif update["ad_status"] == 1:
            self.OffOrDef = self.showImageGroupBox("", self.defenceImage, 90, 90)
        elif update["ad_status"] == 2:
            self.display.setText("승리!")
            tiem.sleep(1)
            self.display.setText("가위바위보 중 하나를 선택하세요.")
        elif update["ad_status"] == 3:
            self.display.setText("패배....")
            time.sleep(1)
            self.display.setText("다시 시작하려면 리셋 버튼을 누르세요.")

        if update["hand_signal"] == 0:
            self.playerLastShape = self.showImageGroupBox("player", self.mukImage, 160, 160)
            if update["ad_status"] == 0:
                self.comLastShape = self.showImageGroupBox("computer", self.jjiImage, 160, 160)
                self.display.setText("묵묵...?")
            elif update["ad_status"] == 1:
                self.comLastShape = self.showImageGroupBox("computer", self.ppaImage, 160, 160)
                self.display.setText("빠빠...!")
            else:
                self.comLastShape = self.showImageGroupBox("computer", self.mukImage, 160, 160)

        elif update["hand_signal"] == 1:
            self.playerLastShape = self.showImageGroupBox("player", self.jjiImage, 160, 160)
            if update["ad_status"] == 0:
                self.comLastShape = self.showImageGroupBox("computer", self.ppaImage, 160, 160)
                self.display.setText("찌찌...?")
            elif update["ad_status"] == 1:
                self.comLastShape = self.showImageGroupBox("computer", self.mukImage, 160, 160)
                self.display.setText("묵묵...!")
            else:
                self.comLastShape = self.showImageGroupBox("computer", self.jjiImage, 160, 160)

        else:
            self.playerLastShape = self.showImageGroupBox("player", self.ppaImage, 160, 160)
            if update["ad_status"] == 0:
                self.comLastShape = self.showImageGroupBox("computer", self.mukImage, 160, 160)
                self.display.setText("빠빠...?")
            elif update["ad_status"] == 1:
                self.comLastShape = self.showImageGroupBox("computer", self.jjiImage, 160, 160)
                self.display.setText("찌찌...!")
            else:
                self.comLastShape = self.showImageGroupBox("computer", self.ppaImage, 160, 160)
        self.row1Layout.addWidget(self.OffOrDef, 0, 0)
        self.lastShapeLayout.addWidget(self.comLastShape, 0, 0)
        self.lastShapeLayout.addWidget(self.playerLastShape, 2, 0)
        self.display.repaint()

    # exit button clicked
    def exitButtonClicked(self):
        button = self.sender()
        #key = button.text()
        self.display.setText("게임을 종료합니다...")
        openDB = ScoreDB()
        sys.exit(openDB)


    # newGame button clicked
    def newGameButtonClicked(self):

        self.com_dataList = [0, 1, 2]
        self.current_score = 0
        self.score = 0
        self.ad_status = None
        self.now = 0
        self.comLastShape = self.showImageGroupBox("computer", self.initialImage, 160, 160)
        self.playerLastShape = self.showImageGroupBox("player", self.initialImage, 160, 160)
        self.lastShapeLayout.addWidget(self.comLastShape, 0, 0)
        self.lastShapeLayout.addWidget(self.playerLastShape, 2, 0)
        self.display.repaint()
        self.display.setText("게임이 리셋되었습니다. 다시 시작중...")
        self.display.repaint()
        time.sleep(1)
        self.display.setText("게임을 시작합니다. 가위바위보 중 하나를 선택하세요.")





    # muk button clicked
    def mukButtonClicked(self):
        try:
            shape = 0
            button = self.sender()
            gameLoop = game.mukjjippa()
            result = gameLoop.ingame(self.ad_status, shape, self.score, self.now, self.com_dataList)
            self.changeVals(result)
            self.changeImages(result)

            print(result)
            print(self.ad_status, shape, self.score, self.now, self.com_dataList)
        except Exception:
            err = traceback.format_exc()
            ErrorLog(str(err))

    # jji button clicked
    def jjiButtonClicked(self):
        try:
            shape = 1
            button = self.sender()
            gameLoop = game.mukjjippa()
            result = gameLoop.ingame(self.ad_status, shape, self.score, self.now, self.com_dataList)
            self.changeVals(result)
            self.changeImages(result)
            print(result)
        except Exception:
            err = traceback.format_exc()
            ErrorLog(str(err))

    # ppa button clicked
    def ppaButtonClicked(self):

        try:
            shape = 2
            button = self.sender()
            gameLoop = game.mukjjippa()
            result = gameLoop.ingame(self.ad_status, shape, self.score, self.now, self.com_dataList)
            self.changeVals(result)
            self.changeImages(result)

            print(result)
        except Exception:
            err = traceback.format_exc()
            ErrorLog(str(err))



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mjpgame = Game()
    mjpgame.show()
    sys.exit(app.exec_())
