#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# ultrasonic_2.py
# Measure distance using an ultrasonic module
# in a loop.
#
# Ultrasonic related posts:
# http://www.raspberrypi-spy.co.uk/tag/ultrasonic/
#
# Author : Matt Hawkins
# Date   : 16/10/2016
# -----------------------

# -----------------------
# Import required Python libraries
# -----------------------
from __future__ import print_function
import time
import RPi.GPIO as GPIO
#from pygame import mixer
import os, random, requests, json
from datetime import datetime, timedelta
import subprocess
# -----------------------
# Define some functions
# -----------------------
def measure():
  # This function measures a distance
  GPIO.output(GPIO_TRIGGER, True)
  # Wait 10us
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()
  
  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()

  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * speedSound)/2

  return distance

def measure_average():
  # This function takes 3 measurements and
  # returns the average.

  distance1=measure()
  time.sleep(0.1)
  distance2=measure()
  time.sleep(0.1)
  distance3=measure()
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance

# -----------------------
# Main Script
# -----------------------

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO    = 24

# Speed of sound in cm/s at temperature
temperature = 20
speedSound = 33100 + (0.6*temperature)

print("Ultrasonic Measurement")
print("Speed of sound is",speedSound/100,"m/s at ",temperature,"deg")

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.5)

# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.
try:
  while True:
    distance = measure_average()
    print(distance)
    if distance > 30 and distance < 120: #about 3 ish feet

    
        #Feeding the seed from Nasa's API... if you want
        """
        now = datetime.today()
        then = now - timedelta(days=30)
        url = "https://api.nasa.gov/DONKI/CME?startDate="+str(then.year)+"-"+str(then.month)+"-"+str(then.day)+"&endDate="+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"&api_key=DEMO_KEY"
        
        responce = requests.get(url)
        if(responce.ok):
            jdata = json.loads(responce.content)
            #solar radiation seed
            if len(jdata)>0:
                stupidCMESeed = int(jdata[0]["cmeAnalyses"][0]["latitude"])+ int(jdata[0]["cmeAnalyses"][0]["longitude"]) * int(jdata[0]["cmeAnalyses"][0]["halfAngle"]) *int(jdata[0]["cmeAnalyses"][0]["speed"])
                random.seed(stupidCMESeed * distance)
            else:
                random.seed( distance)
        else:
            random.seed( distance)
            #print(jdata)

        """
        
        #find a random audio file (will need to redothis to get current folder, dont care to fix this in post)
        file = random.choice(os.listdir("/home/pi/Documents/Tets/Insults"))
        p=subprocess.Popen(["mplayer","/home/pi/Documents/Tets/Insults/"+file],stdout=subprocess.PIPE)

        #waits for audio to finish before continueing
        while p.poll() is None:
            time.sleep(1)
        p.kill()
    time.sleep(1)

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  #p.kill()
  GPIO.cleanup()