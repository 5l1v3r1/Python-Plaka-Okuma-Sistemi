# -*- coding: utf-8 -*-
"""
Created on Fri May 18 14:23:29 2018

@author: MertogluE
"""
import pandas as pd


class Analiz(object):
    
    #   Analiz sınıfının yapıcı fonksiyonu
    def __init__(self,plaka):
        self.plaka=plaka


    
    ####################################################################################################
    
    #   Veri fonksiyonu parametre olarak aldığı yolu ve sıra parametrelerini alıp bize istenen sonucu veriyor
    def veri(self,dosya,sıra):
#        yol='C:\\Users\\mertoglue\\AnacondaProjects\\Bitirme\\CSV\\'+dosya
        yol='C:\\Users\\mertoglue\\AnacondaProjects\\Bitirme\\CSV\\' +dosya
            
        
        veri = pd.read_csv(yol, encoding = "ISO-8859-1" ,sep=',')   # pandas ile dosya okunup veriler alınıyor ve okunan veriler, veri değişkenine atanıyor
        
        filtre=veri['plaka'].str.contains(self.plaka)               # olan değeri/degerleri True dönderiyor
        
        istenen=veri[filtre].values[-1]                             # True olan degerlerden sonuncusunu veriyor
        
        return istenen[sıra]                                        # istenen değişkeninin sıra. sütununu dönderir.

    
    ####################################################################################################
    
    #   Dakika hesaplanması için Gelen araç bilgisinin alınması
    def getirDakikaGelen(self):
        istenen = self.veri('gelen.csv',1)
        return istenen
    
     #   Dakika hesaplanması için Giden araç bilgisinin alınması
    def getirDakikaGiden(self):
        istenen = self.veri('giden.csv',1)
        return istenen
    
    ####################################################################################################
    
    
    #   Saat hesaplanması için Gelen araç bilgisinin alınması
    def getirSaatGelen(self):
        istenen = self.veri('gelen.csv',2)
        return istenen
    
    
    #   Saat hesaplanması için Giden araç bilgisinin alınması
    def getirSaatGiden(self):
        istenen = self.veri('giden.csv',2)
        return istenen
    
    ####################################################################################################
    
    #   Gun hesaplanması için Gelen araç bilgisinin alınması
    def getirGunGelen(self):
        istenen = self.veri('gelen.csv',3)
        return istenen
    
    
    #   Gun hesaplanması için Giden araç bilgisinin alınması
    def getirGunGiden(self):
        istenen = self.veri('giden.csv',3)
        return istenen
    
    
    ####################################################################################################
    
    #   Ay hesaplanması için Gelen araç bilgisinin alınması
    def getirAyGelen(self):
        istenen = self.veri('gelen.csv',4)
        return istenen
    
    
    #   Ay hesaplanması için Giden araç bilgisinin alınması
    def getirAyGiden(self):
        istenen = self.veri('giden.csv',4)
        return istenen
    
    
    ####################################################################################################
    
    #   Yıl hesaplanması için Gelen araç bilgisinin alınması
    def getirYılGelen(self):
        istenen = self.veri('gelen.csv',5)
        return istenen
    
    
    #   Yıl hesaplanması için Giden araç bilgisinin alınması
    def getirYılGiden(self):
        istenen = self.veri('giden.csv',5)
        return istenen
    
    ####################################################################################################
    
    def bul(self):
        sonuc = self.getirGiden()-self.getirGelen()
        return [sonuc]
    
    # hesapla fonksiyonu bir aracın giriş yaptıktan çıkış yapana kadarki zaman bilgisini ölçüyor
    def hesapla(self):
        dakika  =  self.getirDakikaGiden()  -   self.getirDakikaGelen()
        saat    =  self.getirSaatGiden()    -   self.getirSaatGelen()
        gun     =  self.getirGunGiden()     -   self.getirGunGelen()
        ay      =  self.getirAyGiden()      -   self.getirAyGelen()
        yıl     =  self.getirYılGiden()     -   self.getirYılGelen()
        
        return [dakika ,saat ,gun, ay, yıl]
        


####################################################################################################
        
    
#   main fonksiyonu
def main():
    aa=Analiz('34AJE440')
    print (aa.hesapla()[-1],"yıl", aa.hesapla()[3] ,"ay",aa.hesapla()[2] ,"gun",aa.hesapla()[1] ,"saat",aa.hesapla()[0] ,"dakika", "KALDI")
    
            
    
    #aa=Analiz('ersin')
    #print(aa.bul()[0])
    #print (aa.getirGelen())
    #print (aa.getirGiden())

if __name__== "__main__":
  main()

























