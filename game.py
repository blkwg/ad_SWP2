from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QApplication
from PyQt5.QtGui import QPixmap
import sys
import random
import traceback

class mukjjippa(QWidget):


    def __init__(self):
        super().__init__()

    def start(self, hand_signal, now, com_dataList):#게임 시작 시 공수를 결정하는 부분
        com = random.choice(com_dataList)
        if (hand_signal == 0 and com == 1) or (hand_signal == 1 and com == 2) or (hand_signal == 2 and com == 0):
            now +=1
            return 0


        elif (hand_signal == 1 and com == 0) or (hand_signal == 2 and com == 1) or (hand_signal == 0 and com == 2):
            now += 1
            return 1

        elif hand_signal == com:
            return None




    def winPhase(self, hand_signal, now, com_dataList):
        com = random.choice(com_dataList)
        if hand_signal == 0:
            if com == 1:
                com_dataList.append(random.randrange(3))
                now += 1
                return 0
            elif com == 2:
                com_dataList.append(com)
                now += 1
                return 1
            elif com == 2:
                return 2

        elif hand_signal == 1:
            if com == 2:
                com_dataList.append(random.randrange(3))
                now += 1
                return 0
            elif com == 0:
                com_dataList.append(com)
                now += 1
                return 1
            elif com == 1:
                return 2

        elif hand_signal == 2:
            if com == 0:
                com_dataList.append(random.randrange(3))
                now += 1
                return 0
            elif com == 1:
                com_dataList.append(com)
                now += 1
                return 1
            elif com == 2:
                return 2

    def losePhase(self, hand_signal, now, com_dataList):
        com = random.choice(com_dataList)
        if hand_signal == 0:  # 이기고 들어왔을 때
            if com == 1:
                com_dataList.append(random.randrange(3))
                now += 1
                return 0
            elif com == 2:
                com_dataList.append(com)
                now += 1
                return 1
            elif com == 0:
                return 3

        elif hand_signal == 1:
            if com == 2:
                now += 1
                return 0
            elif com == 0:
                com_dataList.append(com)
                now += 1
                return 1
            elif com == 1:
               return 3
        elif hand_signal == 2:
            if com == 0:
                com_dataList.append(random.randrange(3))
                now += 1
                return 0
            elif com == 1:
                com_dataList.append(com)
                now += 1
                return 1
            elif com == 2:
                return 3

    def win(self, score, now):
        score += 2**now
        return None

    def lose(self, score, now):
        score += 2**now
        return None

    def ingame(self, ad_status, hand_signal, score, now, com_dataList):

        if ad_status == None:
            ad_status = self.start(hand_signal, now, com_dataList)
            current_score = score + 2**now

        elif ad_status == 0:
            ad_status = self.winPhase(hand_signal, now, com_dataList)
            current_score = score + 2**now

        elif ad_status == 1:
            ad_status = self.losePhase(hand_signal, now, com_dataList)
            current_score = score + now

        elif ad_status == 2:
            ad_status = self.win(score, now)
            current_score = score

        elif ad_status == 3:
            ad_status = self.lose(score, now)
            current_score = score

        elif ad_status == 4:
            current_score = score





        return {"ad_status": ad_status, "hand_signal": hand_signal, "Hscore": score, "now": now, "com_dataList": com_dataList, "current_score": current_score}
    #현재 점수와 컴퓨터의 손 모양을 리턴


if __name__ == "__main__":

    mjp = mukjjippa()
    result = mjp.ingame(None, 1, 2, 2, [0, 1, 2])
    print(result)
