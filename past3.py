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
import numexpr
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

# aval: 存放所有的照片的路径
aval = []
alpha = 0.5

# name: treansfer
# todo: 将照片转为一样的大小
def transfer(img_path,dst_width,dst_height):
    im = Image.open(img_path)
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    s_w,s_h = im.size
    if s_w < s_h:
        im=im.rotate(90)
	
	#if dst_width/s_w > dst_height/s_h:
	#	ratio = dst_width/s_w
	#else:
	#	ratio = dst_height/s_h

    STA = time.time()
    resized_img = im.resize((dst_width, dst_height))
    print "Transfer Func Time %s"%(time.time()-STA)
    return numpy.array(resized_img)[:dst_height, :dst_width]

	
# name: getAllPhtots
# todo: 获得所有照片的路径
def getAllPhtots():
    root = os.getcwd()+"/"
    src = root+"photos/"
    for i in os.listdir(src):
	    if os.path.splitext(src+i)[-1] == ".jpg":
		    aval.append(src+i)


# name: createNevImg
# todo: 创造一张新的图片，并保存
def createNevImg():
    iW_size = W_num * W_size
    iH_size = H_num * H_size
    I = numpy.array(transfer(root+"lyf.jpg", iW_size, iH_size))
    I = numexpr.evaluate("""I*(1-alpha)""")

    for i in range(W_num):
	    for j in range(H_num):
		    SH = I[(j*H_size):((j+1)*H_size), (i*W_size):((i+1)*W_size)]
		    STA = time.time()
		    DA = transfer(random.choice(aval), W_size, H_size)
		    print "Cal Func Time %s"%(time.time()-STA)
		    res  = numexpr.evaluate("""SH+DA*alpha""")
		    I[(j*H_size):((j+1)*H_size), (i*W_size):((i+1)*W_size)] = res
		

    Image.fromarray(I.astype(numpy.uint8)).save("createNevImg_%s_past3.jpg"%alpha)	


# name: newRotateImage
# todo: 将createnevimg中得到的照片旋转，粘贴到另外一张照片中
def newRotateImage():
    imName = "createNevImg_%s_past3.jpg" % alpha
    print "正在将图片旋转中..."
    im = Image.open(imName)
    im2 = Image.new("RGBA", (W_size * int(W_num + 1), H_size * (H_num + 4)))
    im2.paste(im, (int(0.5 * W_size), int(0.8 * H_size)))
    im2 = im2.rotate(359)
    im2.save("newRotateImage_%s_past3.jpg"%alpha)
    

# name: writetoimage
# todo: 在图片中写祝福语
def writeToImage():
    print "正在向图片中添加祝福语..."
    img = Image.open("newRotateImage_%s_past3.jpg" % alpha)
    font = ImageFont.truetype('xindexingcao57.ttf', 600)
    draw = ImageDraw.Draw(img)
    draw.ink = 21 + 118*256 + 65*256*256

#    draw.text((0,H_size * 6),unicode("happy every day",'utf-8'),(0,0,0),font=font)

    tHeight = H_num + 1
    draw.text((W_size * 0.5, H_size * tHeight), "happy life written by python", font = font)
    img.save("final_%s_past3.jpg" % alpha)


# name:
# todo: 入口函数
if __name__ == "__main__":

    getAllPhtots()
    createNevImg()
    newRotateImage()
    writeToImage()
    print "Total Time %s"%(time.time()-STAG)

