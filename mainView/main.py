import pickle
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel,
    QComboBox, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt

class ScoreDB(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.dbfilename = 'userDB.csv'
        self.scoredb = []
        self.readScoreDB()
        self.showScoreDB()

    def initUI(self):
        NameLabel = QLabel('Name', self)
        self.NameEdit = QLineEdit(self)

        ScoreLabel = QLabel('Score', self)   # 게임과 연결 후 삭제 예정
        self.ScoreEdit = QLineEdit(self)

        inputHbox = QHBoxLayout()
        inputHbox.addStretch(1)
        inputHbox.addWidget(NameLabel)
        inputHbox.addWidget(self.NameEdit)

        inputHbox.addWidget(ScoreLabel)
        inputHbox.addWidget(self.ScoreEdit)

        gameButton = QPushButton('Game Start')
        gameButton.clicked.connect(self.gameClicked)

        addButton = QPushButton('Add')
        addButton.clicked.connect(self.addClicked)

        delButton = QPushButton('Del')
        delButton.clicked.connect(self.delClicked)

        findButton = QPushButton('Find')
        findButton.clicked.connect(self.findClicked)

        UpdateButton = QPushButton('Update')
        UpdateButton.clicked.connect(self.UpdateClicked)

        showButton = QPushButton('Show')
        showButton.clicked.connect(self.showClicked)

        commandHbox = QHBoxLayout()
        commandHbox.addStretch(1)
        commandHbox.addWidget(gameButton)
        commandHbox.addWidget(addButton)
        commandHbox.addWidget(delButton)
        commandHbox.addWidget(findButton)
        commandHbox.addWidget(UpdateButton)
        commandHbox.addWidget(showButton)

        resultLabel = QLabel('Ranking : ', self)
        self.resultEdit = QTextEdit()

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(inputHbox)
        vbox.addLayout(commandHbox)
        vbox.addWidget(resultLabel)
        vbox.addWidget(self.resultEdit)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle('Main')
        self.show()

    def gameClicked(self):
        # 게엠 뷰 연결
        return

    def addClicked(self):
        sender = self.sender()
        name = self.NameEdit.text()
        msg = ''
        result = bool

        for p in self.scoredb:
            if p['Name'] != name:
                result = True
            else:
                result = False
                break

        if result == True:
            record = {'Name': name, 'Score': 0}  # 등록 -> 0점
            self.scoredb += [record]
            self.showScoreDB()
        else :
            msg = '이미 존재하는 닉네임입니다. '
            self.resultEdit.setText(msg)

    def delClicked(self):
        sender = self.sender()
        name = self.NameEdit.text()
        msg = ''
        result = bool

        for p in self.scoredb:
            if p['Name'] != name:
                result = False
            else:
                result = True
                break

        if result == True:
            self.scoredb.remove(p)
            self.showScoreDB()
        else:
            msg = '닉네임이 존재하지 않습니다. '
            self.resultEdit.setText(msg)


    def findClicked(self):
        sender = self.sender()
        name = self.NameEdit.text()
        msg = ''
        idx = 1

        for p in self.scoredb:
            if p['Name'] != name:
                result = False
            else:
                result = True
                break

        if result == True:
            for p in sorted(self.scoredb, key=lambda person: person['Score'], reverse=True):
                if p['Name'] != name:
                    idx += 1
                else:
                    msg += str(idx) + '위' + '       \t'
                    for attr in sorted(p):
                        if attr != 'Age':
                            msg += str(p[attr]) + '       \t'
        else:
            msg = '닉네임이 존재하지 않습니다. '

        self.resultEdit.setText(msg)


    def UpdateClicked(self):   # 게임 종료 후 자동으로 바뀌도록 연계
        sender = self.sender()
        name = self.NameEdit.text()
        score = int(self.ScoreEdit.text())
        msg = ''

        for p in self.scoredb:
            if p['Name'] != name:
                result = False
            else:
                result = True
                break
        if result == True:
            for p in self.scoredb:
                if p['Name'] == name:
                    p['Score'] += score
                    self.showScoreDB()
        else:
            msg = '닉네임이 존재하지 않습니다. '
            self.resultEdit.setText(msg)


    def showClicked(self):
        sender = self.sender()
        self.showScoreDB()

    def closeEvent(self, event):
        self.writeScoreDB()

    def readScoreDB(self):
        try:
            fH = open(self.dbfilename, 'rb')
        except FileNotFoundError as e:
            self.scoredb = []
            return
        try:
            self.scoredb = pickle.load(fH)
        except:
            pass
        else:
            pass
        fH.close()

    def writeScoreDB(self):
        fH = open(self.dbfilename, 'wb')
        pickle.dump(self.scoredb, fH)
        fH.close()

    def showScoreDB(self):   # 동점이라면 먼저 등록한 유저가 앞 순위
        msg = ''
        idx = 1

        for p in sorted(self.scoredb, key = lambda person:person['Score'], reverse = True):
            msg += str(idx) + '위' + '       \t'
            for attr in sorted(p):
                if attr != 'Age':
                    msg += str(p[attr]) + '       \t'
            msg += '\n'
            idx += 1
        self.resultEdit.setText(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScoreDB()
    sys.exit(app.exec_())