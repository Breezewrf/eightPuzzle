import requests
import base64
from PIL import Image
import cv2
import numpy as np
from numpy import *
import os
import json
from ai7 import ai

path = "./imgsSrc/"
toPath = './imgsClipped/'
boxes = [(0, 0, 300, 300), (300, 0, 600, 300), (600, 0, 900, 300),
         (0, 300, 300, 600), (300, 300, 600, 600), (600, 300, 900, 600),
         (0, 600, 300, 900), (300, 600, 600, 900), (600, 600, 900, 900)]
img_size = 900


def clip(imgPath):
    """

    :param imgPath: input the image's path which you wanna clip
                    string;
    :return: void
            clipped images saved to ./imgsClipped/[img_name]/[sector[1,2,3,...]].png
    """
    if not os.path.exists('./imgsClipped/' + imgPath.split('/')[-1].split('.')[0] + '/'):
        os.makedirs('./imgsClipped/' + imgPath.split('/')[-1].split('.')[0] + '/')
    toPath = './imgsClipped/' + imgPath.split('/')[-1].split('.')[0] + '/'
    print('./imgsClipped/' + imgPath.split('/')[-1].split('.')[0] + '/')
    im = Image.open(imgPath)
    print(im.size)
    sector = 1
    # if not os.path.exists(dirs):
    #     os.makedirs(dirs)
    for box in boxes:
        region = im.crop(box)
        region.save(toPath + str(sector) + '.jpg')
        sector += 1


def interface(name):
    te = requests.get("http://47.102.118.1:8089/api/problem?stuid=041801420")
    te = te.text.split(',')
    code = te[0].split(":")[1]
    print(code[0], code[-1])
    img = base64.b64decode(code)
    with open(name + '.png', 'wb') as f:
        f.write(img)
    f.close()
    print("get test image successfully")
    print("saved to : ", './' + name + '.png')


def interfaceJson(name):
    te = requests.get("http://47.102.118.1:8089/api/problem?stuid=041801420")
    te = eval(te.text)
    img = base64.b64decode(te['img'])
    step = te['step']
    swap = te['swap']
    uuid = te['uuid']
    with open(name + '.png', 'wb') as f:
        f.write(img)
    f.close()
    print("get test image successfully")
    print("saved to : ", './' + name + '.png')
    return step, swap, uuid


def countImg(detectImg):
    """
    处理对象是单张图片，用于处理接口get到的测试图片，计算出对应像素值(Index)
    :param detectImg: the relative path to a single image
    :return: count the img[:, :, 0].mean() of the image
    example:
        # countImg('./imgsClipped/001/4.jpg')
        # countImg('./ai/001.png')
    """
    # detectImg = './child/z_ (2)/_sub8.jpg'
    img = cv2.imread(detectImg)
    img = cv2.resize(img, (img_size, img_size))
    print(img[:, :, 0].mean())
    return str(img[:, :, 0].mean())


def count(folderPath):
    blocks = []
    with open(folderPath + '/childIndex.txt', 'a+', encoding='utf-8')as text:
        root_dir = folderPath
        img_list = os.listdir(root_dir)
        for img_name in img_list:
            # print(img_name.split('.')[-1])
            if img_name.split('.')[-1] != 'png' and img_name.split('.')[-1] != 'jpg':
                continue
            img_path = os.path.join(root_dir, img_name)
            print(img_path)
            img = cv2.imread(img_path)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (img_size, img_size))
            # ave = 0
            # for i in range(900):
            #     for j in range(900):
            #         ave += img[i][j] / img_size
            # text.write(str(ave[0]) + '\n')
            # print(ave)
            val = img[:, :, 0].mean()
            text.write(str(val) + '\n')
            blocks.append(val)
    text.close()
    return blocks


def countImgs(folderPath):
    """
    注意：由于采用的是img[:, :, 0].mean()，速度较快，仅用于映射识别到原图像
    制作索引映射集合,已通过验证，请不要修改此函数
    :param folderPath: 输入一个文件夹路相对径--'./child/'
    :return: 计算出child文件夹内所有子文件夹下的所有字母（不同形态空白）的像素均值
            采用img[:, :, 0].mean()，目的是标记每一张图片，作为索引
    example:
        countImgs('./child/')

    :exception
        62.933141975308644
    """
    with open(folderPath + '/childIndex.txt', 'a+', encoding='utf-8')as text:
        root_dir = folderPath
        sub_list = os.listdir(root_dir)
        for folder in sub_list:
            print(folder)
            if folder.split('.')[-1] == 'txt':
                continue
            img_list = os.listdir(os.path.join(root_dir, folder))
            for img_name in img_list:
                if img_name.split('.')[-1] != 'png' and img_name.split('.')[-1] != 'jpg':
                    continue
                img_path = os.path.join(root_dir, folder, img_name)
                print(img_path)
                img = cv2.imread(img_path)
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # img = cv2.resize(img, (img_size, img_size))
                # ave = 0
                # for i in range(900):
                #     for j in range(900):
                #         ave += img[i][j] / img_size
                # text.write(str(ave[0]) + '\n')
                # print(ave)
                text.write(str(img[:, :, 0].mean()) + '\n')
                print("index:", str(img[:, :, 0].mean()))
    text.close()


