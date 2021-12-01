import pickle
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel,
    QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt

from gameUI import Game

class MainView(QWidget):
    global A
    def __init__(self, game):
        super().__init__()
        self.initUI()
        self.dbfilename = 'userDB.csv'
        self.scoredb = []
        self.readScoreDB()
        self.showScoreDB()
        self.game = game

    def initUI(self):
        NameLabel = QLabel('Name', self)
        self.NameEdit = QLineEdit(self)

        inputHbox = QHBoxLayout()
        inputHbox.addStretch(1)
        inputHbox.addWidget(NameLabel)
        inputHbox.addWidget(self.NameEdit)

        gameButton = QPushButton('Game Start')
        gameButton.clicked.connect(self.gameClicked)

        addButton = QPushButton('Add')
        addButton.clicked.connect(self.addClicked)

        delButton = QPushButton('Del')
        delButton.clicked.connect(self.delClicked)

        findButton = QPushButton('Find')
        findButton.clicked.connect(self.findClicked)

        showButton = QPushButton('Show')
        showButton.clicked.connect(self.showClicked)

        commandHbox = QHBoxLayout()
        commandHbox.addStretch(1)
        commandHbox.addWidget(gameButton)
        commandHbox.addWidget(addButton)
        commandHbox.addWidget(delButton)
        commandHbox.addWidget(findButton)
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
        self.setGeometry(700, 400, 300, 200)
        self.setWindowTitle('Main')
        self.show()

    def gameClicked(self):
        try:
            sender = self.sender()
            name = self.NameEdit.text()
            if name == '':
                raise ValueError

            msg = ''
            check = self.nameCheck(name)

            if check == True:
                self.close()
                A.show(name)

            else :
                msg = '없는 닉네임입니다. 추가해주세요. '
                self.resultEdit.setText(msg)

        except ValueError:
            msg = '입력값을 정확하게 입력해주세요 '
            self.resultEdit.setText(msg)
            pass

        except:
            pass

    def updateScore(self, name):
        try:
            if self.gameUI.score > self.gameUI.current_score:
                for p in self.scoredb:
                    if p['Name'] == name:
                        p['Score'] = self.gameUI.score

        except:
            pass


    def addClicked(self):
        try:
            sender = self.sender()
            name = self.NameEdit.text()
            if name == '':
                raise ValueError

            msg = ''
            check = self.nameCheck(name)

            if check == False:
                record = {'Name': name, 'Score': 0}
                self.scoredb += [record]
                self.showScoreDB()
            else :
                msg = '이미 존재하는 닉네임입니다. '
                self.resultEdit.setText(msg)

        except ValueError:
            msg = '입력값을 정확하게 입력해주세요 '
            self.resultEdit.setText(msg)
            pass

        except:
            pass


    def delClicked(self):
        try:
            sender = self.sender()
            name = self.NameEdit.text()
            if name == '':
                raise ValueError

            msg = ''
            check = self.nameCheck(name)

            if check == True:
                self.scoredb[:] = [p for p in self.scoredb if p['Name'] != name]
                self.showScoreDB()
            else:
                msg = '닉네임이 존재하지 않습니다. '
                self.resultEdit.setText(msg)

        except ValueError:
            msg = '입력값을 정확하게 입력해주세요 '
            self.resultEdit.setText(msg)
            pass

        except:
            pass


    def findClicked(self):
        try:
            sender = self.sender()
            name = self.NameEdit.text()
            if name == '':
                raise ValueError

            msg = ''
            idx = 1
            check = self.nameCheck(name)

            if check == True:
                for p in sorted(self.scoredb, key=lambda person: person['Score'], reverse=True):
                    if p['Name'] != name:
                        idx += 1
                    else:
                        msg += str(idx) + '위' + '       \t'
                        for attr in sorted(p):
                            if attr != 'Age':
                                msg += str(p[attr]) + '       \t'
            else :
                msg = '닉네임이 존재하지 않습니다. '

            self.resultEdit.setText(msg)

        except ValueError:
            msg = '입력값을 정확하게 입력해주세요 '
            self.resultEdit.setText(msg)
            pass

        except:
            pass

    def nameCheck(self, name):
        try:
            sender = self.sender()
            result = bool

            for p in self.scoredb:
                if p['Name'] != name:
                    result = False
                else:
                    result = True
                    break

            return result
        except:
            pass

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

    def showScoreDB(self):
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

    game = Game()
    ex = MainView(game)
    A = Game()

    sys.exit(app.exec_())