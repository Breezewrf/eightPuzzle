# -*- coding: utf-8 -*-
from PIL import Image

path = "./imgsSrc/"
toPath = './imgsClipped/'
boxes = [(0, 0, 300, 300), (300, 0, 600, 300), (600, 0, 900, 300),
         (0, 300, 300, 600), (300, 300, 600, 600), (600, 300, 900, 600),
         (0, 600, 300, 900), (300, 600, 600, 900), (600, 600, 900, 900)]


def readImg():
    imgPath = path + "c_.jpg"
    im = Image.open(imgPath)
    print(im.size)
    sector = 1
    for box in boxes:
        region = im.crop(box)
        region.save(toPath+str(sector)+'.jpg')
        sector += 1


if __name__ == '__main__':
    readImg()
