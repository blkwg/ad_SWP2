from PyQt5.QtCore import Qt, QSize, QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGroupBox, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QImage, QBrush
import time
from game import *
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


class QInformationGroupBox(QGroupBox): # information 표시하는 GroupBox는 아예 class로 만듦
    def __init__(self, title, label, height, width):
        super().__init__()
        self.setTitle(title)

        # GroupBox에 Label들 추가
        self.vbox = QVBoxLayout()

        informationLabel = label
        font = informationLabel.font()
        font.setPointSize(font.pointSize() + 6)
        informationLabel.setFont(font)

        self.vbox.addWidget(informationLabel)
        self.setLayout(self.vbox)

        # 크기설정
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
        self.com_dataList = [0, 1, 2]
        self.highScore = 0
        self.current_score = 0
        self.gameStreak = 0
        self.winningStreak = 0

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
        self.wallpaperImage = "image/wallpaper.jpg"

        # wallpaper setting
        # wallpaper = QImage(self.wallpaperImage)
        # wallpaper.scaled(QSize())
        # palette = QPalette()
        # palette.setBrush(10, QBrush(wallpaper))
        # self.setPalette(palette)

        # row1

        # 공격/수비 표시
        self.OffOrDefLabel = self.pixmapLabel(self.initialImage, 75, 75)
        self.OffOrDefLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.OffOrDef = self.showImageGroupBox("", self.OffOrDefLabel, 70, 70)

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
        self.reset.clicked.connect(self.resetButtonClicked)

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
        self.playerShapeLabel = self.pixmapLabel(self.initialImage, 140, 140)
        self.playerShapeLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.playerShape = self.showImageGroupBox("Mine", self.playerShapeLabel, 140, 140)

        # 컴퓨터의 현재 턴
        self.comShapeLabel = self.pixmapLabel(self.questionImage, 280, 280)
        self.comShapeLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.comShape = self.showImageGroupBox("Computer's", self.comShapeLabel, 280, 280)

        # high score / score / game streak 표시
        self.informationLayout = QGridLayout()

        self.showHighScore = QLabel(str(self.highScore))
        self.highScoreGroupBox = QInformationGroupBox("High Score", self.showHighScore, 100, 150)
        self.informationLayout.addWidget(self.highScoreGroupBox, 0, 0)

        self.showScore = QLabel(str(self.current_score))
        self.scoreGroupBox = QInformationGroupBox("Score", self.showScore, 100, 150)
        self.informationLayout.addWidget(self.scoreGroupBox, 1, 0)

        self.showGameStreak = QLabel(str(self.gameStreak))
        self.gameStreakGroupBox = QInformationGroupBox("Game Streak", self.showGameStreak, 100, 150)
        self.informationLayout.addWidget(self.gameStreakGroupBox, 2, 0)

        self.showWinningStreak = QLabel(str(self.winningStreak))
        self.winningStreakGroupBox = QInformationGroupBox("Winning Streak", self.showWinningStreak, 100, 150)
        self.informationLayout.addWidget(self.winningStreakGroupBox, 3, 0)

        # Layout
        self.row2Layout.addWidget(self.playerShape, 0, 0, 1, 1)
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


