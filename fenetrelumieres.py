# -*- coding: utf-8 -*-
"""
Created on Mon May 16 14:44:45 2022

@author: leleu
"""

import dbm

import sys
import threading
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication, QMainWindow, QWidget ,QLabel,QRadioButton,
                             QCheckBox)

from PyQt5.QtGui import QPixmap , QIcon
import asyncio
from qtwidgets  import AnimatedToggle
import RPi.GPIO as GPIO
import time

from PyQt5 import QtCore 
import json
import urllib.request
from flask import *

class FenetreLumieres(QWidget) :
    

    def __init__(self , faccueil):
        super().__init__()
        self.faccueil = faccueil
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(12,GPIO.OUT)
        
          
        self.resistorPin = 13
        self.setStyleSheet("background-color: rgb(255,255,255);")
        
        self.labellampe1 = QLabel(self)
        self.chklampe1 = AnimatedToggle(
            checked_color="#62aac3",
            pulse_checked_color="#44FFB000"
        )

        self.retour = QPushButton("Retour⬆")
        self.retour.setStyleSheet("background-color: #62aac3 ; border-style: outset ; border-width: 0 px; border-radius: 5px ; color : white ; padding: 4px")
        self.retour.adjustSize()
        self.vide = QLabel()
        
        
        self.labellampe2 = QLabel(self)
        self.chklampe2 = AnimatedToggle(
            checked_color="#62aac3",
            pulse_checked_color="#44FFB000"
        )
        
        self.label = QLabel(self)
        self.pixmap = QPixmap('photolumieres.png')
        self.label.setPixmap(self.pixmap)     
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        
        self.labelauto = QLabel("Automatisation")
        
        self.auto = AnimatedToggle(
            checked_color="#62aac3",
            pulse_checked_color="#44FFB000"
        )
        
        
        self.faccueil = faccueil
        self.init_ui()
        
        self.retour.clicked.connect(self.fermer)
        self.chklampe1.clicked.connect(self.chkl1_click)
        self.chklampe2.clicked.connect(self.chkl2_click)
        self.auto.clicked.connect(self.transi)
        self.loop()
        
        
    def init_ui(self):
        
        
         #BEGIN TEST
        v_lampe = QVBoxLayout()
        v_lampe.addWidget(self.labellampe1)
        
        v_chk = QVBoxLayout()
        v_chk.addWidget(self.chklampe1)
        with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
            data = f.read()
            js = json.loads(data)
            etat1 = js["lampe1"]
            etat2 = js["lampe2"]

        
        self.labellampe1.setText("Lampe 1 = "+str(etat1))
       
        self.labellampe2.setText("Lampe 2 = "+str(etat2))


        if etat1==0:
            self.chklampe1.setChecked(False)
            self.labellampe1.setText("Lampe 1 = "+str(etat1) + " lampe éteinte")
            self.pixmapl1e = QPixmap('photolumiereseteinte.png')
            self.label2.setPixmap(self.pixmapl1e)
            GPIO.output(11,GPIO.LOW)
            
            
            
        else:
            self.chklampe1.setChecked(True)
            self.labellampe1.setText("Lampe 1 = "+str(etat1) + " lampe allumée")
            self.pixmapl1a = QPixmap('photolumieresallumee.png')
            self.label2.setPixmap(self.pixmapl1a)
            GPIO.output(11,GPIO.HIGH)
            
        
        if etat2==0:
             self.chklampe2.setChecked(False) 
             self.labellampe2.setText("Lampe 2 = "+str(etat2) + "lampe éteinte")
             self.pixmapl2e = QPixmap('photolumiereseteinte.png')
             self.label3.setPixmap(self.pixmapl2e)
             GPIO.output(12,GPIO.LOW)
             
             
        else:
             self.chklampe2.setChecked(True) 
             self.labellampe2.setText("Lampe 2 = "+str(etat2) + "lampe allumée")
             self.pixmapl2a = QPixmap('photolumieresallumee.png')
             self.label3.setPixmap(self.pixmapl2a)
             GPIO.output(12,GPIO.HIGH)
             
      
    
        
        #END TEST
        
        #v_photo.addWidget(self.label)
        
        
        v_photo = QVBoxLayout()
        v_photo.addWidget(self.label)

        v_box = QHBoxLayout()
        v_box.addWidget(self.labellampe1)
        v_box.addWidget(self.chklampe1)
        v_box.addWidget(self.label2)
        v_box.addStretch()
        
        v_deux = QHBoxLayout()
        v_deux.addWidget(self.labellampe2)
        v_deux.addWidget(self.chklampe2)
        v_deux.addWidget(self.label3)
        v_deux.addStretch()
        

        auto_box = QHBoxLayout()
        auto_box.addWidget(self.labelauto)
        auto_box.addWidget(self.auto)
        
        retour_box = QHBoxLayout()
        retour_box.addWidget(self.retour)
        retour_box.addWidget(self.vide)
        retour_box.addWidget(self.vide)
        
        h_box = QVBoxLayout()
        h_box.addLayout(v_photo)
        h_box.addLayout(v_box)
        h_box.addLayout(v_deux)
        h_box.addLayout(auto_box)
        h_box.addLayout(retour_box)
        self.setLayout(h_box) 
        
        
        self.setGeometry(600,400,500,200)
        self.setWindowTitle("Majord'home : lumières")
        self.setWindowIcon(QIcon('logo5.png'))
        
        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
    def chkl1_click(self, cbt) :
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(12,GPIO.OUT)
        if self.chklampe1.isChecked() == True:
            self.labellampe1.setText("Lampe 1 = " + "lampe allumée")
            self.pixmapl1a = QPixmap('photolumieresallumee.png')
            self.label2.setPixmap(self.pixmapl1a)
            
            
            
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
                data = f.read()
                js = json.loads(data)
                js.update({"lampe1":1})
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json', 'w') as mon_fichier:
                json.dump(js, mon_fichier)
                
                
                
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
                data = f.read()
                js = json.loads(data)
                etat1 = js["lampe1"]
            if etat1==0:
                GPIO.output(11,GPIO.LOW)
            else:
                GPIO.output(11,GPIO.HIGH)
            if cbt == 2:
                pass
            else :
                self.auto.setChecked(False)
                