def mapped(index):
    childIndex = './child/childIndex.txt'
    cnt = 0
    with open(childIndex, 'r', encoding='utf-8') as Index:
        for dex in Index.readlines():
            dex = dex.strip('\n')
            if dex == index:
                break
            cnt += 1
    print(cnt)
    Index.close()
    cnt += 1
    charaList = os.listdir('./child/')
    charaList.remove('childIndex.txt')  # 注意文件列表中还有这个.txt，必须要remove掉否则会影响映射
    # 需要防止越界，如果恰好被9整除的话，应归属上一个字母的最后一张（sub9）
    if cnt % 9 == 0:
        charaIndex = cnt // 9 - 1
        _subIndex = 9
    else:
        charaIndex = cnt // 9
        _subIndex = cnt % 9
    chara = charaList[charaIndex]
    chara_sub = '_sub' + str(_subIndex) + '.png'
    origImgPath = os.path.join('./child', chara, chara_sub)
    print("The original image is : ", origImgPath)
    # img = cv2.imread(origImgPath)
    # cv2.imshow('orig', img)
    # cv2.waitKey(6000)
    return origImgPath


def produceChildImg():
    """
    预处理
    对原完整图像一次取1/9块填充白块
    分别保存在child中
    :return:
    """
    childboxes = [(0, 0, 300, 300), (300, 0, 600, 300), (600, 0, 900, 300),
                  (0, 300, 300, 600), (300, 300, 600, 600), (600, 300, 900, 600),
                  (0, 600, 300, 900), (300, 600, 600, 900), (600, 600, 900, 900)]
    img_list = os.listdir(path)
    for imgPath in img_list:
        if not os.path.exists('./child/' + imgPath.split('.')[0] + '/'):
            os.makedirs('./child/' + imgPath.split('.')[0] + '/')
        for cnt in range(1, 10):
            print(imgPath)
            img_path = './imgsSrc/' + imgPath
            print(img_path)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (img_size, img_size))
            vertex1 = [childboxes[cnt - 1][0], childboxes[cnt - 1][1]]
            vertex2 = [childboxes[cnt - 1][0], childboxes[cnt - 1][3] - 1]
            vertex3 = [childboxes[cnt - 1][2] - 1, childboxes[cnt - 1][3] - 1]
            vertex4 = [childboxes[cnt - 1][2] - 1, childboxes[cnt - 1][1]]
            rectangular = np.array([vertex1, vertex2, vertex3, vertex4])
            cv2.fillConvexPoly(img, rectangular, (256, 256, 256))
            # cv2.imshow('img', img)
            # cv2.waitKey(1000)
            cv2.imwrite('./child/' + imgPath.split('.')[0] + '/' + '_sub' + str(cnt) + '.png', img)


# if __name__ == '__main__':
def getSequence():
    step, swap, uuid = interfaceJson('test')
    testIndex = countImg('./test.png')
    # origImgPath -> ./child\A_ (2)\_sub7.png
    origImgPath = str(mapped(testIndex))
    # countImg('./child/O_/_sub8.png')

    clip('./test.png')
    # 因为origImgPath是os.path.join生成的，并不全是相对路径的/，所以不能直接用clip函数中自带的split方法
    clip(origImgPath.replace('\\', '/'))

    testBlocks = count("./imgsClipped/test")
    origBlocks = count('./imgsClipped/' + str(origImgPath).split('\\')[-1].split('.')[0])
    # zero = testBlocks.index(255)
    # # 在返回的时候不能简单编号，因为"0"必须在空白处
    # res = []
    # for item in origBlocks:
    #     res.append(str(testBlocks.index(item)))
    #
    # org = [i for i in '012345678']
    # temp = org[zero]
    # org[zero] = '0'
    # org[0] = temp
    # # org : ['2', '1', '0', '3', '4', '5', '6', '7', '8']
    # # print(org)
    #
    # ta = res.index('0')
    # tb = res.index(temp)
    # res[ta] = temp
    # res[tb] = '0'
    # print(res)
    # packUp = [''.join(org), ''.join(res)]
    # print(packUp)

    # ----------------------------------
    origT = []
    testT = []
    cnt = 1
    for item in origBlocks:
        if item == 255:
            origT.append(0)
        else:
            origT.append(cnt)
            cnt += 1
    # print(origT)
    for item in testBlocks:
        testT.append(origT[origBlocks.index(item)])
    # print(testT)
    # packUp = [''.join([str(i) for i in origT]), ''.join([str(j) for j in testT])]
    print("orig: ", origT, '\n', "test:", testT)
    print("swap at steps:", step)
    swap[0] -= 1
    swap[1] -= 1
    print("to be swap:", swap)
    return origT, testT, step, swap, uuid
    # preprocess function:
    # produceChildImg() # git clone后第一次运行代码请用该函数预处理原图片
    # countImgs('./child/') # 已得到childIndex，不必重复运行此函数


