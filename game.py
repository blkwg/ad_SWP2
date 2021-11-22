from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QApplication
from PyQt5.QtGui import QPixmap
import sys
import random

class mukjjippa(QWidget):
    def __init__(self):
        super().__init__()
        self.now = 0
        self.user_status = None
        self.com_dataList = [0, 1, 2]
        self.score = 0
        self.current_score = 0
        self.gbb(self.now, self.score)


    def gbb(self, now, score):
        while now == 0:
            user = input("Enter 가위/바위/보: ")
            if user == "가위":
                user = 1
            elif user == "바위":
                user = 0
            elif user == "보":
                user = 2
            com = random.choice(self.com_dataList)
            if com == 1:
                print("com: 가위")
            elif com == 2:
                print("com: 보")
            elif com == 0:
                print("com: 바위")
            if user != com:
                now = 1
                if user == 0 and com == 1:
                    self.user_status = 0
                elif user == 1 and com == 2:
                    self.user_status = 0
                elif user == 2 and com == 0:
                    self.user_status = 0
                elif user == com:
                    print("다시")
                    self.gbb(now, score)
                else:
                    self.user_status = 1
        self.mjp(self.user_status, now, self.com_dataList, score)

    def mjp(self, stat, length, dataList, fullScore):
        # 이기고 들어갔을 때
        if stat == 0:
            print("공격")
            user = input("가위/바위/보>>")
            if user == "가위":
                user = 1
            elif user == "바위":
                user = 0
            elif user == "보":
                user = 2

            # 컴퓨터가 손모양을 선택하고, 출력하는 부분
            com = random.choice(dataList)
            if com == 1:
                print("com: 가위")
            elif com == 2:
                print("com: 보")
            elif com == 0:
                print("com: 바위")

            # 유저가 이겼을 때: -컴퓨터는 임의의 손 모양의 확률을 증가시킨다.
            if (user == 0 and com == 1) or (user == 1 and com == 2) or (user == 2 and com == 0):
                dataList.append(random.randrange(3))
                length += 1
                # 현재 점수를 보여준다. 현재 점수 = 최종 점수(얻을 점수 반영 전) + 얻을 점수
                print('current Score:', fullScore + 2 ** length)
                print()
                self.mjp(0, length, dataList, fullScore)

            # 유저가 졌을 때: 컴퓨터는 컴퓨터가 낸 손 모양의 확률을 증가시킨다.
            elif (user == 1 and com == 0) or (user == 2 and com == 1) or (user == 0 and com == 2):
                dataList.append(com)
                length += 1
                print('current Score:', fullScore + 2 ** length)
                print()
                self.mjp(1, length, dataList, fullScore)

            # 승부가 났다-여기서는 승리했다.
            elif user == com:
                print("승리!")
                # 최종 점수 fullScore에 얻은 점수를 합산한다.
                fullScore += 2 ** length
                print("Current Score:", fullScore)
                # 묵찌빠에서 질 때까지 게임을 진행하므로, 새로운 판을 시작한다.
                self.gbb(0, fullScore)

        # 지고 들어갔을 때
        elif stat == 1:
            print("수비")
            user = input("가위/바위/보>>")
            if user == "가위":
                user = 1
            elif user == "바위":
                user = 0
            elif user == "보":
                user = 2

            # 컴퓨터가 손 모양을 선택한다.
            com = random.choice(dataList)
            if com == 1:
                print("com: 가위")
            elif com == 2:
                print("com: 보")
            elif com == 0:
                print("com: 바위")

            # 유저가 이겼을 때- user_status == 0인 경우와 동일.
            if (user == 0 and com == 1) or (user == 1 and com == 2) or (user == 2 and com == 0):
                dataList.append(random.randrange(3))
                length += 1
                print('current Score:', fullScore + 2 ** length)
                print()
                self.mjp(0, length, dataList, fullScore)

            # 유저가 졌을 때- user_status == 0인 경우와 동일.
            elif (user == 1 and com == 0) or (user == 2 and com == 1) or (user == 0 and com == 2):
                dataList.append(com)
                length += 1
                print('current Score:', fullScore + 2 ** length)
                print()
                self.mjp(1, length, dataList, fullScore)

            # 승부가 났을 때- 점수 합산을 한다.
            elif user == com:
                # print("패배...")
                fullScore += 2 ** length
                print("Score:", fullScore)


    def ingame(self, ad_status, hand_signal):
        # 이기고 들어갔을 때:
        com = random.choice(self.com_dataList)
        if com == 0:
            # 주먹 이미지
            pass
        elif com == 1:
            # 가위 이미지
            pass
        elif com == 2:
            # 보 이미지
            pass

        if ad_status == 0:
            if hand_signal == 0:#이기고 들어왔을 때
                if com == 1:
                    self.com_dataList.append(random.randrange(3))
                    self.now += 1
                    self.current_score = self.score + 2**self.now
                elif com == 2:
                    self.com.datalist.append(com)
                    self.now += 1
                    self.current_score = self.score  + 2**self.now
                    ad_status = 1
                elif com == 2:
                    self.score += 2**self.now
                    # 승리 신호 제공, 새로운 게임을 시작할 수 있는 신호 제공 코드 추가.
            elif hand_signal == 1:
                if com == 2:
                    self.com_dataList.append(random.randrange(3))
                    self.now += 1
                    self.current_score = self.score + 2**self.now
                elif com == 0:
                    self.com.datalist.append(com)
                    self.now += 1
                    self.current_score = self.score  + 2**self.now
                    ad_status = 1
                elif com == 1:
                    self.score += 2**self.now
                    # 승리 신호 제공, 새로운 게임을 시작할 수 있는 신호 제공 코드 추가.
            elif hand_signal == 2:
                if com == 0:
                    self.com_dataList.append(random.randrange(3))
                    self.now += 1
                    self.current_score = self.score + 2**self.now
                elif com == 1:
                    self.com.datalist.append(com)
                    self.now += 1
                    self.current_score = self.score  + 2**self.now
                    ad_status = 1
                elif com == 2:
                    self.score += 2**self.now
                    # 승리 신호 제공, 새로운 게임을 시작할 수 있는 신호 제공 코드 추가.


        elif ad_status == 1:
            if hand_signal == 0:  # 이기고 들어왔을 때
                if com == 1:
                    self.com_dataList.append(random.randrange(3))
                    self.now += 1
                    self.current_score = self.score + 2 ** self.now
                elif com == 2:
                    self.com.datalist.append(com)
                    self.now += 1
                    self.current_score = self.score + 2 ** self.now
                    ad_status = 1
                elif com == 2:
                    self.score += 2 ** self.now
                    # 패배 신호 제공, 새로운 게임을 시작할 수 있는 신호 제공 코드 추가.
            elif hand_signal == 1:
                if com == 2:
                    self.com_dataList.append(random.randrange(3))
                    self.now += 1
                    self.current_score = self.score + 2 ** self.now
                elif com == 0:
                    self.com.datalist.append(com)
                    self.now += 1
                    self.current_score = self.score + 2 ** self.now
                    ad_status = 1
                elif com == 1:
                    self.score += 2 ** self.now
                    # 패배 신호 제공, 새로운 게임을 시작할 수 있는 신호 제공 코드 추가.
            elif hand_signal == 2:
                if com == 0:
                    self.com_dataList.append(random.randrange(3))
                    self.now += 1
                    self.current_score = self.score + 2 ** self.now
                elif com == 1:
                    self.com.datalist.append(com)
                    self.now += 1
                    self.current_score = self.score + 2 ** self.now
                    ad_status = 1
                elif com == 2:
                    self.score += 2 ** self.now
                    # 패배 신호 제공, 스코어보드를 띄우는 코드, 새로운 게임을 연결할 수 있는 코드 추가.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mjp = mukjjippa()


    #app.exec_()

