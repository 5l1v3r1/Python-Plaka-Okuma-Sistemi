# -*- coding: utf-8 -*-
"""
Created on Thu May 17 15:30:28 2018

@author: MertogluE
"""

import csv
import datetime
#from olustur import Olustur



def plakaYaz(plaka):
#    plaka=Olustur().gonder()            #    plaka'yı okuyorum 
    plaka=plaka
    skod = plaka[:2]                    #   plakanın ilk iki karakterini skod(şehir kodu) olarak alıyorum
    
    
    
    now=datetime.datetime.now()         # zaman bilgisini almak için 
    
    
    #   zaman degeeleri
    dakika  = now.minute
    saat    = now.hour
    gun     = now.day
    ay      = now.month
    yıl     = now.year
    
    #   veri değişkeni csv formatına yazılmadan hepsinden oluşan bir string haline getiriyor
    veri=plaka +','+ str(dakika) +','+ str(saat) +','+ str(gun) +','+ str(ay) +','+ str(yıl) +','+ skod
    
    
    liste=[[veri]]
    
    csv.register_dialect('myDialect',
        delimiter = '|',                        # ayıraç türünü belirtmek için
        lineterminator = '\r') 
    
    #   veri csv dosyasına ekleniyor
    with open('gelen.csv', 'a') as csvFile:
        writer = csv.writer(csvFile, dialect='myDialect')
        writer.writerows(liste)
            
    
    csvFile.close()     #   csv doayası kapatılıyor