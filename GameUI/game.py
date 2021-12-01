import sys
import random
import traceback

class mukjjippa():

    def __init__(self):
        super().__init__()

    def start(self, hand_signal, com_dataList):#게임 시작 시 공수를 결정하는 부분
        com = random.choice(com_dataList)
        if (hand_signal == 0 and com == 1) or (hand_signal == 1 and com == 2) or (hand_signal == 2 and com == 0):
            return 0


        elif (hand_signal == 1 and com == 0) or (hand_signal == 2 and com == 1) or (hand_signal == 0 and com == 2):
            return 1

        elif hand_signal == com:
            return None




    def winPhase(self, hand_signal, com_dataList):
        com = random.choice(com_dataList)
        if hand_signal == 0:
            if com == 1:
                com_dataList.append(random.randrange(3))
                return 0
            elif com == 2:
                com_dataList.append(hand_signal)
                return 1
            elif com == 0:
                return 2

        elif hand_signal == 1:
            if com == 2:
                com_dataList.append(random.randrange(3))
                return 0
            elif com == 0:
                com_dataList.append(hand_signal)
                return 1
            elif com == 1:
                return 2

        elif hand_signal == 2:
            if com == 0:
                com_dataList.append(random.randrange(3))
                return 0
            elif com == 1:
                com_dataList.append(hand_signal)
                return 1
            elif com == 2:
                return 2

    def losePhase(self, hand_signal, com_dataList):
        com = random.choice(com_dataList)
        if hand_signal == 0:  # 이기고 들어왔을 때
            if com == 1:
                com_dataList.append(random.randrange(3))
                return 0
            elif com == 2:
                com_dataList.append(hand_signal)
                return 1
            elif com == 0:
                return 3

        elif hand_signal == 1:
            if com == 2:
                return 0
            elif com == 0:
                com_dataList.append(hand_signal)
                return 1
            elif com == 1:
               return 3
        elif hand_signal == 2:
            if com == 0:
                com_dataList.append(random.randrange(3))
                return 0
            elif com == 1:
                com_dataList.append(hand_signal)
                return 1
            elif com == 2:
                return 3


    def ingame(self, ad_status, hand_signal, current_score, gameStreak, com_dataList):

        current = current_score
        streak = gameStreak

        if ad_status == None:
            ad_status = self.start(hand_signal, com_dataList)
            current += 2 * streak

        elif ad_status == 0:
            ad_status = self.winPhase(hand_signal, com_dataList)
            current += 2 * streak

        elif ad_status == 1:
            ad_status = self.losePhase(hand_signal, com_dataList)
            current += 2 * streak

        elif ad_status == 2: # win
            ad_status = None
            current += 2 * streak

        elif ad_status == 3: # lose
            ad_status = None
            current += 2 * streak




        return {"ad_status": ad_status, "hand_signal": hand_signal, "com_dataList": com_dataList, "current_score": current}
    #현재 점수와 컴퓨터의 손 모양을 리턴


if __name__ == "__main__":

    mjp = mukjjippa()
    result = mjp.ingame(None, 1, [0, 1, 2])
    print(result)
