#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

# Author: Littlefisher
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
IGNOREWARNING = False


def showWindow(img0, img1=None, mode=0):
    if (mode == 0):
        # plt.ion()
        plt.figure("0 - QR-Tools By Littlefisher")
        plt.imshow(img0)
        if (img1.any != None):
            plt.figure("1 - QR-Tools By Littlefisher")
            plt.imshow(img1)
        # plt.ioff()
        plt.show()
    else:
        cv.namedWindow('0 - QR-Tools By Littlefisher', cv.WINDOW_AUTOSIZE)
        cv.imshow('0 - QR-Tools By Littlefisher', img0)
        if (img1.any != None):
            cv.namedWindow('1 - QR-Tools By Littlefisher', cv.WINDOW_AUTOSIZE)
            cv.imshow('1 - QR-Tools By Littlefisher', img1)

        cv.waitKey(0)
        cv.destroyAllWindows()

# 反转颜色
def inverse_color(image):
    height, width, temp = image.shape
    img2 = image.copy()

    for i in range(height):
        for j in range(width):
            img2[i, j] = (255 - image[i, j][0], 255 - image[i, j][1], 255 - image[i, j][2])
    return img2

# 判断坐标点是否越出边界
def valid(picsize, point):
    if (point[0] < 0 or point[1] < 0 or point[0] > picsize or point[1] > picsize):
        return False
    else:
        return True

# 将图片灰度化、二值化
def thresholdimg(img):
    image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    retval, img = cv.threshold(image, 127, 255, cv.THRESH_BINARY)

# 计算二值化后的图片中的黑像素个数
def countblack(img):
    blackcnt = 0

    for j in range(img.shape[0]):
        for i in range(img.shape[1]):
            if img[j, i] == 0:
                blackcnt += 1
    # print(img.shape, blackcnt)

    return blackcnt

# 在一个横向区域里对图片进行纵向分割，分割成指定的块数
# 需要指定两个纵坐标，作为横向区域的范围
# count 决定了纵向切割要切成多少片
# offset_x0/x1 对每个切片再进行进一步水平分割
# 改变y0/y1 循环调用函数可实现对整个图片的分割
def horizontally_split_img(img, split_count, y0, y1, offset_x0, offset_x1):
    step = img.shape[0] // split_count
    imgs = []
    for i in range(29):
        a, b = i * step + offset_x0, i * step + offset_x1
        t = img[y0:y1, a:b]
        imgs.append(t)

    return imgs



# 逐个显示list中的所有图片，按q强制退出
def showimglist(imgs):
    for i in imgs:
        cv.imshow('img', i)
        if (cv.waitKey(0) == ord('q')):
            break

# 裁切图片，删去图片中空白的部分
def cutimg(img):
    x = [list(img[i]).count(255) != img.shape[1] for i in range(0, img.shape[0])]
    x1 = x.index(True)
    x.reverse()
    x2 = img.shape[0] - x.index(True) - 1
    print(x1, x2)
    y = [list(img[:, i]).count(255) != img.shape[0] for i in range(0, img.shape[1])]
    y1 = y.index(True)
    y.reverse()
    y2 = img.shape[1] - y.index(True) - 1
    print(y1, y2)
    return img[x1:x2, y1:y2]

# 从给出的坐标点生成二维码图片
def parseFromXY(filename, size):
    # -- file data parsefrom --#
    data = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if (line == ""):
                print("Empty line detected! Skip...")
                continue
            tmp = line.split(" ")

            try:
                data.append((int(tmp[0]), int(tmp[1])))
            except:
                print("Illgeal data format:", tmp, ",Skip...")

    # -- init the picture --#
    img = np.zeros((size, size, 3), np.uint8)
    cv.rectangle(img, (0, 0), (size, size), WHITE, -1)

    # -- print data in picture --#
    for p in data:
        if (valid(size, p) or IGNOREWARNING):
            cv.rectangle(img, p, p, BLACK)
        else:
            print("Warning: ", p, "is out of range!")

    showWindow(img, inverse_color(img))

# 从给出的由两种字符分别代表白像素和黑像素的文件，转换出二维码
def parseFrom01(filename, size):
    # -- init the picture --#
    img = np.zeros((size, size, 3), np.uint8)
    cv.rectangle(img, (0, 0), (size, size), WHITE, -1)

    with open(filename, "r") as f:
        curX = 0
        curY = 0
        chwhite = ''
        for line in f:
            line = line.strip()
            if (line == ""):
                print("Empty line detected! Skip...")
                continue
            # -- choose the first point as white --#
            if (chwhite == ''):
                chwhite = line[0]

            curX = 0
            for ch in line:
                p = (curX, curY)
                if (valid(size, p) or IGNOREWARNING):
                    if (chwhite != ch):
                        cv.rectangle(img, p, p, BLACK, -1)
                    else:
                        cv.rectangle(img, p, p, WHITE, -1)
                else:
                    print("Warning: ", p, "is out of range!")

                curX += 1
            pass

            curY += 1
        pass
    pass

    showWindow(img, inverse_color(img))


def main(args):
    if (len(args) < 3):
        print("Illegal arguments! Size:", len(args))
        print("Help:\n\tqrparse.py <mode: xy | 01> <filename> <size> [ignore: ignore]")
        exit(0)

    mode = args[0].strip()
    filename = args[1].strip()
    sizestr = args[2].strip()

    try:
        size = int(sizestr)
    except:
        print("Illegal size specified!")
        print("Help:\n\tqrparse.py <mode: xy | 01> <filename> <size> [ignore: ignore]")
        exit(0)

    if (len(args) >= 4):
        ignorestr = args[3].strip()
        if (ignorestr == "ignore"):
            IGNOREWARNING = True
        else:
            print("Unknown agrument:", ignorestr)
            print("Help:\n\tqrparse.py <mode: xy | 01> <filename> [ignore: ignore]")
            exit(0)

    if (mode == "xy"):
        parseFromXY(filename, size)
    else:
        if (mode == "01"):
            parseFrom01(filename, size)
        else:
            print("Unknown Mode! You must specify \"xy\" or \"01\" in the first argument")
            print("Help:\n\tqrparse.py <mode: xy | 01> <filename> <size> <ignore>")




if __name__ == '__main__':
    main(sys.argv[1:])
