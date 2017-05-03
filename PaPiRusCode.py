#!/usr/bin/env python

from papirus import Papirus
from papirus import PapirusText
from papirus import PapirusTextPos
from papirus import PapirusImage
import RPi.GPIO as GPIO
import time
from urllib import urlopen
import json
import math
import thread

screen = Papirus()
text = PapirusTextPos()

userMonthGallons= 2250.000
avgMonthGallons=1500.000
lastMonthGallons = 2500.000
userMonthElectricBtu= 3000000.000
avgMonthEletricBtu=2650000.000
lastMonthElectricBtu = 3100000.000
userMonthGasBtu=5000000.000
avgMonthGasBtu=4266666.000
lastMonthGasBtu = 5100000.000
waterScore = 0
electricScore = 0
gasScore = 0

currentTempOut = 0

GPIO.setmode(GPIO.BCM)
chan_list = [21, 16,26,20]
GPIO.setup(chan_list, GPIO.IN)
currentState = True

import os
import sys
import string
from papirus import Papirus
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep
import RPi.GPIO as GPIO


# Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    execfile('/etc/default/epd-fuse')
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

# Running as root only needed for older Raspbians without /dev/gpiomem
if not (os.path.exists('/dev/gpiomem') and os.access('/dev/gpiomem', os.R_OK | os.W_OK)):
    user = os.getuid()
    if user != 0:
        print("Please run script as root")
        sys.exit()

# Command line usage
# papirus-buttons

hatdir = '/proc/device-tree/hat'

WHITE = 1
BLACK = 0
SIZE = 27
SW2 = 26
SW3 = 20
AC = True
text.AddText("Welcome. Press the left button to move backwards and the right button to move forwards to begin", Id = "Main")

def checkAC():
    global AC
    AC = True


def windowInfoDisplay():
    textA = ""
    if math.fabs(tempInside()-currentTempOut)<2:
        if AC:
            textA = "Your AC is on when it can be turned off because the temperature inside (" + (str)(tempInside()) + ") and ouside (" + (str)(currentTempOut) +") are the same"
        else:
            if not door():
                textA = "Your window is closed when the temperature inside (" + (str)(tempInside()) + ") and ouside (" + (str)(currentTempOut) +") are the same. You can open your window"
    else:
        if AC:
            if door():
                textA = "Your AC is on when the window is open. Please close the window. The temperature inside is " + (str)(tempInside()) + " and ouside is " + (str)(currentTempOut) +"."
    if textA == "":
        textA = "You're monitoring your AC usage well. Keep up the good work! The temperature inside is " + (str)(tempInside()) + " and ouside is " + (str)(currentTempOut) +"."
    return textA

def door():
    # pin is 21
    global currentState
    if (GPIO.input(21) == False and currentState==True):
        currentState = False
        #we don't do anything
    elif(GPIO.input(21) == True and currentState==False):
        #the door is open if we have reached here,
        #so we should send a value to Adafruit IO.
        currentState = True
    time.sleep(.1)
    return currentState

def tempOutside():
    global currentTempOut
    apikey= '06e1dbcfafa9653b'
    url="http://api.wunderground.com/api/"+apikey+"/conditions/q/USA/CA/Claremont.json"
    meteo=urlopen(url).read()
    meteo = meteo.decode('utf-8')
    weather = json.loads(meteo)
    cur_temp =weather['current_observation']['temperature_string'].split()
    currentTempOut = (float)(cur_temp[0])
    sleep(60*3)

thread.start_new_thread(tempOutside, ())

def tempInside():
    #reading = GPIO.input(16)
    #voltage = reading * 5.0
    #voltage /= 1024.0
    #temperatureC = (voltage - 0.5) * 100 #converting from 10 mv per degree wit 500 mV offset
    #now convert to Fahrenheit
    #temperatureF = (temperatureC * 9.0 / 5.0) + 32.0
    #text.AddText((str)(temperatureF) , 10, 10, Id = "Temp")
    #text.AddText("degrees F" , 10, 10, Id = "Label")
    #return (float)(temperatureF)
    return 70.0 #Value will be generated by the nest

