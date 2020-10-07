import requests
import base64
from PIL import Image
import cv2
import numpy as np
from numpy import *
import os

path = "./imgsSrc/"
toPath = './imgsClipped/'
boxes = [(0, 0, 300, 300), (300, 0, 600, 300), (600, 0, 900, 300),
         (0, 300, 300, 600), (300, 300, 600, 600), (600, 300, 900, 600),
         (0, 600, 300, 900), (300, 600, 600, 900), (600, 600, 900, 900)]
img_size = 900


def clip():
    imgPath = path + "c_.jpg"
    imgPath = './ai/001.png'
    im = Image.open(imgPath)
    print(im.size)
    sector = 1
    # if not os.path.exists(dirs):
    #     os.makedirs(dirs)
    for box in boxes:
        region = im.crop(box)
        region.save(toPath + str(sector) + '.jpg')
        sector += 1


def interface():
    te = requests.get("http://47.102.118.1:8089/api/problem?stuid=041801420")
    te = te.text.split(',')
    code = te[0].split(":")[1]
    print(code[0], code[-1])
    img = base64.b64decode(code)
    with open('002.png', 'wb') as f:
        f.write(img)


def countImg(detectImg):
    # detectImg = './child/z_ (2)/_sub8.jpg'
    img = cv2.imread(detectImg)
    img = cv2.resize(img, (img_size, img_size))
    # print(img[:, :, 0].mean())
    height, width = 900, 900
    ave = 0
    for i in range(height):
        for j in range(width):
            ave += img[i][j] / img_size
    print(ave)


def countImgs():
    with open('./childIndex.txt','a+', encoding='utf-8')as text:
        root_dir = './child/'
        sub_list = os.listdir(root_dir)
        for folder in sub_list:
            img_list = os.listdir(os.path.join(root_dir, folder))
            for img_name in img_list:
                img_path = os.path.join(root_dir, folder, img_name)
                print(img_path)
                img = cv2.imread(img_path)
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (img_size, img_size))
                ave = 0
                for i in range(900):
                    for j in range(900):
                        ave += img[i][j] / img_size
                text.write(str(ave[0])+'\n')
                print(ave)


def produceChildImg():
    childboxes = [(0, 0, 300, 300), (300, 0, 600, 300), (600, 0, 900, 300),
         (0, 300, 300, 600), (300, 300, 600, 600), (600, 300, 900, 600),
         (0, 600, 300, 900), (300, 600, 600, 900), (600, 600, 900, 900)]
    img_list = os.listdir(path)
    for imgPath in img_list:
        if not os.path.exists('./child/'+imgPath.split('.')[0]+'/'):
            os.makedirs('./child/'+imgPath.split('.')[0]+'/')
        for cnt in range(1, 10):
            print(imgPath)
            img_path = './imgsSrc/'+imgPath
            print(img_path)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (img_size, img_size))
            vertex1 = [childboxes[cnt - 1][0], childboxes[cnt - 1][1]]
            vertex2 = [childboxes[cnt - 1][0], childboxes[cnt - 1][3]]
            vertex3 = [childboxes[cnt - 1][2], childboxes[cnt - 1][3]]
            vertex4 = [childboxes[cnt - 1][2], childboxes[cnt - 1][1]]
            rectangular = np.array([vertex1, vertex2, vertex3, vertex4])
            cv2.fillConvexPoly(img, rectangular, (256, 256, 256))
            # cv2.imshow('img', img)
            # cv2.waitKey(1000)
            cv2.imwrite('./child/'+imgPath.split('.')[0]+'/'+'_sub'+str(cnt)+'.png', img)


if __name__ == '__main__':
    # interface()
    countImg('./child/z_ (2)/_sub8.png')
    countImg('./ai/001.png')
    # produceChildImg()
    # clip()

    '''
    log:20201007---->>>>>
        一个晚上图片的识别还是没有完成
        思路是直接暴力求出每张原图的像素均值作为映射，对于目标图像也求出像素均值，对应过来即可找到相应字母
        然而不知道为什么来源相同的两张图乱序后像素均值竟是不同的
        不知道是否是算法上出了差错
        明天应再检查一下算法上的计算；
        
        深入一点的话，分割为9张小图分别计算，然后看匹配度来映射
        也方便后面给图片编序号
    '''