# -----------------------------------------------------------------------------------------
# 한 턴 실행하기
# -----------------------------------------------------------------------------------------
    # change value
    def changeVals(self, update):
        self.ad_status = update["ad_status"]
        self.com_dataList = update["com_dataList"]
        self.gameStreak += 1
        self.current_score = update["current_score"]

        if self.current_score > self.highScore:
            self.highScore = self.current_score

        self.showHighScore.setText(str(self.highScore))
        self.showScore.setText(str(self.current_score))
        self.showGameStreak.setText(str(self.gameStreak))

    # 현재 턴을 실행하거나 게임 종료처리
    def currentTurn(self, update):

        if update["ad_status"] == 0:
            pixmapImage = self.changePixLabelImage(self.offenceImage, 70, 70)
            self.OffOrDefLabel.setPixmap(QPixmap(pixmapImage))
        elif update["ad_status"] == 1:
            pixmapImage = self.changePixLabelImage(self.defenceImage, 75, 75)
            self.OffOrDefLabel.setPixmap(QPixmap(pixmapImage))
        elif update["ad_status"] == 2:
            pixmapImage = self.changePixLabelImage(self.offenceImage, 70, 70)
            self.OffOrDefLabel.setPixmap(QPixmap(pixmapImage))
            self.changeImages(update)
            self.display.setText("승리!!!")
            self.winningStreak += 1
            self.showWinningStreak.setText(str(self.winningStreak))

            self.display.repaint()
            time.sleep(2)

            pixmapImage = self.changePixLabelImage(self.initialImage, 140, 140)
            self.playerShapeLabel.setPixmap(QPixmap(pixmapImage))
            pixmapImage = self.changePixLabelImage(self.questionImage, 280, 280)
            self.comShapeLabel.setPixmap(QPixmap(pixmapImage))
            pixmapImage = self.changePixLabelImage(self.initialImage, 70, 70)
            self.OffOrDefLabel.setPixmap(QPixmap(pixmapImage))

            self.display.setText("가위바위보 중 하나를 선택하세요.")
            return

        elif update["ad_status"] == 3:
            self.changeImages(update)
            self.display.setText("패배....")
            self.display.repaint()
            time.sleep(2)
            self.display.setText("게임을 다시 시작합니다.")
            self.newGame()
            return

        self.changeImages(update)

        self.display.repaint()

    # 공/방 image와 player's & computer's shape 바꾸기
    def changeImages(self, update):

        if update["hand_signal"] == 0:
            pixmapImage = self.changePixLabelImage(self.mukImage, 140, 140)
            self.playerShapeLabel.setPixmap(QPixmap(pixmapImage))
            if update["ad_status"] == 0:
                pixmapImage = self.changePixLabelImage(self.jjiImage, 280, 280)
                self.comShapeLabel.setPixmap(QPixmap(pixmapImage))
                self.display.setText("묵 묵...?")
            elif update["ad_status"] == 1:
                pixmapImage = self.changePixLabelImage(self.ppaImage, 280, 280)
                self.comShapeLabel.setPixmap(QPixmap(pixmapImage))
                self.display.setText("빠 빠...!")
            else:
                pixmapImage = self.changePixLabelImage(self.mukImage, 280, 280)
                self.comShapeLabel.setPixmap(QPixmap(pixmapImage))

        elif update["hand_signal"] == 1:
            pixmapImage = self.changePixLabelImage(self.jjiImage, 140, 140)
            self.playerShapeLabel.setPixmap(QPixmap(pixmapImage))
            if update["ad_status"] == 0:
                pixmapImage = self.changePixLabelImage(self.ppaImage, 280, 280)
                self.comShapeLabel.setPixmap(QPixmap(pixmapImage))
                self.display.setText("찌 찌...?")
            elif update["ad_status"] == 1:
                pixmapImage = self.changePixLabelImage(self.mukImage, 280, 280)
                self.comShapeLabel.setPixmap(QPixmap(pixmapImage))
                self.display.setText("묵 묵...!")
            else:
                pixmapImage = self.changePixLabelImage(self.jjiImage, 280, 280)
                self.comShapeLabel.setPixmap(QPixmap(pixmapImage))

        else:
            pixmapImage = self.changePixLabelImage(self.ppaImage, 140, 140)
            self.playerShapeLabel.setPixmap(QPixmap(pixmapImage))
            if update["ad_status"] == 0:
                pixmapImage = self.changePixLabelImage(self.mukImage, 280, 280)
                self.comShapeLabel.setPixmap(QPixmap(pixmapImage))
                self.display.setText("빠 빠...?")
            elif update["ad_status"] == 1:
                pixmapImage = self.changePixLabelImage(self.jjiImage, 280, 280)
                self.comShapeLabel.setPixmap(QPixmap(pixmapImage))
                self.display.setText("찌 찌...!")
            else:
                pixmapImage = self.changePixLabelImage(self.ppaImage, 280, 280)
                self.comShapeLabel.setPixmap(QPixmap(pixmapImage))