def first():
    global userMonthGallons
    textA = ""
    textA = "Your monthly water usage is " + str(userMonthGallons) + " gallons"
    return wrap(textA)

def second():
    global userMonthGallons
    global lastMonthGallons
    global waterScore
    textA = ""
    if userMonthGallons > lastMonthGallons:
        textA = "Over last month's water usage by " + (str)(round(abs((lastMonthGallons-userMonthGallons)/lastMonthGallons)*100,2)) + " pecent"
        waterScore -= 1
    elif userMonthGallons<lastMonthGallons:
        textA = "Under last month's water usage by " + (str)(round(abs((lastMonthGallons-userMonthGallons)/lastMonthGallons)*100,2)) + " percent"
        waterScore += 1
    else:
        textA = "Same amount as last month's water usage"
    return wrap(textA)

def third():
    global userMonthGallons
    global avgMonthGallons
    global waterScore
    textA = ""
    if userMonthGallons > avgMonthGallons:
        textA = "Over the average water usage by "+ (str)(round(abs((userMonthGallons-avgMonthGallons)/avgMonthGallons)*100,2)) + " percent"
        waterScore -= 1
    elif userMonthGallons < avgMonthGallons:
        textA = "Under the average water usage by " + (str)(round(abs((userMonthGallons-avgMonthGallons)/avgMonthGallons)*100,2)) + " percent"
        waterScore += 1
    else:
        textA = "Same amount as average water usage"
    return wrap(textA)


def fourth():
    global userMonthElectricBtu
    textA = ""
    textA = "Your monthly electric usage is " + (str)(userMonthElectricBtu) + " electric British thermal units"
    return wrap(textA)

def fifth():
    global userMonthElectricBtu
    global lastMonthElectricBtu
    global electricScore
    textA = ""
    if userMonthElectricBtu > lastMonthElectricBtu:
        textA = "Over last month's electric usage by "+ (str)(round(abs((lastMonthElectricBtu-userMonthElectricBtu)/lastMonthElectricBtu)*100,2)) + " pecent"
    elif userMonthElectricBtu<lastMonthElectricBtu:
        textA = "Under last month's electric usage by "+ (str)(round(abs((lastMonthElectricBtu-userMonthElectricBtu)/lastMonthElectricBtu)*100,2)) + " percent"
        electricScore += 1
    else:
        textA = "Same electricty usage as last month"
    return wrap(textA)

def sixth():
    global userMonthElectricBtu
    global avgMonthEletricBtu
    global electricScore
    textA = ""
    if userMonthElectricBtu > avgMonthEletricBtu:
        textA = "Over the average electric usage by " + (str)(round(abs((userMonthElectricBtu-avgMonthEletricBtu)/avgMonthEletricBtu)*100,2)) + " percent"
        electricScore -= 1
    elif userMonthElectricBtu < avgMonthEletricBtu:
        textA = "Under the average electric usage by "+ (str)(round(abs((userMonthElectricBtu-avgMonthEletricBtu)/avgMonthEletricBtu)*100,2)) + " percent"
        electricScore += 1
    else:
        textA = "Same electrvity usage as the average"
    return wrap(textA)

def seventh():
    global userMonthGasBtu
    textA = ""
    textA = "Your monthly gas usage is " + str(userMonthGasBtu) + " gas British thermal units"
    return wrap(textA)

def eighth():
    global userMonthGasBtu
    global lastMonthGasBtu
    global gasScore
    textA = ""
    if userMonthGasBtu > lastMonthGasBtu:
        textA = "Over last month's gas usage by " + (str)(round(abs((lastMonthGasBtu-userMonthGasBtu)/lastMonthGasBtu)*100,2)) + " pecent"
        gasScore -= 1
    elif userMonthGasBtu<lastMonthGasBtu:
        textA = "Under last month's gas usage by " + (str)(round(abs((lastMonthGasBtu-userMonthGasBtu)/lastMonthGasBtu)*100,2)) + " percent"
        gasScore += 1
    else:
        textA = "Same gas usage as last month"
    return wrap(textA)

