# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 13:15:53 2018

@author: mertoglue
"""

import sys

import cv2

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage , QPixmap
from PyQt5.QtWidgets import QDialog, QApplication ,QFileDialog
from PyQt5.uic import loadUi

from Main import Veri


class Plaka(QDialog):
    
    def __init__(self):
        super(Plaka, self).__init__()
        loadUi('untitled.ui',self)

        self.image=None
        self.alan=None
        self.plaka=None
        self.resimSecButon.clicked.connect(self.loadClicked)
        self.plakaBulButon.clicked.connect(self.bulPlaka)

    
    def resimSec(self):
        fname , filter = QFileDialog.getOpenFileName(self,'Open File','C:\\Users\\mertoglue\\AnacondaProjects\\pyQt5\pyqtPlakaBul',"Image Files (*.png *.jpg)")
        return fname


    @pyqtSlot()
    def loadClicked(self):
        fname=self.resimSec()
        if fname :
            self.loadImage(fname)
        else:
            print("hatalı resim")
    

    def loadImage(self,fname):
        self.image=cv2.imread(fname,cv2.IMREAD_GRAYSCALE)
        self.displayImage()


    def displayImage(self):
        qformat=QImage.Format_Indexed8

        if len(self.image.shape)==3:
            if(self.image.shape[2])==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
#        print("/"*50)    
        img=QImage(self.image,self.image.shape[1],self.image.shape[0],self.image.strides[0],qformat)

        img=img.rgbSwapped()
        self.resimAlLabel.setPixmap(QPixmap.fromImage(img))
        self.resimAlLabel.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)


    def displayImagePlate(self):
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


    def bulPlaka(self):
        v=Veri()
        self.alan,self.plaka = v.getVeri()

        self.karakterLabel.setText(self.plaka)
        self.karakterLabel.setReadOnly(True)
        self.karakterLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.displayImagePlate()







app=QApplication(sys.argv)

window=Plaka()
window.setWindowTitle('PyQt ile OpenCV')
window.show()

sys.exit(app.exec_())