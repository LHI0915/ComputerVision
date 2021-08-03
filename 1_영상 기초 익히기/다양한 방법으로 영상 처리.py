# -*- coding: utf-8 -*-

"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import cv2

user = input("파일명 : ")
img = cv2.imread(user,1)

img_h = img.shape[0]
img_w = img.shape[1]

cv2.imshow('Original',img)

blue=(255,0,0)
font = cv2.FONT_HERSHEY_SIMPLEX

resize_h = img_h
resize_w = img_w

while(True):
    key=cv2.waitKey(0)
    if  key & 0xFF == ord('r'):
        cv2.destroyAllWindows()
        img = cv2.putText(img,user+' '+str(img_w)+'x'+str(img_h)+' '+str(img.dtype) ,(0, img_w-20),font,0.5,blue)
        cv2.imshow('r',img)
    elif key & 0xFF == ord('g'):
        cv2.destroyAllWindows()
        img = cv2.imread(user,cv2.IMREAD_GRAYSCALE)
        resize_h = img_h
        resize_w = img_w
        cv2.imshow('g',img)
    elif key & 0xFF == ord('c'):
        resize_h = img_h
        resize_w = img_w
        cv2.destroyAllWindows()
        img = cv2.imread(user,cv2.IMREAD_COLOR)
        cv2.imshow('c',img)    
    elif key & 0xFF == ord('f'): #추가구현 flip left&right
        cv2.destroyAllWindows()
        img = np.fliplr(img) 
        cv2.imshow('flip_left&right',img)
    elif key & 0xFF == ord('u'): #추가구현 flip up&down
        cv2.destroyAllWindows()
        img = np.flipud(img) 
        cv2.imshow('flip_up&down',img)
    elif key & 0xFF == ord('s'): #추가구현 사이즈 확대
        cv2.destroyAllWindows()
        resize_h=resize_h*2
        resize_w=resize_w*2
        img = cv2.resize(img, dsize=(int(resize_w), int(resize_h)), interpolation=cv2.INTER_AREA) 
        cv2.imshow('size_up',img)
    elif key & 0xFF == ord('d'): #추가구현 사이즈 축소
        cv2.destroyAllWindows()
        resize_h=resize_h/2
        resize_w=resize_w/2
        img = cv2.resize(img, dsize=(int(resize_w), int(resize_h)), interpolation=cv2.INTER_AREA) 
        cv2.imshow('size_down',img)
    elif key & 0xFF == ord('m'):
        block_w = int(input("가로 블록 수 입력: "))
        block_h = int(input("세로 블록 수 입력: "))
        block_m = input("블록 모드: ")

        half_block_w = int(block_w/2) #받은 크기 /2
        half_block_h = int(block_h/2) #받은 크기 /2

        if(block_m == "mean"): #mean 평균값        
            for i in range(0, resize_h - half_block_h , block_h):
                save_h = block_h+i
                for j in range(0, resize_w - half_block_w , block_w):
                    save_w = block_w+j
                    block_num_r = []
                    block_num_g = []
                    block_num_b = []
                    if(save_h>img_h):
                        save_h = img_h
                    if(save_w>img_w):
                        save_w = img_w
                    for k in range(i,save_h):
                        for l in range(j, save_w):
                            block_num_r.append(img[k][l][0])
                            block_num_g.append(img[k][l][1])
                            block_num_b.append(img[k][l][2])
                    mean_r = int(np.mean(block_num_r))
                    mean_g = int(np.mean(block_num_g))
                    mean_b = int(np.mean(block_num_b))
                    for k in range(i,save_h):
                        for l in range(j, save_w):
                            img[k][l][0] = mean_r
                            img[k][l][1] = mean_g
                            img[k][l][2] = mean_b

        elif(block_m == "median"): #median 중앙값
            for i in range(0, resize_h - half_block_h , block_h):
                save_h = block_h+i
                for j in range(0, resize_w - half_block_w , block_w):
                    save_w = block_w+j
                    block_num_r = []
                    block_num_g = []
                    block_num_b = []
                    if(save_h>img_h):
                        save_h = img_h
                    if(save_w>img_w):
                        save_w = img_w
                    for k in range(i,save_h):
                        for l in range(j, save_w):
                            block_num_r.append(img[k][l][0])
                            block_num_g.append(img[k][l][1])
                            block_num_b.append(img[k][l][2])
                    median_r = int(np.median(block_num_r))
                    median_g = int(np.median(block_num_g))
                    median_b = int(np.median(block_num_b))
                    for k in range(i,save_h):
                        for l in range(j, save_w):
                            img[k][l][0] = median_r
                            img[k][l][1] = median_g
                            img[k][l][2] = median_b
            
        elif(block_m == "center"): #center 중심값
            for i in range(0, resize_h - half_block_h , block_h):
                save_h=block_h+i
                for j in range(0, resize_w - half_block_w , block_w):
                    save_w=block_w+j
                    if(save_h>img_h):
                        save_h = img_h
                    if(save_w>img_w):
                        save_w = img_w
                    center = img[i+half_block_h][j+half_block_w]
                    for k in range(i,save_h):
                        for l in range(j, save_w):
                            img[k][l]=center
        
        width=0
        height=0
        first_W=0
        first_h=0
        save_w=(int)(img_w/block_w)
        save_h=(int)(img_h/block_h)
        if(img_w%block_w!=0): save_w+=1
        if(img_h%block_h!=0): save_h+=1
        for i in range(1,save_w+1):
            first_w=(int)((block_w)/2.0) #14
            first_h=(int)((block_h)/2.0) #14
            for j in range(1,save_h+1):
                width=first_w+((j-1)*(first_w*2))
                height=first_h+((i-1)*(first_h*2))
                img = cv2.putText(img,(str)(i)+','+(str)(j),(width-3,height),font,0.2,blue)
                #print('width:%d height:%d' %(width,height))    
        cv2.destroyAllWindows()
        if(block_m == "center"):
            cv2.imshow('mosaic center',img)
        elif(block_m == "median"):
            cv2.imshow('mosaic median',img)
        elif(block_m == "mean"):
            cv2.imshow('mosaic mean',img)
        else:
            pass
    elif key & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
