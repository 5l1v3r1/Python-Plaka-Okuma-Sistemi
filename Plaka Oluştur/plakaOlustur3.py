# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 09:08:26 2018

@author: mertoglue
"""

import random
import time
import datetime
import csv


for _ in range(500):
    on=random.randrange(1,81)
    
    if on<10:
        on='0'+str(on)
    
    arka=random.randrange(1,1000)
    
    listeHarf = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','T','U','V','Y','Z']
    
    boyutPlakaList = [2,3]
    boyut=random.sample(boyutPlakaList,1)
    boyut=boyut[0]
    
    harf = random.sample(listeHarf,boyut)
    yazi=""
    for i in harf:
        yazi = yazi +i
    
    
    plaka=str(on)+yazi+str(arka)
    
    now=datetime.datetime.now()
    
    dakika  = random.randint(1,60)
    saat    = random.randint(1,24)
    gun     = random.randint(1,31)
    ay      = random.randint(1,12)
    yıl     = random.randint(2015,2018)
    
    csv.register_dialect('myDialect',
    delimiter = '|',                        # ayıraç türünü belirtmek için
    lineterminator = '\r') 



    time.sleep(0.5)
    veri=plaka +','+ str(dakika) +','+ str(saat) +','+ str(gun) +','+ str(ay) +','+ str(yıl) + ','+ str(on)
    
    liste=[[veri]]
    
    with open('gelen.csv', 'a') as csvFile:
        writer = csv.writer(csvFile, dialect='myDialect')
        writer.writerows(liste)
        

csvFile.close()



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
