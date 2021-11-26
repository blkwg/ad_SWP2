from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGroupBox, QLineEdit
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QImage, QBrush

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

        # images
        mukImage = "image/mjp/묵.png"
        jjiImage = "image/mjp/찌.png"
        ppaImage = "image/mjp/빠.png"
        offenceImage = "image/공격.png"
        defenceImage = "image/방어.png"
        newGameImage = "image/재시작.png"
        exitImage = "image/종료.png"
        # wallpaperImage = "image/wallpaper.jpg"

        # wallpaper setting
        # wallpaper = QImage("wallpaper.jpg")
        # wallpaper.scaled(QSize())
        # palette = QPalette()
        # palette.setBrush(10, QBrush(wallpaper))
        # self.setPalette(palette)


        # row1

        # 공격/수비 표시
        self.OffOrDef = self.showImageGroupBox("", defenceImage, 90, 90)

        # 현재 상태 표시
        self.display = QLineEdit(self)
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
        self.comLastShape = self.showImageGroupBox("computer", mukImage, 160, 160)

        # 플레이어가 이전 턴에 낸 모양
        self.playerLastShape = self.showImageGroupBox("player", jjiImage, 160, 160)

        self.lastShapeLayout = QGridLayout()
        self.lastShapeLayout.addWidget(self.comLastShape, 0, 0)
        self.lastShapeLayout.addWidget(self.playerLastShape, 2, 0)

        # 컴퓨터가 현재 턴에 낸 모양
        self.comShape = self.showImageGroupBox("", ppaImage, 300, 300)

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
        self.muk = QPushButton("", mukImage, 150, 150, self.mukButtonClicked)
        self.jji = QPushButton("", jjiImage, 150, 150, self.jjiButtonClicked)
        self.ppa = QPushButton("", ppaImage, 150, 150, self.ppaButtonClicked)

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

    # exit button clicked
    def exitButtonClicked(self):
        button = self.sender()
        key = button.text()
        self.display.setText(key)


    # newGame button clicked
    def newGameButtonClicked(self):
        pass

    # muk button clicked
    def mukButtonClicked(self):
        shape = 0

        button = self.sender()
        # key = button.text()

    # jji button clicked
    def jjiButtonClicked(self):
        shape = 1

        button = self.sender()
        # key = button.text()

    # ppa button clicked
    def ppaButtonClicked(self):
        shape = 2

        button = self.sender()
        # key = button.text()



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())