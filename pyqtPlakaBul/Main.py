# Main.py

import cv2
import os
import sys

import DetectChars
import DetectPlates

from olustur2 import *


# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = True

###################################################################################################

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage , QPixmap
from PyQt5.QtWidgets import QDialog, QApplication ,QFileDialog
from PyQt5.uic import loadUi


class Plaka(QDialog):
    
    def __init__(self):
        super(Plaka, self).__init__()
        loadUi('untitled.ui',self)
        self.resimSecButon.clicked.connect(self.loadClicked)
        self.plakaBulButon.clicked.connect(self.main)

    


    @pyqtSlot()
    def loadClicked(self):
        self.fname , filter = QFileDialog.getOpenFileName(self,'Open File','C:\\Users\\mertoglue\\AnacondaProjects\\Bitirme\\pyqtPlakaBul\\foto',"Image Files (*.png *.jpg)")
                                                                            
        self.image=cv2.imread(self.fname)
        qformat=QImage.Format_Indexed8

        if len(self.image.shape)==3:
            if(self.image.shape[2])==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888   
        img=QImage(self.image,self.image.shape[1],self.image.shape[0],self.image.strides[0],qformat)

        img=img.rgbSwapped()
        self.resimAlLabel.setPixmap(QPixmap.fromImage(img))
        self.resimAlLabel.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.karakterLabel.setText("")      # yeni fotoğraf seçildiğinde önceden olan plakanın sıfırlanması için
        self.plakaLabel.clear()             # yeni fotoğraf seçildiğinde önceden alınan plaka bölgesinin sıfırlanması için
       



###################################################################################################
    def main(self):
    
        blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         # attempt KNN training (True ya da False)
        
    
        if blnKNNTrainingSuccessful == False:                               # if KNN training was not successful
            print ("\n error: KNN traning was not successful \n")             # show error message
            return                                                          # and exit program

        imgOriginalScene  = cv2.imread(self.fname)                 # open image
    
        if imgOriginalScene is None:                            # if image was not read successfully
            print ("\n error: image not read from file \n\n")    # print error message to std out
            os.system("pause")                                  # pause so user can see error message
            return                                              # and exit program
    
        listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           # detect plates (plakaları algıla)
        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates (Plakadaki karakterleri algıla)
        
    
        if len(listOfPossiblePlates) == 0:                           # if no plates were found --> eğer plaka bulunmuyorsa 
            print ("\n no license plates were detected\n")           # inform user no plates were found (hiçbir plaka bulunamadı)
        else:                                                       # else
            listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)
            self.licPlate = listOfPossiblePlates[0]
            

            if len(self.licPlate.strChars) == 0:                     # if no chars were found in the plate
                print ("\nno characters were detected\n\n")     # show message
                return                                          # and exit program
    
            self.drawRedRectangleAroundPlate(imgOriginalScene, self.licPlate)             # draw red rectangle around plate           
#            print ("\n license plate read from image = " + self.licPlate.strChars + "\n")       # write license plate text to std out
            self.writeLicensePlateCharsOnImage(imgOriginalScene, self.licPlate)           # write license plate text on the image

        self.alan = self.licPlate.imgPlate
        self.plaka = self.licPlate.strChars

        self.karakterLabel.setText(self.plaka)
        self.karakterLabel.setReadOnly(True)
        self.karakterLabel.setAlignment(QtCore.Qt.AlignHCenter)

        qformat=QImage.Format_Indexed8
        
        if len(self.alan.shape)==3:
            if(self.alan.shape[2])==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888

        img=QImage(self.alan,self.alan.shape[1],self.alan.shape[0],self.alan.strides[0],qformat)

        img=img.rgbSwapped()
        self.plakaLabel.setPixmap(QPixmap.fromImage(img))
        self.plakaLabel.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        plakaYaz(self.plaka)

        cv2.waitKey(0)					# hold windows open until user presses a key (Kullanıcı bir tuşa basana kadar pencereleri açık tutar)
    

    
    ###################################################################################################
    def drawRedRectangleAroundPlate(self,imgOriginalScene, licPlate):
        p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect 
    
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)         # draw 4 red lines
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
    # end function
    
    ###################################################################################################
    def writeLicensePlateCharsOnImage(self,imgOriginalScene, licPlate):
        ptCenterOfTextAreaX = 0                             # this will be the center of the area the text will be written to
        ptCenterOfTextAreaY = 0
    
        ptLowerLeftTextOriginX = 0                          # this will be the bottom left of the area that the text will be written to
        ptLowerLeftTextOriginY = 0
    
        sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
        plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape 
        
    
        intFontFace = cv2.FONT_HERSHEY_SIMPLEX                      # choose a plain jane font (Yazılan plakanın yazı fontu)
        fltFontScale = float(plateHeight) / 30.0                    # base font scale on height of plate area 
        intFontThickness = int(round(fltFontScale * 2.5))           # base font thickness on font scale (Yazılan plakanın yazı kalınlığı)
    
        textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)        # call getTextSize
        print("-----------------> ",textSize, "-----",baseline)
    
                # unpack roatated rect into center point, width and height, and angle
        ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene
    
        intPlateCenterX = int(intPlateCenterX)              # make sure center is an integer
        intPlateCenterY = int(intPlateCenterY)
    
        ptCenterOfTextAreaX = int(intPlateCenterX)         # the horizontal location of the text area is the same as the plate
    
        if intPlateCenterY < (sceneHeight * 0.75):                                                  # if the license plate is in the upper 3/4 of the image
            ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))      # write the chars in below the plate
        else:                                                                                       # else if the license plate is in the lower 1/4 of the image
            ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))      # write the chars in above the plate
        # end if
    
        textSizeWidth, textSizeHeight = textSize                # unpack text size width and height
    
        ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))           # calculate the lower left origin of the text area
        ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))          # based on the text area center, width, and height
    
                # write the text on the image
        cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_GREEN, intFontThickness)
    # end function

####################################################################################################
class Olustur(object):
    
    def __init__(self):
        self.plaka="34AJE440"

    @staticmethod
    def gonder(plaka):
        return plaka
        

####################################################################################################
if __name__ == "__main__":
    app=QApplication(sys.argv)

    window=Plaka()
    window.setWindowTitle('PyQt ile OpenCV')
    window.show()
    
    sys.exit(app.exec_())


















