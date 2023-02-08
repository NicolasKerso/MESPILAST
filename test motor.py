# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setwarnings(False)
GPIO.setup(15,GPIO.OUT)

servo1 = GPIO.PWM(15,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
servo1.start(1)
time.sleep(1)
servo1.start(12)
time.sleep(1)
servo1.start(1)
time.sleep(1)
servo1.start(12)
time.sleep(1)
# Loop to allow user to set servo angle. Try/finally allows exit
# with execution of servo.stop and GPIO cleanup :)



servo1.stop()
GPIO.cleanup()
print("Goodbye!")

