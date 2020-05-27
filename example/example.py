from qrtools import *

split_count = 29 # 29*29
thresold = 11
origineImage = cv.imread('example.jpg')

if __name__ == "__main__":
    img = thresholdimg(origineImage)
    img = cutimg(img)

    step = img.shape[1] // split_count
    data = open('data.txt', 'w')

    for curY in range(split_count):
        imglist = horizontally_split_img(img, split_count, curY * step, curY * step + 9, 5, 15)
        blackcountlist = [countblack(img) for img in imglist]
        blacks = [int(i >= thresold) for i in blackcountlist]
        if blacks.count(1) >= 25:
            imglist = horizontally_split_img(img, split_count, curY * step + 3, curY * step + 12, 5, 15)
            blackcountlist = [countblack(img) for img in imglist]
            blacks = [int(i >= thresold) for i in blackcountlist]
            print(blackcountlist)
            if blacks.count(1) >= 25:
                print('error!')
                showimglist(imglist)
                exit(0)
        print(blacks)

        for i in a:
            data.write(str(i))
        data.write('\r\n')

    data.close()
    parseFrom01('data.txt', 29)
