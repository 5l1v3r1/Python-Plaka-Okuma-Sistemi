# -*- coding: utf-8 -*-
"""
Created on Mon May 14 11:33:18 2018

@author: MertogluE
"""

import numpy as np
import cv2
import time
import glob
import os

class Camera:
    

    path = "."
    
    def __init__(self, camera_id, img_path):
        print("Camera Constructor")
        self.cap = cv2.VideoCapture(camera_id) 
        self.path = img_path + "/" 
        
        
    def __del__(self):
        print("Camera destructor")
        self.cap.release()
        cv2.destroyAllWindows()
        
       
    def is_opened(self):
        return self.cap.isOpened()
    
    
    def read_frame(self):
        
        ret, frame = self.cap.read() #read a frame  
            
        if ret==False:
            print("No Camera found")   
        
        return frame
          
            
    def save_to_file(self,filename):
        
#        print(self.path+filename)
        cv2.imwrite(self.path+filename,frame)
        
        



class Gonder(object):
    def __init__(self):
        self.resim=""
        
    def gond(self):
        return self.resim
    
gg=Gonder()



fotodir = os.path.dirname(os.path.abspath(__file__))
fotodir = fotodir+"/static"

sayac=0

included_extensions = ['jpg','png']

video='araba.mp4'

#frame = ""

cam = Camera(video,fotodir)

while cam.is_opened():
    
    frame = cam.read_frame()
    
    cv2.imshow('Frame',frame)
    
    timefloat = time.time()
    timestr = str(timefloat)
    
    cam.save_to_file(timestr+".jpg")
    time.sleep(0.1)

    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    
    
    
del cam

