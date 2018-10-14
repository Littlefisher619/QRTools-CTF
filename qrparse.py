#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Littlefisher
import cv2 as cv
import numpy as np
import os,sys
import matplotlib.pyplot as plt

WHITE=(255,255,255)
BLACK=(0,0,0)
IGNOREWARNING=False
def showWindow(img0,img1=None,mode=0):
    if(mode==0):
        # plt.ion()
        plt.figure("0 - QR-Tools By Littlefisher")
        plt.imshow(img0)
        if(img1.any!=None):
            plt.figure("1 - QR-Tools By Littlefisher")
            plt.imshow(img1)
        # plt.ioff()
        plt.show()
    else:
        cv.namedWindow('0 - QR-Tools By Littlefisher',cv.WINDOW_AUTOSIZE)
        cv.imshow('0 - QR-Tools By Littlefisher',img0)
        if(img1.any!=None):
            cv.namedWindow('1 - QR-Tools By Littlefisher',cv.WINDOW_AUTOSIZE)
            cv.imshow('1 - QR-Tools By Littlefisher',img1)

        cv.waitKey(0)
        cv.destroyAllWindows()

def inverse_color(image):
    height,width,temp = image.shape
    img2 = image.copy()

    for i in range(height):
        for j in range(width):
            img2[i,j] = (255-image[i,j][0],255-image[i,j][1],255-image[i,j][2]) 
    return img2

def valid(picsize,point):
    if(point[0]<0 or point[1]<0 or point[0]>picsize or point[1]>picsize):
        return False
    else:
        return True

def parseFromXY(filename,size):
    #-- file data parsefrom --#
    data=[]
    with open(filename,"r") as f:
        for line in f:
            line=line.strip()
            if(line==""):
                print("Empty line detected! Skip...")
                continue
            tmp=line.split(" ")

            try:
                data.append((int(tmp[0]),int(tmp[1])))
            except:
                print("Illgeal data format:",tmp,",Skip...")
                
    
    #-- init the picture --#
    img = np.zeros((size, size, 3), np.uint8)
    cv.rectangle(img, (0,0), (size,size), WHITE,-1)

    #-- print data in picture --#
    for p in data:
        if(valid(size,p) or IGNOREWARNING):
            cv.rectangle(img, p, p, BLACK)
        else:
            print("Warning: ", p ,"is out of range!")

    showWindow(img,inverse_color(img))

def parseFrom01(filename,size):
    #-- init the picture --#
    img = np.zeros((size, size, 3), np.uint8)
    cv.rectangle(img, (0,0), (size,size), WHITE,-1)

    with open(filename,"r") as f:
        curX=0
        curY=0
        chwhite=''
        for line in f:
            line=line.strip()
            if(line==""):
                print("Empty line detected! Skip...")
                continue
            #-- choose the first point as white --#
            if(chwhite==''):
                chwhite=line[0]

            curX=0
            for ch in line:
                p=(curX,curY)
                if(valid(size,p) or IGNOREWARNING):
                    if(chwhite!=ch):
                        cv.rectangle(img, p, p, BLACK,-1)
                    else:
                        cv.rectangle(img, p, p, WHITE,-1)
                else:
                    print("Warning: ", p ,"is out of range!")

                curX+=1
            pass

            curY+=1   
        pass
    pass

    showWindow(img,inverse_color(img))

def main(args):
    if(len(args)<3):
        print("Illegal arguments! Size:",len(args))
        print("Help:\n\tqrparse.py <mode: xy | 01> <filename> <size> [ignore: ignore]")
        exit(0)


    mode=args[0].strip()
    filename=args[1].strip()
    sizestr=args[2].strip()


    try:
        size=int(sizestr)
    except:
        print("Illegal size specified!")
        print("Help:\n\tqrparse.py <mode: xy | 01> <filename> <size> [ignore: ignore]")
        exit(0)

    if(len(args)>=4):
        ignorestr=args[3].strip()
        if(ignorestr=="ignore"):
            IGNOREWARNING=True
        else:
            print("Unknown agrument:",ignorestr)
            print("Help:\n\tqrparse.py <mode: xy | 01> <filename> [ignore: ignore]")
            exit(0)

    if(mode=="xy"):
        parseFromXY(filename,size)
    else:
        if(mode=="01"):
            parseFrom01(filename,size)
        else:
            print("Unknown Mode! You must specify \"xy\" or \"01\" in the first argument")
            print("Help:\n\tqrparse.py <mode: xy | 01> <filename> <size> <ignore>")

if __name__ == '__main__':
    main(sys.argv[1:])