#-------------------------------------------------------------------------------
        else : 
            self.labellampe1.setText("Lampe 1 = " + "lampe éteinte")
            self.pixmapl1e = QPixmap('photolumiereseteinte.png')
            self.label2.setPixmap(self.pixmapl1e)
            
            
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
                data = f.read()
                js = json.loads(data)
                js.update({"lampe1":0})
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json', 'w') as mon_fichier:
                json.dump(js, mon_fichier)
                
                
                
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
                data = f.read()
                js = json.loads(data)
                etat1 = js["lampe1"]
            if etat1==0:
                GPIO.output(11,GPIO.LOW)
            else:
                GPIO.output(11,GPIO.HIGH)
              
            
            if cbt == 2:
                pass
            else :
                self.auto.setChecked(False)
            
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
            
            
    def chkl2_click(self, cbt):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(12,GPIO.OUT)
        
        if self.chklampe2.isChecked() == True:
            self.labellampe2.setText("Lampe 2 = " + "lampe allumée")
            self.pixmapl2a = QPixmap('photolumieresallumee.png')
            self.label3.setPixmap(self.pixmapl2a)
            
            
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
                data = f.read()
                js = json.loads(data)
                js.update({"lampe2":1})
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json', 'w') as mon_fichier:
                json.dump(js, mon_fichier)
                
                
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
                data = f.read()
                js = json.loads(data)
                etat2 = js["lampe2"]
            if etat2==0:
                GPIO.output(12,GPIO.LOW)
            else:
                GPIO.output(12,GPIO.HIGH)
            if cbt == 2:
                pass
            else :
                self.auto.setChecked(False)
            if cbt == 2:
                pass
            else :
                self.auto.setChecked(False)
                
