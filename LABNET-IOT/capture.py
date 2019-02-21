import numpy as np
import cv2
import time
import os

start = time.time()
dir = '/home/pi/Documents/peixinhos/'
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
fish_cascade = cv2.CascadeClassifier(dir + 'peixinhos.xml')
#cap  = cv2.VideoCapture(dir + 'video.avi')
font = cv2.FONT_HERSHEY_SIMPLEX
fishes = [(1,1,1,1)]


fgbg = cv2.createBackgroundSubtractorMOG2()

elapsed=0.2
fps = 1/elapsed
factor = 1
temp = float(os.popen('vcgencmd measure_temp').readline().replace("temp=","").replace("'C\n",""))

kernel = np.ones((2,2),np.uint8)


while(True):
    end = time.time()
    elapsed = end-start
    fps = (9*fps + 1/elapsed)/10
    start = time.time()
    
    _, img = cap.read()
    img = img[60:470]
    
    if fps < 2 or temp > 70:
        factor *= 1.002
        factor=min(4,factor)
    elif fps > 5:
        factor *= .998
        factor = max(1,factor)
        

    if fps > 3 and factor <3:
        #small = cv2.resize(img, (0,0), fx=1/factor, fy=1/factor)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = fgbg.apply(gray)
        #gauss = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(mask, 50, 255, 0)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for con in contours:
            area = cv2.contourArea(con)
            if 50 < area < 900 and len(con) >=5:
                ellipse = cv2.fitEllipse(con)
                img = cv2.ellipse(img,ellipse,(0,255,0),2)
                #cv2.drawContours(img, [elps],  -1, (0,0,255),3)
        ###fishes = fish_cascade.detectMultiScale(gray)
        ###grey_full = np.mean(gray)
        '''for (x,y,w,h) in fishes:
            grey = np.mean(gray[y:y+h,x:x+w])
            #cv2.putText(img,str(int(grey_full)),(50,50), font, 2,(255,255,0),2)
            if (w < 50/factor and w > 2 and h > 2 and (grey_full/3) < grey < grey_full*2) :
                cv2.circle(img,(int(factor*x+factor/2*w),int(factor*y+factor/2*h)),10,(255,0,0),2)
                #cv2.putText(img,str(int(grey)),(x,int(y+h/2)), font, .5,(255,0,0),1)
            else:
                cv2.circle(img,(int(factor*x+factor/2*w),int(factor*y+factor/2*h)),10,(0,0,255),2)
                #cv2.putText(img,str(int(grey)),(x,y), font, 1,(0,0,255),1)
        '''
    time.sleep(factor/10)
    temp = float(os.popen('vcgencmd measure_temp').readline().replace("temp=","").replace("'C\n",""))
    cv2.putText(img,"fps="+str(int(100*fps)/100)+", factor="+str(int(100*factor)/100)+", temp="+str(temp),(30,50), font, .5,(0,255,255),1)
    #cv2.imshow('contour',thresh)
    #cv2.imshow('gray',gray)

    cv2.imshow('img',img)
    #cv2.imshow('fgmask',thresh)

    #print(lim_inf,lim_sup)
    if temp > 75:
        time.sleep(10)
    k = cv2.waitKey(1) & 0xff
    if k == ord('q'):
        break
        
    end = time.time()
cap.release()
cv2.destroyAllWindows()


    