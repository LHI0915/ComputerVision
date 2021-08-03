# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math

def gb(image,var,size):
    total = 0.0
    sigma = 0.3*((size-1)*0.5-1)+0.8
    
    mask = np.zeros((2*size+1,2*size+1),np.float32)

    for i in range(-size,size+1):
        for j in range(-size,size+1):
            mask[i+size][j+size] =np.exp(-((i)**2+(j)**2) / (2*sigma*sigma)) / (2*np.pi*sigma*sigma)
            total+=mask[i+size][j+size]
   
    for i in range(-size,size+1):
        for j in range(-size,size+1):
            mask[i+size][j+size]/=total
    '''
    total = 0
    for i in range(-size, size+1):
        for j in range(-size,size+1):
            total+=mask[i+size][j+size]
    print("\n\ntotal은 ", total)
    '''
    
    output = cv2.filter2D(img,-1,mask)

    return output

img = cv2.imread('L1.png',1)
var = (int)(input('variance :'))
size = (int)(input('size :'))

output = gb(img,var,size) 
cv2.imshow("GaussianBlur", output)

cv2.waitKey(0)
cv2.destroyAllWindows()