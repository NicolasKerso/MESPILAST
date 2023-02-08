import RPi.GPIO as GPIO
import time

import json
import urllib

from flask import *


# Create the application instance
app = Flask(__name__, template_folder="templates/")

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
        

    :return:        the rendered template 'home.html'
    """
    #url = "http://172.16.115.65:5000/lampe"
    #urllib.request.urlopen(url)
    #return render_template('exJson1.json')
    with open('templates/exJson1.json') as f:
        data = json.load(f)
        #for d in data:
        #    print(d)
    return render_template('index.html', jsonfile=json.dumps(data))

@app.route('/lampe/<n>')
def lampe(n):
    nlamp=int(n)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(nlamp,GPIO.OUT)
    GPIO.output(18,GPIO.HIGH)
    flag=1
    if flag==1 :
        print ("LED on")
        lampe1 = {"lampe1" : "1"}
    with open('exJson1.json', 'w') as mon_fichier:
        json.dump(lampe1, mon_fichier)
       
    time.sleep(1)
    flag = 0
    if flag==0 :
        print ("LED off")
        valJson["lampe1"] = 0
    GPIO.output(18,GPIO.LOW)
    time.sleep(1)
    
    url = "http://192.168.127.49:5000/"
    data = urllib.request.urlopen(url).read().decode()
    valJson = json.loads(data)
    etat1 = valJson["lampe1"]
    etat2 = valJson["lampe2"]
    print(data)
    print(valJson["lampe1"])
    print(valJson["lampe2"])
    
    
    return redirect('/')




# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    
    app.run(host = "192.168.127.49", debug = True, port="5000")
    
        
    

    
    