# -*- coding: utf-8 -*-
# @Time    : 2020/10/8 14:53
# @Author  : Breeze
# @Email   : 578450426@qq.com
"""
    用于与接口交互
    1、get到目标图片
    2、将目标图片计算出像素值，从而在childIndex中映射得到"坐标"，找到原图
    3、将原图均分九块，目标图片也均分九块，分别计算每一块的像素值从而确定打乱了的目标图片的编号
    4、将此编号返回与ai算法相结合
"""
from ai9 import ai as AI
import numpy as np
import requests
import json
from utils import getSequence
from ai7 import ai
import base64

url = "http://47.102.118.1:8089"


def showQuiz():
    api = "/api/challenge/list"
    Url = url + api
    re = requests.get(Url)
    te = eval(re.text)
    print("今天已有{}个赛题被发布".format(len(te)))
    for i in te:
        print(i)


def showRecod(uid):
    api = "/api/challenge/record/" + uid
    Url = url + api
    re = requests.get(Url)

    te = eval(re.text)
    for i in te:
        print(i)


def create():
    api = "/api/challenge/create"
    Url = url + api
    po = {
        "teamid": 56,
        "data": {
            "letter": "b",
            "exclude": 9,
            "challenge": [
                [7, 3, 5], [4, 0, 2], [6, 8, 1]
            ],
            "step": 7,
            "swap": [1, 3]
        },
        "token": "c5b0346e-1a39-43d1-86e2-b643fd15c818"
    }
    s = json.dumps(po)
    # print(s)
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url=Url, headers=headers, data=s)
    print(r.text)


def fight(uuid):
    api = "/api/challenge/start/"
    Url = url + api + uuid
    data = {
        "teamid": 56,
        "token": "c5b0346e-1a39-43d1-86e2-b643fd15c818"
    }
    s = json.dumps(data)
    # print(s)
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url=Url, headers=headers, data=s)
    r.text.replace("true", "none")
    te = r.text
    te = json.loads(te)
    # print(te)
    print("今日还剩挑战次数：{}".format(te["chanceleft"]))
    fightData = te["data"]
    img = base64.b64decode(fightData['img'])
    with open('test' + '.png', 'wb') as f:
        f.write(img)
    f.close()
    print("get test image successfully")
    print("saved to : ", './' + 'test' + '.png')
    origT, testT, step, swap, uuid = getSequence(1, fightData["step"], fightData["swap"], te["uuid"])
    o = np.array(origT).reshape(3, 3)
    t = np.array(testT).reshape(3, 3)
    o = list(o.tolist())
    t = list(t.tolist())
    mmap = dict(zip(['MoveUp', 'MoveLeft', 'MoveDown', 'MoveRight'], ['w', 'a', 's', 'd']))
    steps, swapped, seq = AI(t, o, swap, step)
    res = [mmap[i] for i in steps]
    print(res)
    p = ''.join(res)
    if len(seq) != 0:
        p = seq + p
    if swapped[0] == -1:
        swapped = [1, 1]
    submit(uuid, p, swapped)


def submit(uuid, operation, swap):
    api = "/api/challenge/submit"
    Url = url + api
    swap[0] += 1
    swap[1] += 1
    datas = {
        "uuid": str(uuid),
        "teamid": 56,
        "token": "c5b0346e-1a39-43d1-86e2-b643fd15c818",
        "answer": {
            "operations": str(operation),
            "swap": swap
        }
    }

    s = json.dumps(datas)
    print(s)
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url=Url, headers=headers, data=s)
    print(r.text)


def showRankList():
    api = "/api/rank"
    Url = url + api
    re = requests.get(Url)
    te = eval(re.text)
    for i in te:
        print(i)


def showTeamDetail(teamId):
    api = "/api/teamdetail/"
    Url = url + api + str(teamId)
    re = requests.get(Url)
    print(re.text)


def showProblem(teamId):
    api = "/api/team/problem/"
    Url = url + api + str(teamId)
    re = requests.get(Url)
    for i in eval(re.text):
        print(i)


if __name__ == '__main__':
    # showQuiz()
    # print("-------------------------------------")
    # showProblem(56)
    # showRecod("218ba788-b0a3-45d0-86b5-33b0e03e13c2")
    # create()
    # fight("7d8a94d9-193b-48d4-a0a7-9145781c40a3")
    showRankList()
    # showTeamDetail(56)
