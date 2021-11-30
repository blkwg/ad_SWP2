from PyQt5.QtCore import Qt, QSize, QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGroupBox, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QImage, QBrush
import time
import sys
from game import *
from mainView.main import ScoreDB
import traceback

def ErrorLog(error: str):
    current_time = time.strftime("%Y.%m.%d/%H:%M:%S", time.localtime(time.time()))
    with open("Log.txt", "a") as f:
        f.write(f"[{current_time}] - {error}\n")

class QPushButton(QPushButton):
    def __init__(self, height, width):
        super().__init__()

        # QPushButton size setting
        self.setMaximumHeight(height)
        self.setMaximumWidth(width)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

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

        # game values
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

        self.newGameImage = "image/재시작.png"
        self.exitImage = "image/종료.png"
        self.initialImage = "image/투명.png" # 처음 시작할 때 나오는 투명 배경
        self.questionImage = "image/물음표.png"
        # self.wallpaperImage = "image/wallpaper.jpg"

        # wallpaper setting
        # wallpaper = QImage("wallpaper.jpg")
        # wallpaper.scaled(QSize())
        # palette = QPalette()
        # palette.setBrush(10, QBrush(wallpaper))
        # self.setPalette(palette)

        # row1

        # 공격/수비 표시
        self.OffOrDef = self.reset = self.imagePushButton(self.initialImage, 90, 90)

        # 현재 상태 표시
        self.display = QLineEdit(self)
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setReadOnly(True)
        self.display.setMaximumHeight(80)

        font = self.display.font()
        font.setPointSize(font.pointSize() + 2)
        self.display.setFont(font)

        # 새로운 게임
        self.reset = self.imagePushButton(self.newGameImage, 70, 70)
        self.reset.clicked.connect(self.newGameButtonClicked)

        # 나가기 버튼
        self.exit = self.imagePushButton(self.exitImage, 70, 70)
        self.exit.clicked.connect(self.exitButtonClicked)

        # Layout
        self.row1Layout.addWidget(self.OffOrDef, 0, 0)
        self.row1Layout.addWidget(self.display, 0, 1)
        self.row1Layout.addWidget(self.reset, 0, 2)
        self.row1Layout.addWidget(self.exit, 0, 3)

        self.mainLayout.addLayout(self.row1Layout, 0, 0)


        # row 2


        # 플레이어가 현재 턴에 낸 모양
        self.playerShapeLabel = QLabel("player's shape")
        self.playerShape = self.imagePushButton(self.initialImage, 160, 160)

        self.ShapeLayout = QGridLayout()
        self.ShapeLayout.addWidget(self.playerShapeLabel, 0, 0)
        self.ShapeLayout.addWidget(self.playerShape, 1, 0)

        # 컴퓨터의 현재 턴
        self.comShape = self.imagePushButton(self.questionImage, 300, 300)

        # high score / score / game streak 표시
        self.informationLayout = QGridLayout()

        groupboxList = [["High Score", '%d' % self.score], ["Score", '%d' % self.current_score], ["Game Streak", '%d' % self.now]]
        for content in groupboxList:
            self.groupbox = QInformationGroupBox(content, 130, 150)
            self.informationLayout.addWidget(self.groupbox, groupboxList.index(content), 0)

        # Layout
        self.row2Layout.addLayout(self.ShapeLayout, 0, 0, 1, 1)
        self.row2Layout.addWidget(self.comShape, 0, 1, 2, 1)
        self.row2Layout.addLayout(self.informationLayout, 0, 5, 2, 1)

        self.mainLayout.addLayout(self.row2Layout, 1, 0)


        # row 3

        # 묵찌빠 선택 버튼
        self.muk = self.imagePushButton(self.mukImage, 150, 150)
        self.muk.clicked.connect(self.mukButtonClicked)

        self.jji = self.imagePushButton(self.jjiImage, 150, 150)
        self.jji.clicked.connect(self.jjiButtonClicked)

        self.ppa = self.imagePushButton(self.ppaImage, 150, 150)
        self.ppa.clicked.connect(self.ppaButtonClicked)

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
        self.mainLayout.addLayout(self.row3Layout, 2, 0)

        self.display.setText("게임을 시작합니다. 가위바위보 중 하나를 선택하세요.")

    # image를 출력하는 QPushButton
    def imagePushButton(self, image, height, width):
        button = QPushButton(height, width)
        button.setIcon(QIcon(image))
        button.setIconSize(QSize(height - 15, width - 15))

        return button

    # change value
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

    # change image of imagePushButton
    def changeImages(self, update):

        self.comShape.setIcon(QIcon(self.questionImage))
        time.sleep(1)

        if update["ad_status"] == 0:
            self.OffOrDef.setIcon(QIcon(self.offenceImage))
        elif update["ad_status"] == 1:
            self.OffOrDef.setIcon(QIcon(self.defenceImage))
        elif update["ad_status"] == 2:
            self.OffOrDef.setIcon(QIcon(self.offenceImage))
            self.display.setText("승리!!!")
            self.comShape.setIcon(QIcon(self.questionImage))
            self.display.repaint()
            time.sleep(2)
            self.display.setText("가위바위보 중 하나를 선택하세요.")
        elif update["ad_status"] == 3:
            self.display.setText("패배....")
            self.comShape.setIcon(QIcon(self.questionImage))
            self.display.repaint()
            time.sleep(2)
            self.display.setText("다시 시작하려면 리셋 버튼을 누르세요.")

        if update["hand_signal"] == 0:
            self.playerShape.setIcon(QIcon(self.mukImage))
            if update["ad_status"] == 0:
                self.comShape.setIcon(QIcon(self.jjiImage))
                self.display.setText("묵 묵...?")
            elif update["ad_status"] == 1:
                self.comShape.setIcon(QIcon(self.ppaImage))
                self.display.setText("빠 빠...!")
            else:
                self.comShape.setIcon(QIcon(self.mukImage))
                self.lastShape[1] = self.mukImage

        elif update["hand_signal"] == 1:
            self.playerShape.setIcon(QIcon(self.jjiImage))
            if update["ad_status"] == 0:
                self.comShape.setIcon(QIcon(self.ppaImage))
                self.display.setText("찌 찌...?")
            elif update["ad_status"] == 1:
                self.comShape.setIcon(QIcon(self.mukImage))
                self.display.setText("묵 묵...!")
            else:
                self.comShape.setIcon(QIcon(self.jjiImage))


        else:
            self.playerShape.setIcon(QIcon(self.ppaImage))
            if update["ad_status"] == 0:
                self.comShape.setIcon(QIcon(self.mukImage))
                self.display.setText("빠 빠...?")
            elif update["ad_status"] == 1:
                self.comShape.setIcon(QIcon(self.jjiImage))
                self.display.setText("찌 찌...!")
            else:
                self.comShape.setIcon(QIcon(self.ppaImage))

        self.display.repaint()

    # exit button clicked
    def exitButtonClicked(self):
        re = QMessageBox.question(self, "종료 확인", "게임을 종료하시겠습니까?",
                                  QMessageBox.Yes|QMessageBox.No)

        if re == QMessageBox.Yes:
            QCoreApplication.instance().quit()

    # reset button clicked
    def newGameButtonClicked(self):
        re = QMessageBox.question(self, "리셋 확인", "게임을 다시 시작하시겠습니까?",
                                  QMessageBox.Yes | QMessageBox.No)

        if re == QMessageBox.Yes:
            self.com_dataList = [0, 1, 2]
            self.current_score = 0
            self.score = 0
            self.ad_status = None
            self.now = 0
            self.OffOrDef.setIcon(QIcon(self.initialImage))
            self.comLastShape.setIcon(QIcon(self.initialImage))
            self.playerLastShape.setIcon(QIcon(self.initialImage))
            self.comLastShape.setIcon(QIcon(self.initialImage))
            self.playerLastShape.setIcon(QIcon(self.initialImage))
            self.comShape.setIcon(QIcon(self.questionImage))

            self.display.repaint()
            self.display.setText("게임이 리셋되었습니다. 다시 시작중...")
            self.display.repaint()
            time.sleep(1)
            self.display.setText("게임을 시작합니다. 가위바위보 중 하나를 선택하세요.")


    # muk button clicked
    def mukButtonClicked(self):
        try:
            shape = 0
            gameLoop = mukjjippa()
            result = gameLoop.ingame(self.ad_status, shape, self.score, self.now, self.com_dataList)
            self.changeVals(result)
            self.changeImages(result)
            print(result)
            print(self.ad_status, shape, self.score, self.now, self.com_dataList)
        except Exception:
            err = traceback.format_exc()
            ErrorLog(str(err))
            print(str(err))

    # jji button clicked
    def jjiButtonClicked(self):
        try:
            shape = 1
            gameLoop = mukjjippa()
            result = gameLoop.ingame(self.ad_status, shape, self.score, self.now, self.com_dataList)
            self.changeVals(result)
            self.changeImages(result)
            print(result)
        except Exception:
            err = traceback.format_exc()
            ErrorLog(str(err))
            print(str(err))

    # ppa button clicked
    def ppaButtonClicked(self):
        try:
            shape = 2
            gameLoop = mukjjippa()
            result = gameLoop.ingame(self.ad_status, shape, self.score, self.now, self.com_dataList)
            self.changeVals(result)
            self.changeImages(result)
            print(result)
        except Exception:
            err = traceback.format_exc()
            ErrorLog(str(err))
            print(str(err))



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())