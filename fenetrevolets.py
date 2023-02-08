import dbm

import sys
import threading
from PyQt5.QtWidgets import *

from PyQt5.QtGui import *
import asyncio
from qtwidgets  import AnimatedToggle
import RPi.GPIO as GPIO
import time

from PyQt5 import QtCore 
import json
import urllib.request
from flask import *

class FenetreVolets(QWidget) :
    

    def __init__(self , faccueil):
        super().__init__()
        global hauteur
        hauteur = 2
        global base
        base = 2
        
        
        
        
        self.faccueil = faccueil
        
        self.setStyleSheet("background-color: rgb(255,255,255);")
        
        self.retour = QPushButton("Retour⬆")
        self.retour.setStyleSheet("background-color: #62aac3 ; border-style: outset ; border-width: 0 px; border-radius: 5px ; color : white ; padding: 4px")
        
        self.label = QLabel(self)
        
        self.pixmap = QPixmap('photovolet.png')
        self.smaller_pixmap = self.pixmap.scaled(400, 400)
        self.label.setPixmap(self.smaller_pixmap)     
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.vide = QLabel()
        
        self.monter = QPushButton("⬆Monter⬆")
        self.monter.setFont(QFont('Arial',20))
        self.monter.setStyleSheet("background-color: #62aac3 ; border-style: outset ; border-width: 0 px; border-radius: 5px;  color : white ; padding: 4px")
    
        self.stop = QPushButton("⏸Stop⏸")
        self.stop.setFont(QFont('Arial',10))
        self.stop.setStyleSheet("background-color: #62aac3 ; border-style: outset ; border-width: 0 px; border-radius: 5px;  color : white ; padding: 4px")
      
        self.descendre =  QPushButton("⬇Descendre⬇")
        self.descendre.setFont(QFont('Arial',18))
        self.descendre.setStyleSheet("background-color: #62aac3 ; border-style: outset ; border-width: 0 px; border-radius: 5px;  color : white ; padding: 4px")
      
        
        self.init_ui()
        
        self.retour.clicked.connect(self.fermer)
        
        self.monter.clicked.connect(self.transiopen)
        self.descendre.clicked.connect(self.transiclose)
        
        
    def init_ui(self):
            
        v_photo = QVBoxLayout()
        v_photo.addWidget(self.label)
        
        row1 = QHBoxLayout()
        row1.addWidget(self.vide)
        row1.addWidget(self.monter)
        row1.addWidget(self.vide)
        
        row2 = QHBoxLayout()
        row2.addWidget(self.vide)
        row2.addWidget(self.stop)
        row2.addWidget(self.vide)
        
        row3 = QHBoxLayout()
        row3.addWidget(self.vide)
        row3.addWidget(self.descendre)
        row3.addWidget(self.vide)
        
        retour_box = QHBoxLayout()
        retour_box.addWidget(self.retour)
        retour_box.addWidget(self.vide)
        retour_box.addWidget(self.vide)
        
        
        v_box = QVBoxLayout()
        v_box.addLayout(v_photo)
        v_box.addLayout(row1)
        v_box.addLayout(row2)
        v_box.addLayout(row3)
        v_box.addLayout(retour_box)
        
        
        
        
        self.setLayout(v_box)
        
        self.setGeometry(600,400,500,200)
        self.setWindowTitle("Majord'home : volets")
        self.setWindowIcon(QIcon('logo5.png'))
        
        
        

        
        
    def fermer(self):
        self.hide()
        self.faccueil.show()
        
        
    def ouverture(self):
        global base
        global hauteur
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(15,GPIO.OUT)
        self.servo1 = GPIO.PWM(15,50)
        self.servo1.start(0)
        
        self.servo1.ChangeDutyCycle(12)
        time.sleep(1)
        self.servo1.ChangeDutyCycle(0)
        
        self.servo1.stop()
        GPIO.cleanup()    
        print("done")
        
    def transiopen(self):
        t = threading.Thread(target=self.ouverture)
        t.start()
        
    def transiclose(self):
        f = threading.Thread(target=self.fermeture)
        f.start()
        
        
    def fermeture(self):
        global base
        global hauteur
        print("hauteur = ",hauteur)
        var = 0
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(15,GPIO.OUT)
        self.servo1 = GPIO.PWM(15,50)
        self.servo1.start(0)
        
        self.servo1.ChangeDutyCycle(2)
        time.sleep(1)
        
        self.servo1.ChangeDutyCycle(0)
       
        self.servo1.stop()
        GPIO.cleanup()    
        print("done")
        
        
        
        