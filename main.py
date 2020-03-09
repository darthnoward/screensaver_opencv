#! /usr/bin/python3 

# Dependency: Python3, OpenCV, NumPy, i3lock, fortune.

import numpy as np 
import cv2 
from os import system 
from subprocess import run, PIPE

system('xfce4-screenshooter -f --save ~/Scripts/python/cv/lock_screen/pre.png')

img = cv2.imread('/home/noward/Scripts/python/cv/lock_screen/pre.png',cv2.IMREAD_COLOR)
arch = cv2.imread('/home/noward/Scripts/python/cv/lock_screen/arch_white.png')

resize_factor = 0.3
arch = cv2.resize(arch, (0,0), fx=resize_factor, fy=resize_factor) 

img = cv2.GaussianBlur(img, (25,25), cv2.BORDER_DEFAULT)
img = cv2.blur(img,(20,20))
img = cv2.GaussianBlur(img, (25,25), cv2.BORDER_DEFAULT)

mask = cv2.inRange(arch, np.array([1,1,1]),np.array([255,255,255]))
invert_mask = cv2.bitwise_not(mask)

x,y,channel = arch.shape
tmp = int(x/2)
height, width, channel = img.shape
start_height = int(height/2 - tmp)
start_width = int(width/2 - tmp)
end_height = start_height + x
end_width = start_width + y

r = 25
g = 173
b = 255
percent = 0.6
arch[mask == 255] = (int(b*percent),int(g*percent),int(r*percent))
selection = img[start_height:end_height,start_width:end_width]

# for i in range(selection.shape[0]):
    # for u in range(selection.shape[1]):
        # if mask[i][u] == 255:
#             selection[i][u] = selection[i][u]*0.4 + arch[i][u]*0.6 
selection[mask == 255] = selection[mask == 255] * 0.4
selection[mask == 255 ] += arch[mask == 255]

img[start_height:end_height,start_width:end_width] = selection

font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX

i = 7757
while (i >= width*2):
    text = run(['fortune'], stdout=PIPE).stdout.decode('utf-8').replace("\n"," ").replace("(", " ").replace(")", " ").replace("\t", "    ")
    textsize = cv2.getTextSize(text,font,1.5,2)[0]
    i = textsize[0]
if i <= width:
    textX = int((width - textsize[0]) / 2)
    textY = int((height + end_height - textsize[1]) / 2)

    cv2.putText(img, text, (textX, textY), font, 1.5 ,(143, 33, 217), 2)
else:
    textX = int((width - textsize[0]/2) / 2)
    textY = int((height + end_height - textsize[1]*2) / 2)
    cv2.putText(img, text[0:int(len(text)/2)], (textX, textY), font, 1.5 ,(143, 33, 217), 2)
    textY = int((height + end_height + textsize[1]*2) / 2)
    cv2.putText(img, text[int(len(text)/2):], (textX, textY), font, 1.5 ,(143, 33, 217), 2)


textsize = cv2.getTextSize("I USE ARCH BTW", cv2.FONT_HERSHEY_DUPLEX, 1, 2)[0]
cv2.putText(img, "I USE ARCH BTW", (int((width - textsize[0]) / 2), textsize[1]+100), cv2.FONT_HERSHEY_DUPLEX, 1, (230,172,0), 2)
tmp = textsize[1]+40
textsize = cv2.getTextSize("Yup and I wrote the lock screen myself", cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 1)[0]
cv2.putText(img, "Yup and I wrote the lock screen myself", (int((width - textsize[0]) / 2), textsize[1]+tmp), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (230,172,0), 1)

cv2.imwrite('/home/noward/Scripts/python/cv/lock_screen/lock.png',img)
system('i3lock --insidevercolor=0000a000 --insidewrongcolor=ff8000bf --insidecolor=ffffff00 --ringvercolor=0020ffff --ringwrongcolor=4040ffff --ringcolor=404090ff --linecolor=aaaaaaff --keyhlcolor=30ccccff --bshlcolor=ff8000ff --timecolor=404090ff --datecolor=404090ff -mekt -i /home/noward/Scripts/python/cv/lock_screen/lock.png')
