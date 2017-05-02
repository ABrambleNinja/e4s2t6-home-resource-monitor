from papirus import Papirus
from papirus import PapirusText
from papirus import PapirusTextPos
from papirus import PapirusImage
import RPi.GPIO as GPIO
import time
from urllib import urlopen
import json

screen = Papirus()
text = PapirusTextPos()
GPIO.setmode(GPIO.BCM)
chan_list = [21, 16]# add as many channels as you want!#you can tuples instead i.e.: #chan_list = (11, 12)
GPIO.setup(chan_list, GPIO.IN)
currentState = True

def print1():
    text.AddText("Widnow is closed" , 10, 10, Id = "Closed")

def door():
    # pin is 21
    global currentState
    if (GPIO.input(21) == False and currentState==True):
        text.Clear()
        text.AddText("Window is closed" , 10, 10, Id = "Closed")
        currentState = False
        #we don't do anything
    elif(GPIO.input(21) == True and currentState==False):
        #the door is open if we have reached here,
        #so we should send a value to Adafruit IO.
        text.Clear()
        text.AddText("Window is open" , 10, 10, Id = "Open")
        currentState = True
    time.sleep(.1)
    return currentState

def thermometer():
    #reading = GPIO.input(16)
    #voltage = reading * 5.0
    #voltage /= 1024.0
    #temperatureC = (voltage - 0.5) * 100 #converting from 10 mv per degree wit 500 mV offset
    #now convert to Fahrenheit
    #temperatureF = (temperatureC * 9.0 / 5.0) + 32.0
    #text.AddText((str)(temperatureF) , 10, 10, Id = "Temp")
    #text.AddText("degrees F" , 10, 10, Id = "Label")
    apikey= '06e1dbcfafa9653b'
    url="http://api.wunderground.com/api/"+apikey+"/conditions/q/USA/CA/Claremont.json"
    meteo=urlopen(url).read()
    meteo = meteo.decode('utf-8')
    weather = json.loads(meteo)
    cur_temp =weather['current_observation']['temperature_string'].split()
    tempOut= cur_temp[0]
    text.AddText(tempOut , 10, 10, Id = "Label")
