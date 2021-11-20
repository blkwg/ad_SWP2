import random

def kbb(now, Score):
    user_status = None
    com_dataList = [0, 1, 2]
    while now == 0:
        user = input("Enter 가위/바위/보: ")
        com = random.choice(com_dataList)
        if com == 1:
            print("com: 가위")
        elif com == 2:
            print("com: 보")
        elif com == 0:
            print("com: 바위")
        if user != com:
            now = 1
            if user == 0 & com == 1:
                user_status = 0
            elif user == 1 & com == 2:
                user_status = 0
            elif user == 2 & com == 0:
                user_status = 0
            else:
                user_status = 1
    mjp(user_status, now, com_dataList, Score)



def mjp(stat, length, dataList, fullScore):
    #이기고 들어갔을 때
    if stat == 0:
        print("공격")
        user = input("가위/바위/보>>")
        if user == "가위":
            user = 1
        elif user == "바위":
            user = 0
        elif user == "보":
            user = 2

        #컴퓨터가 손모양을 선택하고, 출력하는 부분
        com = random.choice(dataList)
        if com == 1:
            print("com: 가위")
        elif com == 2:
            print("com: 보")
        elif com == 0:
            print("com: 바위")


        #유저가 이겼을 때: -컴퓨터는 임의의 손 모양의 확률을 증가시킨다.
        if (user == 0 and com == 1) or (user == 1 and com == 2) or (user == 2 and com == 0):
            dataList.append(random.randrange(3))
            length += 1
            #현재 점수를 보여준다. 현재 점수 = 최종 점수(얻을 점수 반영 전) + 얻을 점수
            print('current Score:', fullScore + 2**length)
            print()
            mjp(0, length, dataList, fullScore)

        #유저가 졌을 때: 컴퓨터는 컴퓨터가 낸 손 모양의 확률을 증가시킨다.
        elif (user == 1 and com == 0) or (user == 2 and com == 1) or (user == 0 and com == 2):
            dataList.append(com)
            length += 1
            print('current Score:', fullScore + 2 ** length)
            print()
            mjp(1, length, dataList, fullScore)

        #승부가 났다-여기서는 승리했다.
        elif user == com:
            print("승리!")
            # 최종 점수 fullScore에 얻은 점수를 합산한다.
            fullScore += 2**length
            print("Current Score:", fullScore)
            # 묵찌빠에서 질 때까지 게임을 진행하므로, 새로운 판을 시작한다.
            kbb(0, fullScore)

    #지고 들어갔을 때
    elif stat == 1:
        print("수비")
        user = input("가위/바위/보>>")
        if user == "가위":
            user = 1
        elif user == "바위":
            user = 0
        elif user == "보":
            user = 2

        #컴퓨터가 손 모양을 선택한다.
        com = random.choice(dataList)
        if com == 1:
            print("com: 가위")
        elif com == 2:
            print("com: 보")
        elif com == 0:
            print("com: 바위")

        #유저가 이겼을 때- user_status == 0인 경우와 동일.
        if (user == 0 and com == 1) or (user == 1 and com == 2) or (user == 2 and com == 0):
            dataList.append(random.randrange(3))
            length += 1
            print('current Score:', fullScore + 2**length)
            print()
            mjp(0, length, dataList, fullScore)

        #유저가 졌을 때- user_status == 0인 경우와 동일.
        elif (user == 1 and com == 0) or (user == 2 and com == 1) or (user == 0 and com == 2):
            dataList.append(com)
            length += 1
            print('current Score:', fullScore + 2 ** length)
            print()
            mjp(1, length, dataList, fullScore)

        #승부가 났을 때- 점수 합산을 한다.
        elif user == com:
            #print("패배...")
            fullScore += 2**length
            print("Score:", fullScore)




torch = "Y"


while torch == 'Y':
    score = 0
    user_status = None
    now = 0

    kbb(now, score)




    torch = input("계속하시겠습니까?... [Y/N]")

