import PIL 
import Image
import numpy
import os
import random

def transfer(img_path, dst_width,dst_height):
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

    return resized_img


root = os.getcwd()
src = root+"/photos/"
print "src is %s" % src
aval = []
for i in os.listdir(src):
	if os.path.splitext(src+i)[-1] == ".jpg" or os.path.splitext(src+i)[-1] == ".png":
		aval.append(src+i)

W_num =15
H_num = 15
W_size = 640
H_size = 360

alpha = 0.5

I = numpy.array(transfer(root+"/lyf.jpg", W_num*W_size, H_num*H_size)) * 0.8
print I
print I.shape

for i in range(W_num):
    for j in range(H_num):
        s = random.choice(aval)
        I[ j*H_size:(j+1)*H_size, i*W_size:(i+1)*W_size] = I[ j*H_size:(j+1)*H_size, i*W_size:(i+1)*W_size] * numpy.array(transfer(s, W_size, H_size))/255
        #I[ j*H_size:(j+1)*H_size, i*W_size:(i+1)*W_size] += numpy.array(transfer(s, W_size, H_size))*alpha

img = Image.fromarray(I.astype(numpy.uint8))
img = img.point(lambda i : i * 1.5)
img.save("%s_2res.jpg"%alpha)	
