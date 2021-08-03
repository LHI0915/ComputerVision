import cv2
import numpy as np

def main():

    #명도,switch 변수 선언
    hsv = 0
    savehsv=0
    cont = 0
    switch = 0
    check_c=0
    check_s=0
    img_hsv=0
    img_save=0
    save_hsv_result=0
    cnt=0
    save_cont=0 
    def nothing(x):
        pass


    def callback_contrast(x):
        #명도 저장
        nonlocal cont
        nonlocal hsv #들어올 때 완전 처음의 이미지
        nonlocal check_c,cnt
        check_c=1
        cnt+=1
        cont = x-100
        h,s,v = cv2.split(hsv)
        for i in range(0,v.shape[0]):
            for j in range(0,v.shape[1]):
                if(v[i][j]+cont>=255):
                    v[i][j]=255
                elif(v[i][j]+cont<=0):
                    v[i][j]=0
                else:
                    v[i][j] = v[i][j]+cont
        
        hsv = cv2.merge([h,s,v])
        #값 변화에 따른 이미지 변환
        img_remake()ㄴ

    def callback_switch(x):
        #switch값 저장
        nonlocal switch
        switch = x
        #값 변화에 따른 이미지 변환
        switch_move(switch)
        img_remake()
    
    def callback_saturation(x):
        nonlocal cont
        nonlocal hsv
        nonlocal check_s,cnt
        cnt+=1
        check_s=1
        cont = x - 100
        h,s,v = cv2.split(hsv)
        for i in range(0,s.shape[0]):
            for j in range(0,s.shape[1]):
                if(s[i][j]+cont>=255):
                    s[i][j]=255
                elif(s[i][j]+cont<=0):
                    s[i][j]=0
                else:
                    s[i][j] = s[i][j]+cont
               
                
        #test = cv2.bitwise_and(hsv,hsv,mask = s)
        hsv = cv2.merge([h,s,v])
        print(hsv)
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print(s)
        print('-------------------------')
        img_remake()
    def switch_move(switch):
        nonlocal cnt
        nonlocal save_hsv_result,hsv
        switch_hsv = cv2.cvtColor(save_hsv_result,cv2.COLOR_BGR2HSV)
        if((1-switch==0 and cnt!=0) or (1-switch==1 and cnt!=0)):
             hsv = switch_hsv
           
        
    def img_remake():
        nonlocal switch
        nonlocal cont
        nonlocal img
        nonlocal savehsv
        nonlocal hsv,img_hsv,img_save,save_hsv_result,cnt,save_cont
        nonlocal check_s, check_c
        # 2. 명도를 움직임 바뀐 명도와 바뀌지 않은 채도(hsv)
        
        if(cnt>=2):
            img_hsv = cv2.cvtColor(save_hsv_result, cv2.COLOR_BGR2HSV)
            print('img_hsv의 값이에요')
            print(img_hsv)
            h_r,s_r,v_r = cv2.split(img_hsv) #채도가 바뀐 것이 들어가 있음
            h,s,v = cv2.split(hsv)
            if(check_c==1):
                for i in range(0,s.shape[0]):
                    for j in range(0,s.shape[1]):
                        s[i][j] = s_r[i][j]
                print('명도가 움직여서 들어왔어')
            elif(check_s==1):
                for i in range(0,v.shape[0]):
                    for j in range(0,v.shape[1]):
                        v[i][j] = v_r[i][j]
                print('채도가 움직여서 들어왔어')
            hsv = cv2.merge([h,s,v])
            img_hsv = cv2.merge([h_r,s_r,v_r])
            print('if문 안의 hsv')
            print(hsv)
            print('%%%%%%%%%%%%%%%%%%%%%%')
        
        img_result = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
        img_result = img_result.astype('float64')
        img_save = img_result.copy() #img_save 는 RGB
       
        # 명도조절 ~
        #선형     # pix * (1+a)^cont

        if switch == 0:
            for i in range(0,img_save.shape[0]):
                for j in range(0,img_save.shape[1]):
                    for k in range(1,3):
                        if(img_save[i][j][k]>=255):
                            img_save[i][j][k]=255
                        elif(img_save[i][j][k]<=0):
                            img_save[i][j][k]=0
                        else:
                            if cont > 0: #x-100 = 100 x-100 = 40
                                img_save[i][j][k] = img_result[i][j][k] + (20.0+ float(1.0 + 1.0 / 128.0) ** cont)
                            elif cont < 0:
                                img_save[i][j][k] = img_result[i][j][k] + (20.0+ float(1.0 - 1.0 / 128.0) ** -cont)   
                                
        #s형     # pix * (1+a)
        else:
            for i in range(0,img_save.shape[0]):
                for j in range(0,img_save.shape[1]):
                    for k in range(0,3):
                        if(img_save[i][j][k]>=255):
                            img_save[i][j][k]=255
                        elif(img_save[i][j][k]<=0):
                            img_save[i][j][k]=0
                        else:
                            img_save[i][j][k] = img_result[i][j][k] + (2.0+ float(1.0 + cont / 128.0)) 
            
        # ~ 명도조절
        
        #이미지 예외처리 ~
        
        np.clip(img_save,0,255,img_save)
        #~ 이미지 예외처리
        img_save = img_save.astype('uint8')
        #이미지 출력
        print('img_ed의 값이에요 ')
        print(img_save)
        cv2.imshow('image', img_save)
        #hsv_result는 전 이미지
        if(check_s==1 or check_c==1 ):    
            save_hsv_result = img_save.copy() #hsv_result는 RGB 저장
        hsv = savehsv #처음 img hsv로 돌아감(초기화)
        check_s=0
        check_c=0

    #이미지 읽기
    img = cv2.imread("/Users/yount/Desktop/dataset/4.1.01.tiff")
    img_ed = cv2.cvtColor(img,1)
    img_ed = img_ed.astype('float64')
    #print(img_ed)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #원본이미지
    savehsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v=cv2.split(hsv)
    
    print('----------------------')
    print(s)
    print('----------------------')
    print('@@@@@@@@@@@@@@@@@@@@@@')
    print(v)
    print('@@@@@@@@@@@@@@@@@@@@@@')
    # print(hsv)
    #print('%%%%%%%%%%%%%%%%%%%%%%')
    
    cv2.namedWindow('image')
    cv2.createTrackbar('Contrast', 'image', 100, 200, callback_contrast)b
    cv2.createTrackbar('Saturation', 'image', 100, 200, callback_saturation)
    cv2.createTrackbar('S or LINE', 'image', 1, 1, callback_switch)
    #이미지 출력
    cv2.imshow('image', img_ed.astype('uint8'))
    #esc입력 시 종료
    if cv2.waitKey(0) & 0xFF == 27:
    #윈도우 종료
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()