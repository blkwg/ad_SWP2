from PyQt5.QtCore import Qt, QSize, QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGroupBox, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QImage, QBrush
import time
import sys
from mainView.main import ScoreDB
import traceback


class QPushButton(QPushButton):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

class QImagePushButton(QPushButton):
    def __init__(self, text, image, height, width):
        super().__init__()
        self.setText(text)

        # QPushButton image setting
        self.setIcon(QIcon(image))
        self.setIconSize(QSize(height - 15, width - 15))

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
        self.OffOrDef = QPushButton()
        self.OffOrDef.setMaximumHeight(100)
        self.OffOrDef.setMaximumWidth(100)
        self.OffOrDef.setIconSize(QSize(85, 85))

        self.OffOrDef.clicked.connect(self.OffOrDefClicked)

        # 현재 상태 표시
        self.display = QLineEdit(self)
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setReadOnly(True)
        self.display.setMaximumHeight(80)

        font = self.display.font()
        font.setPointSize(font.pointSize() + 2)
        self.display.setFont(font)

        # 새로운 게임
        self.reset = QPushButton()
        self.reset.setMaximumHeight(70)
        self.reset.setMaximumWidth(70)
        self.reset.setIcon(QIcon(self.newGameImage))
        self.reset.setIconSize(QSize(55, 55))

        # 나가기 버튼
        self.exit = QPushButton()
        self.exit.setMaximumHeight(70)
        self.exit.setMaximumWidth(70)
        self.exit.setIcon(QIcon(self.exitImage))
        self.exit.setIconSize(QSize(55, 55))
        self.exit.clicked.connect(self.exitButtonClicked)

        # Layout
        self.row1Layout.addWidget(self.OffOrDef, 0, 0)
        self.row1Layout.addWidget(self.display, 0, 1)
        self.row1Layout.addWidget(self.reset, 0, 2)
        self.row1Layout.addWidget(self.exit, 0, 3)

        self.mainLayout.addLayout(self.row1Layout, 0, 0)


        # row 2

        # 컴퓨터가 이전 턴에 낸 모양
        self.comLastShape = QPushButton()
        self.comLastShape.setMaximumHeight(160)
        self.comLastShape.setMaximumWidth(160)
        self.comLastShape.setIcon(QIcon(self.initialImage))
        self.comLastShape.setIconSize(QSize(145, 145))

        # 플레이어가 이전 턴에 낸 모양
        self.playerLastShape = QPushButton()
        self.playerLastShape.setMaximumHeight(160)
        self.playerLastShape.setMaximumWidth(160)
        self.playerLastShape.setIcon(QIcon(self.initialImage))
        self.playerLastShape.setIconSize(QSize(145, 145))

        self.lastShapeLayout = QGridLayout()
        self.lastShapeLayout.addWidget(self.comLastShape, 0, 0)
        self.lastShapeLayout.addWidget(self.playerLastShape, 2, 0)

        # 컴퓨터의 현재 턴
        self.comShape = QPushButton()
        self.comShape.setMaximumHeight(300)
        self.comShape.setMaximumWidth(300)
        self.comShape.setIcon(QIcon(self.initialImage))
        self.comShape.setIconSize(QSize(285, 285))

        # high score / score / game streak 표시
        self.informationLayout = QGridLayout()

        groupboxList = [["High Score", '0'], ["Score", '0'], ["Game Streak", '0']]
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
        self.muk = QImagePushButton("", self.mukImage, 150, 150)
        self.muk.clicked.connect(self.mukButtonClicked)
        self.jji = QImagePushButton("", self.jjiImage, 150, 150)
        self.jji.clicked.connect(self.jjiButtonClicked)
        self.ppa = QImagePushButton("", self.ppaImage, 150, 150)
        self.ppa.clicked.connect(self.ppaButtonClicked)



        # Layout
        self.row3Layout.addWidget(self.muk)
        self.row3Layout.addWidget(self.jji)
        self.row3Layout.addWidget(self.ppa)
        self.mainLayout.addLayout(self.row3Layout, 2, 0)

        self.display.setText("게임을 시작합니다. 가위바위보 중 하나를 선택하세요.")


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
        pass

    # jji button clicked
    def jjiButtonClicked(self):
        pass

    # ppa button clicked
    def ppaButtonClicked(self):
        pass

    def OffOrDefClicked(self):
        self.OffOrDef.setIcon(QIcon("GameUI\image\물음표.png"))
        self.display.setText("hello")





if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())