def ninth():
    global userMonthGasBtu
    global avgMonthGasBtu
    global gasScore
    textA = ""
    if userMonthGasBtu > avgMonthGasBtu:
        textA = "Over the average gas usage by " + (str)(round(abs((userMonthGasBtu-avgMonthGasBtu)/avgMonthGasBtu)*100,2)) + " percent"
        gasScore -= 1
    elif userMonthGasBtu < avgMonthGasBtu:
        textA = "Under the average gas usage by" + (str)(round(abs((userMonthGasBtu-avgMonthGasBtu)/avgMonthGasBtu)*100,2)) + "percent"
        gasScore += 1
    else:
        textA = "Same amount as average gas usage"
    return wrap(textA)

def tenth():
    global waterScore
    global electricScore
    global gasScore
    return genSuggestions(waterScore, electricScore,gasScore)

def eleventh():
    return windowInfoDisplay()

def genSuggestions(water, electricity, gas):
    displayBuffer = ""
    if water > 0:
        displayBuffer += "Youre doing great on water, keep it up!" + "\n"
    elif water == 0:
        displayBuffer += "Youre doing ok on water... Consider taking shorter showers, turning off the faucet when brushing, etc." + "\n"
    elif water < 0:
        displayBuffer += "You could use some improvement on water on usage. Make sure to turn off water when youre not using it! Try shorter showers might and reducing time on watering the lawn." + "\n"

    if electricity > 0:
        displayBuffer += "Youre doing great on electricity, keep it up!" + "\n"
    elif electricity == 0:
       displayBuffer += "Youre doing ok on electricity... Consider unplugging chargers when not in use." + "\n"
    elif electricity < 0:
        displayBuffer += "You could use some improvement on electricity usage. Make sure to turn off lights when you dont need them!" + "\n"

    if gas > 0:
        displayBuffer += "Youre doing great on gas, keep it up!" + "\n"
    elif gas == 0:
        displayBuffer += "Youre doing ok on gas... Consider using colder water in showers and to wash dishes." + "\n"
    elif gas < 0:
        displayBuffer += "You could use some improvement on gas usage. Make sure to turn off the stove when youre done cooking! Use colder water in showers and to wash dishes/clothes." + "\n"

    return wrap(displayBuffer)

def getWords(text):
    counter = 0
    array = []
    for word in text.split(" "):
        for other in word.split("\n"):
            array.append(other)
    return array

def wordsIntoLines(stuff):
    words = getWords(stuff)
    lines = []
    lineBuffer = ""
    for word in words:
        if word == "\n":
            lines.append(lineBuffer)
            lineBuffer = ""
        elif len(lineBuffer) + len(word) <= 20:
            lineBuffer += word + " "
        else:
            lines.append(lineBuffer)
            lineBuffer = word + " "
    lines.append(lineBuffer)
    return lines

def wrap(text):
    pages = []
    lines = wordsIntoLines(text)
    pageBuffer = []
    for i in range(len(lines)):
        pageBuffer.append(lines[i])
        if i % 8 == 0 and i !=0:
            pages.append("\n".join(pageBuffer))
            pageBuffer = []
    pages.append("\n".join(pageBuffer))
    return pages

def main():
    textAC = ""
    methods1 = [first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh]
    IDs = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth", "eleventh"]
    count = 0
    page = 0
    global SIZE
    papirus = Papirus()
    # Use smaller font for smaller dislays
    if papirus.height <= 96:
        SIZE = 18
    while True:
        if GPIO.input(SW3) == False:
            if page ==0:
                    count = count-1
            else:
                page = page-1
            count = (count%11)
            if count == 10:
                textAC = methods1[count]()
                text.AddText(textAC)
            else:
                text.Clear()
                text.AddText(str(methods1[count]()[page]))
        elif GPIO.input(SW2) == False:
            if page == len(methods1[count]())-1:
                page = 0
                count = count + 1
            else:
                page = page+1
            count = (count%11)
            if count == 10:
                textAC = methods1[count]()
                text.AddText(textAC)
            else:
                text.Clear()
                text.AddText(str(methods1[count]()[page]))
        else:
            if count == 10:
                if methods1[count] != textAC:
                    text.Clear()
                    text.AddText(str(methods1[count]()[page]))
                sleep(.5)
        sleep(0.1)


main()
