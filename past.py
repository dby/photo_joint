#coding: utf-8

#
# @note: 这里两张照片层叠选择的方法是：
#   假设两张照片的同一点的像素分别为A，B，则层叠之后该点得像素为(alpha取值在0和1之间)：
#       A * alpha + B * (1-alpha)
#

from __future__ import division
import PIL 
import Image
import numpy
import os
import random
import time
import ImageFont, ImageDraw

STAG = time.time()

# W_num: 一行放多少张照片
# H_num: 一列放多少张照片
# W_size: 照片宽为多少
# H_size: 照片高为多少
# root: 脚本的根目录
root=""
W_num =15
H_num = 15
W_size = 640
H_size = 360

# aval: 存放所有照片的路径
alpha = 0.5
aval = []

# name: transfer
# todo: 将照片转为一样的大小
def transfer(img_path, dst_width,dst_height):

    STA = time.time()
    im = Image.open(img_path)
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    s_w,s_h = im.size
    if s_w < s_h:
        im = im.rotate(90)
	
    #if dst_width*0.1/s_w > dst_height*0.1/s_h:
    #    ratio = dst_width*0.1/s_w
    #else:
    #    ratio = dst_height*0.1/s_h
    resized_img = im.resize((dst_width, dst_height), Image.ANTIALIAS)  
    resized_img = resized_img.crop((0,0,dst_width,dst_height))
    print "transfer Func Time %s"%(time.time()-STA)

    return resized_img

# name: getAllPhotos
# todo: 获得所有照片的路径
def getAllPhotos():
    STA = time.time()
    root = os.getcwd() + "/"
    src = root+"/photos/"
    for i in os.listdir(src):
	    if os.path.splitext(src+i)[-1] == ".jpg" or os.path.splitext(src+i)[-1] == ".png":
		    aval.append(src+i)
    print "getAllPhotos Func Time %s"%(time.time()-STA)

# name: createNevImg
# todo: 创建一张新的照片并保存
def createNevImg():
    STAA = time.time()
    iW_size = W_num * W_size
    iH_size = H_num * H_size
    print root
    I = numpy.array(transfer(root+"lyf.jpg", iW_size, iH_size)) * 1.0

    for i in range(W_num):
        for j in range(H_num):
            s = random.choice(aval)
            res = I[ j*H_size:(j+1)*H_size, i*W_size:(i+1)*W_size] * numpy.array(transfer(s, W_size, H_size))/255
            I[ j*H_size:(j+1)*H_size, i*W_size:(i+1)*W_size] = res

    img = Image.fromarray(I.astype(numpy.uint8))
    img = img.point(lambda i : i * 1.5)
    img.save("createNevImg_past.jpg")	
    print "createNevImg Func time %s"%(time.time()-STAA)


# name: newRotateImage
# todo: 将createnevimg中得到的照片旋转，粘贴到另外一张照片中
def newRotateImage():
    imName = "createNevImg_past.jpg"
    print "正在将图片旋转中..."
    STA = time.time()
    im = Image.open(imName)
    im2 = Image.new("RGBA", (W_size * int(W_num + 1), H_size * (H_num + 4)))
    im2.paste(im, (int(0.5 * W_size), int(0.8 * H_size)))
    im2 = im2.rotate(359)
    im2.save("newRotateImage_past.jpg")
    print "newRotateImage Func Time %s"%(time.time()-STA)


# name: writetoimage
# todo: 在图片中写祝福语
def writeToImage():
    print "正在向图片中添加祝福语..."
    STA = time.time()
    img = Image.open("newRotateImage_past.jpg")
    font = ImageFont.truetype('xindexingcao57.ttf', 600)
    draw = ImageDraw.Draw(img)
    draw.ink = 21 + 118*256 + 65*256*256

#    draw.text((0,H_size * 6),unicode("happy every day",'utf-8'),(0,0,0),font=font)

    tHeight = H_num + 1
    draw.text((W_size * 0.5, H_size * tHeight), "happy life written by python", font = font)
    img.save("final_past.jpg")
    print "writeToImage Func Time %s"%(time.time()-STA)


# name:
# todo: 入口函数
if __name__ == "__main__":

    getAllPhotos()
    createNevImg()
    newRotateImage()
    writeToImage()
    print "Total Time %s"%(time.time()-STAG)

