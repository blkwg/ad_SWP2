# 유저 추가
def Add(user):
    name = input('닉네임 입력 : ')
    if (name not in user) == True:
        print('닉네임 생성')

    else:
        # 이름이 중복일 경우
        print('이미 존재하는 닉네임')
        return Add(user)

    user[name] = 0
    return user

# 순위 확인 - 동점일 경우 먼저 생성된 유저의 순위가 더 높음
def Show(user):
    i = 1
    for key, value in sorted(user.items(), key=lambda x: x[1], reverse=True):
        print(str(i)+'위: ' + str(key) + ' ' + str(value) +'점')
        i += 1

    return user


def Find(user):
    search_name = input('검색할 닉네임 입력 : ')

    if (search_name in user) == True:
        print(search_name, ':', user.get(search_name), ' ')

    else:
        print('닉네임 없음')

    return user


# 새로운 점수 업데이트
def Update(user):
    update_name = input('수정할 닉네임 입력 : ')

    if (update_name in user) == True:
        new_score = int(input('새로운 점수 : '))
        # 새로운 점수가 더 높다면
        if (new_score > user[update_name]):
            user[update_name] = new_score
    else:
        print('없는 닉네임')

    return user


def Delete(user):
    delete_name = input('삭제할 닉네임 입력 : ')

    if (delete_name in user) == True:
        user.pop(delete_name)
    else:
        print('닉네임 없음')

    return user

# ===================================================================

user = dict()

while True:
    select = int(input("1.입력 2.출력 3.검색 4.수정 5.삭제 6.종료 \n"))

    if select == 1:
        user = Add(user)

    elif select == 2:
        user = Show(user)

    elif select == 3:
        user = Find(user)

    elif select == 4:
        user = Update(user)

    elif select == 5:
        user = Delete(user)

    else:
        print("종료")
        break