# -----------------------------------------------------------------------------------------
# buttonClicked Methods
# -----------------------------------------------------------------------------------------

    # exit button clicked
    def exitButtonClicked(self):
        re = QMessageBox.question(self, "종료 확인", "게임을 종료하시겠습니까?",
                                  QMessageBox.Yes | QMessageBox.No)

        if re == QMessageBox.Yes:
            QCoreApplication.instance().quit()

    # reset button clicked
    def resetButtonClicked(self):
        re = QMessageBox.question(self, "리셋 확인", "게임을 다시 시작하시겠습니까?",
                                  QMessageBox.Yes | QMessageBox.No)

        if re == QMessageBox.Yes:
            self.newGameSet()

            self.display.repaint()
            self.display.setText("게임이 리셋되었습니다. 다시 시작중...")
            self.display.repaint()
            time.sleep(1)
            self.display.setText("게임을 시작합니다. 가위바위보 중 하나를 선택하세요.")

    # 패배해서 새로운 게임 시작할 때때
    def newGame(self):
        self.newGameSet()

        self.display.repaint()
        self.display.setText("새 게임 시작중...")
        self.display.repaint()
        time.sleep(1)
        self.display.setText("게임을 새로 시작합니다. 가위바위보 중 하나를 선택하세요.")

    # 게임 reset할 때 변수 initialize
    def newGameSet(self):
        self.com_dataList = [0, 1, 2]
        self.ad_status = None
        self.current_score = 0
        self.gameStreak = 0
        self.winningStreak = 0

        pixmapImage = self.changePixLabelImage(self.initialImage, 75, 75)
        self.OffOrDefLabel.setPixmap(QPixmap(pixmapImage))

        pixmapImage = self.changePixLabelImage(self.questionImage, 280, 280)
        self.comShapeLabel.setPixmap(QPixmap(pixmapImage))

        pixmapImage = self.changePixLabelImage(self.initialImage, 140, 140)
        self.playerShapeLabel.setPixmap(QPixmap(pixmapImage))

        self.showScore.setText(str(self.current_score))
        self.showGameStreak.setText(str(self.gameStreak))
        self.showWinningStreak.setText(str(self.winningStreak))

    # muk button clicked
    def mukButtonClicked(self):
        try:
            shape = 0
            gameLoop = mukjjippa()
            result = gameLoop.ingame(self.ad_status, shape, self.current_score, self.gameStreak, self.com_dataList)
            self.changeVals(result)
            self.currentTurn(result)

        except Exception:
            err = traceback.format_exc()
            ErrorLog(str(err))
            print(str(err))

    # jji button clicked
    def jjiButtonClicked(self):
        try:
            shape = 1
            gameLoop = mukjjippa()
            result = gameLoop.ingame(self.ad_status, shape, self.current_score, self.gameStreak, self.com_dataList)
            self.changeVals(result)
            self.currentTurn(result)

        except Exception:
            err = traceback.format_exc()
            ErrorLog(str(err))
            print(str(err))

    # ppa button clicked
    def ppaButtonClicked(self):
        try:
            shape = 2
            gameLoop = mukjjippa()
            result = gameLoop.ingame(self.ad_status, shape, self.current_score, self.gameStreak, self.com_dataList)
            self.changeVals(result)
            self.currentTurn(result)

        except Exception:
            err = traceback.format_exc()
            ErrorLog(str(err))
            print(str(err))


# -----------------------------------------------------------------------------------------
# 특정 목적 widget 제작 methods
# -----------------------------------------------------------------------------------------
    # image를 출력하는 QPushButton
    def imagePushButton(self, image, height, width):
        button = QPushButton(height, width)
        button.setIcon(QIcon(image))
        button.setIconSize(QSize(height - 15, width - 15))

        return button

    # label -> pixmapLabel
    def pixmapLabel(self, image, height, width):
        pixmapLabel = QLabel()

        pixmap = QPixmap(image)
        pixmap = pixmap.scaledToHeight(height)
        pixmap = pixmap.scaledToWidth(width)

        pixmapLabel.setPixmap(QPixmap(pixmap))

        return pixmapLabel

    def changePixLabelImage(self, image, height, width):
        pixmap = QPixmap(image)
        pixmap = pixmap.scaledToHeight(height)
        pixmap = pixmap.scaledToWidth(width)

        return pixmap

    # image를 보여주는 groupbox
    def showImageGroupBox(self, title, widget, height, width):
        self.showGroupBox = QGroupBox(title, height + 20, width + 20)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(widget)
        self.showGroupBox.setLayout(self.vbox)

        return self.showGroupBox




if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())