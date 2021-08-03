import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    path = "barbara_025_noisy_comp.png"
    img = cv2.imread(path, 1)
    
    h,w,c = img.shape
    noise_img = img[0:h, 0:int(w/2)]
    origin_img = img[0:h, int(w/2):w+1]
    
    cv2.imshow("img", img)
    cv2.waitKey(0)

    x = (int)(input('x&y :'))
    y = x
    
    while(True):
        mode = input("mode입력: ")
        if mode == '0': #평균값 블러
            blur = cv2.blur(noise_img, (x,y))
            cv2.imshow("Blur", blur)
        elif mode == '1': #가우시안 블러
            blur = cv2.GaussianBlur(noise_img, (x,y), 0)
            cv2.imshow("GaussianBlur", blur)
        elif mode == '2': #중앙값 블러
            blur = cv2.medianBlur(noise_img, x)
            cv2.imshow("MedianBlur", blur)
            
        else:
            break
        
        err_h, err_w, err_c = origin_img.shape
        img_float = origin_img.astype(np.float)
        blur_float = blur.astype(np.float)
        pixel = err_h*err_w*err_c
        err_mse = abs(img_float - blur_float)**2
        err_avg = abs(img_float - blur_float)
        
        mse = np.sum(err_mse)/pixel
        avg = np.sum(err_avg)/pixel
        
        print("mse: %.2f" %mse)
        print("avg: %.2f" %avg)
        cv2.waitKey(0)
        
        k = cv2.waitKey(1) & 0XFF
        if k == 27:
            break
        
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    main()