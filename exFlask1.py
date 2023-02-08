# -*- coding: utf-8 -*-
"""
Created on Mon May 16 17:11:35 2022

@author: leleu
"""

from flask import *
from fenetrelumieres import FenetreLumieres
import json
import html
import os
# Create the application instance
app = Flask(__name__, template_folder="templates/")


 
# Create a URL route in our application for "/"
@app.route('/')
def home():
         
    with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json', 'r') as myfile:
        data = myfile.read()
    return render_template('index.html', jsonfile=data)


@app.route('/', methods = ["GET","POST"])
def update():
    value = request.form
    var = 0
    
            
    if value["lampe1"] == "valuelampe1a":
        with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
            data = f.read()
            js = json.loads(data)
            js.update({"lampe1":1})
        with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json', 'w') as mon_fichier:
            json.dump(js, mon_fichier)
            
            
            
    if value["lampe1"] == "valuelampe1e":
        with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
            data = f.read()
            js = json.loads(data)
            js.update({"lampe1":0})
        with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json', 'w') as mon_fichier:
            json.dump(js, mon_fichier)



    if value["lampe2"] == "valuelampe2a":
        with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
            data = f.read()
            js = json.loads(data)
            js.update({"lampe2":1})
        with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json', 'w') as mon_fichier:
            json.dump(js, mon_fichier)  
        
        
        
    if value["lampe2"] == "valuelampe2e":
        with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json') as f: 
            data = f.read()
            js = json.loads(data)
            js.update({"lampe2":0}) 
        with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json', 'w') as mon_fichier:
            json.dump(js, mon_fichier) 
            
            
            
    with open('/home/pi/Desktop/MESPI/MESPI-main/templates/exJson1.json', 'r') as myfile:
        data = myfile.read()
    return render_template('index.html', jsonfile=data)
    
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='192.168.248.110' , port=5000, debug=False)


    
    
    
    