#-------------------------------------------------------------------------------               
        else : 
            self.labellampe2.setText("Lampe 2 = " + "lampe éteinte")
            self.pixmapl2e = QPixmap('photolumiereseteinte.png')
            self.label3.setPixmap(self.pixmapl2e)
            
            
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
                data = f.read()
                js = json.loads(data)
                js.update({"lampe2":0})
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json', 'w') as mon_fichier:
                json.dump(js, mon_fichier)
        
            
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
                data = f.read()
                js = json.loads(data)
                etat2 = js["lampe2"]
            if etat2==0:
                GPIO.output(12,GPIO.LOW)
            else:
                GPIO.output(12,GPIO.HIGH)
                
            
            if cbt == 2:
                pass
            else :
                self.auto.setChecked(False)
                
            
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
    def transi(self):
        t = threading.Thread(target=self.recuplum)
        t.start()
    
    
    
    def recuplum(self):
        diff = 0
        lux = 0
        
        if self.auto.isChecked() == True :
            while(1==1):
                
                GPIO.setup(self.resistorPin, GPIO.OUT)
                GPIO.output(self.resistorPin, GPIO.LOW)
                time.sleep(0.1)
                GPIO.setup(self.resistorPin, GPIO.IN)
                currentTime = time.time()
                diff = 0
                
                while(GPIO.input(self.resistorPin) == GPIO.LOW):
                    diff  = time.time() - currentTime
                lux = diff * 1000      
                print(lux)
                time.sleep(1)
                
                
                if lux>300:
                    if self.auto.isChecked() == False :
                        break
                    self.chklampe1.setChecked(True)
                    self.chklampe2.setChecked(True)
                    
                    self.chkl1_click(2)
                    self.chkl2_click(2)
                    
                if lux <100:
                    
                    if self.auto.isChecked() == False :
                        break
                    
                    self.chklampe1.setChecked(False)
                    self.chklampe2.setChecked(False)
                    
                    self.chkl1_click(2)
                    self.chkl2_click(2)
                    
                if self.auto.isChecked() == False :
                    break
    def loop(self):
        t = threading.Thread(target=self.looping)
        t.start()
            
    def looping(self):
        while(1==1):
            time.sleep(2)
            with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
                data = f.read()
                js = json.loads(data)
                etat1 = js["lampe1"]
                etat2 = js["lampe2"]

        
            self.labellampe1.setText("Lampe 1 = "+str(etat1))
           
            self.labellampe2.setText("Lampe 2 = "+str(etat2))


            if etat1==0:
                self.chklampe1.setChecked(False)
                self.labellampe1.setText("Lampe 1 = "+" lampe éteinte")
                self.pixmapl1e = QPixmap('photolumiereseteinte.png')
                self.label2.setPixmap(self.pixmapl1e)
                GPIO.output(11,GPIO.LOW)
                
                
                
            else:
                self.chklampe1.setChecked(True)
                self.labellampe1.setText("Lampe 1 = "+" lampe allumée")
                self.pixmapl1a = QPixmap('photolumieresallumee.png')
                self.label2.setPixmap(self.pixmapl1a)
                GPIO.output(11,GPIO.HIGH)
                
            
            if etat2==0:
                self.chklampe2.setChecked(False) 
                self.labellampe2.setText("Lampe 2 = "+" lampe éteinte")
                self.pixmapl2e = QPixmap('photolumiereseteinte.png')
                self.label3.setPixmap(self.pixmapl2e)
                GPIO.output(12,GPIO.LOW)
                 
                 
            else:
                self.chklampe2.setChecked(True) 
                self.labellampe2.setText("Lampe 2 = "+ " lampe allumée")
                self.pixmapl2a = QPixmap('photolumieresallumee.png')
                self.label3.setPixmap(self.pixmapl2a)
                GPIO.output(12,GPIO.HIGH)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
    def fermer(self):
        self.hide()
        self.faccueil.show()
            
            
