# -*- coding: utf-8 -*-
import cv2
import numpy as np
#좌상 우상 좌하 우하
save_coor= []
path = "C:\\Users\\gowns\\.spyder-py3\\car.jpg"
windowName = 'image'
img_g = cv2.imread(path,0)
img_original = cv2.imread(path,1)
ret, img_thre = cv2.threshold(img_g, 127, 255, cv2.THRESH_BINARY)
cv2.namedWindow(windowName)
def mouse_callback(event,x,y,flags,param):
    if(event==cv2.EVENT_LBUTTONDOWN):
        cv2.circle(img_thre,(x,y),5,(255,255,255),-1)
        save_coor.append([x,y])
        if(len(save_coor)==4):
            make_img(save_coor)
def make_img(save_coor):
    height, weight = img_original.shape[:2]
    pts1 = np.float32([save_coor[0],save_coor[1],save_coor[2],save_coor[3]])
    pts2 = np.float32([[0,0],[weight,0],[0,height],[weight,height]])   
    perspective = cv2.getPerspectiveTransform(pts1,pts2)
    img_result = cv2.warpPerspective(img_original,perspective,(weight,height))
    cv2.imshow('result',img_result)

cv2.setMouseCallback(windowName,mouse_callback)
while(True):
    cv2.imshow(windowName,img_thre)
    if cv2.waitKey(1) & 0xFF==27:
        break;
cv2.destroyAllWindows()