def post(uuid, operation):
    postUrl = 'http://47.102.118.1:8089/api/answer'
    datas = {
        "uuid": uuid,
        "answer": {
            "operations": operation,
            "swap": [1, 2]
        }
    }
    s = json.dumps(datas)
    r = requests.post(postUrl, data=s)


if __name__ == '__main__':
    origT, testT, step, swap, uuid = getSequence()
    o = np.array(origT).reshape(3, 3)
    t = np.array(testT).reshape(3, 3)
    o = list(o.tolist())
    t = list(t.tolist())
    mmap = dict(zip(['MoveUp', 'MoveLeft', 'MoveDown', 'MoveRight'], ['w', 'a', 's', 'd']))
    res = [mmap[i] for i in ai(t, o, swap, step)]
    print(res)
    p = ''.join(res)
    post(uuid, p)
    '''
    log:20201007---->>>>>
        一个晚上图片的识别还是没有完成
        思路是直接暴力求出每张原图的像素均值作为映射，对于目标图像也求出像素均值，对应过来即可找到相应字母
        然而不知道为什么来源相同的两张图乱序后像素均值竟是不同的
        不知道是否是算法上出了差错
        明天应再检查一下算法上的计算；
        
        深入一点的话，分割为9张小图分别计算，然后看匹配度来映射
        也方便后面给图片编序号
        
    log:20201008/11:36---->>>>>
        根据对九块图片分别计算像素值，发现每张图片其实只有1/9是有问题的，造成了最后整张算出来的像素值无法匹配
        测试了001，002两张图片，都是在白块右侧的一张图（1/9图）出现了一条狭窄的白线
        分析应该是画填充白块时出现bug，对于顶点的右边界超出了估计是1个单位
        
                /11:58---->>>>>
        问题完美解决！
        关键get到的样例好像都是只截取第九块为空白，不知道后面会不会有其他情况
        现在只加上了两个顶点要-1，那这样的话岂不是其他顶点还有可能越界？不大懂
        下午计划把映射做好，今天完成识别任务！冲！
        
    log:20201008/14:42----->>>>>
        62.933141975308644属于图片002.png，对应child/O_/_sub8.png
            其在childIndex中第为161行，floor(161/9) = 17，161%9 = 8
            (child文件夹序列第17个（0开始计数）-->>"./O_/";第8张图片(0开始计数)-->>"/_sub8.jpg")
    
    log:20201008/17:15----->>>>>
        已经完成对get到的测试图片的识别
        并比对原图，返回相应的九片图片的编号
        下一步将与ai结合（应该很快完成这部分）
        另外就是让ai输出wasd序列，并且返回post（界面gui的设计先放着）
    
    log:20201008/20:55----->>>>>>
        ai有问题，难搞
        输入的原图和乱图的序列可能需要调整
        只能明天解决了
        
    log:20201009/21.29----->>>>>
        庆幸今天搞完了八数码ai，已经可以输出正确的解体路径了
        还差交换的问题，明天来弄：
        def sswap(step, swap, node, s):
        # 将node.State平展为一维后，由swap数组来交换顺序得到新的序列，从头执行ai()
        虽然说这样可能比较耗时间，但是目前只能这样了
        明天需要完成：
            1、写完swap的函数
            2、swap后如果无解还要根据启发值来确定又一次的交换
            
    log:20201010/23:05----->>>>>
        又打了一个晚上代码。。好累
        手腕都有点麻木了
        作业多得一批，还要同时兼顾软件杯，明天还有实验，真897了
        晚上改了swap的情况，如果一开始get到的图片就是无解，那么直接去swap，或者等到走到step了再swap
        swap中包括判断强制交换是否有解，如果没有，需要手动交换
        明天还要检查一下各个输出，看一下有没有bug
        今天太累了不想看了
    '''
