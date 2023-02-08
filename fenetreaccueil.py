# -*- coding: utf-8 -*-
"""
Created on Thu May  5 15:53:37 2022
@author: LELEU
"""

import dbm
import sys
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication, QMainWindow, QWidget ,QLabel,QRadioButton,
                             QCheckBox)
from PyQt5.QtGui import QPixmap , QIcon
import RPi.GPIO as GPIO
from pirc522 import RFID
import time
from PyQt5 import QtCore 
import threading
from fenetrelumieres import FenetreLumieres
from fenetrevolets import FenetreVolets
import json
import urllib.request

class View(QWidget):
    def __init__(self):
        super().__init__()
        
        GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
        GPIO.setwarnings(False) #On désactive les messages d'alerte
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(12,GPIO.OUT)
        self.rc522 = RFID() #On instancie la lib
        self.flum = FenetreLumieres(self)
        self.fvol = FenetreVolets(self)
        self.bvolets = QPushButton('Menu Volets')
        self.bvolets.setStyleSheet("background-color: #62aac3 ; border-style: outset ; border-width: 0 px; border-radius: 5px;  color : white ; padding: 4px")
        self.blumieres = QPushButton('Menu lumières')
        self.blumieres.setStyleSheet("background-color: #62aac3 ; border-style: outset ; border-width: 0 px; border-radius: 5px ; color : white ; padding: 4px")
        #self.bbeeper = QPushButton('Beeper')
        #self.bbeeper.setStyleSheet("background-color: rgb(94,213,207) ; border-style: outset ; border-width: 0 px; border-radius: 5px;  color : white ; padding: 4px")
        
        
        self.label = QLabel(self)
        self.pixmap = QPixmap('logo5.png')
        self.label.setPixmap(self.pixmap)     
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        #BEGIN TEST

        #END TEST
        
        
         
        self.init_ui1()
        
        self.blumieres.clicked.connect(self.blumieres_click)
        self.bvolets.clicked.connect(self.bvolets_click)
        self.show()
        
    def init_ui1(self):
        
       
        
        
        v_photo = QVBoxLayout()
        
        #BEGIN TEST

        #END TEST
        
        v_photo.addWidget(self.label)

        v_box = QHBoxLayout()
        v_box.addWidget(self.bvolets)
        v_box.addWidget(self.blumieres)
        #v_box.addWidget(self.bbeeper)
        
       
        
        h_box = QVBoxLayout()
        h_box.addLayout(v_photo)
        h_box.addLayout(v_box)
        
        self.setLayout(h_box) 
        
        self.setGeometry(400,400,400,400)
        self.setWindowTitle("Majord'home")
        self.setWindowIcon(QIcon('logo5.png'))
        t = threading.Thread(target=self.badge)
        t.start()
    def blumieres_click(self):
        self.hide()
        self.flum.show()
    
    def bvolets_click(self):
        self.hide()
        self.fvol.show()
    
    def badge(self):
        
        while True :
            self.rc522.wait_for_tag() 
            (error, tag_type) = self.rc522.request() #Quand une puce a été lue, on récupère ses infos

            if not error : #Si on a pas d'erreur
                (error, uid) = self.rc522.anticoll() #On nettoie les possibles collisions, ça arrive si plusieurs cartes passent en même temps

                if not error : #Si on a réussi à nettoyer
                    print('Vous avez passé le badge avec l\'id : {}'.format(uid)) #On affiche l'identifiant unique du badge RFID
                    time.sleep(1)
                    print(uid)
                    if(uid == [233, 77, 90, 211, 45]):
                        GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
                        GPIO.setwarnings(False) #On désactive les messages d'alerte
                        GPIO.setup(11,GPIO.OUT)
                        GPIO.setup(12,GPIO.OUT)
                        GPIO.setup(15,GPIO.OUT)
                        
                        GPIO.output(11,GPIO.HIGH)
                        GPIO.output(12,GPIO.HIGH)
                        
                        self.servo1 = GPIO.PWM(15,50)
                        self.servo1.start(0)
                        duty = 2
                        while duty <= 12:
                            self.servo1.ChangeDutyCycle(duty)
                            time.sleep(0.5 )
                            duty = duty + 5
                        time.sleep(3)
                        self.servo1.ChangeDutyCycle(2)
                        time.sleep(1)
                        self.servo1.ChangeDutyCycle(0)

                        #Clean things up at the end
                        GPIO.output(11,GPIO.LOW)
                        GPIO.output(12,GPIO.LOW)
                        self.servo1.stop()
                        GPIO.cleanup()
                        
                   
 
        
app = QApplication(sys.argv)
interface = View()
sys.exit(app.exec_())
        