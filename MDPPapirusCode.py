from papirus import Papirus
from papirus import PapirusText
from papirus import PapirusTextPos
from papirus import PapirusImage

screen = Papirus()
text = PapirusTextPos()

userMonthGallons= 2250
avgMonthGallons=1500
lastMonthGallons = 2500
userMonthElectricBtu= 3000000
avgMonthEletricBtu=2650000
lastMonthElectricBtu = 3100000
userMonthGasBtu=5000000
avgMonthGasBtu=4266666
lastMonthGasBtu = 5100000
waterScore = 0
electricScore = 0
gasScore = 0

def first(userMonthGallons):
    text.AddText(str(userMonthGallons), 10, 10, Id = "Start")

def second(userMonthGallons, lastMonthGallons):
    if userMonthGallons > lastMonthGallons:
        text.AddText("Over last month's usage by"
        + str(abs((lastMonthGallons-userMonthGallons)/lastMonthGallons)) + "pecent", 10, 10, Id= "Water2")
        waterScore -= 1
    elif userMonthGallons<lastMonthGallons:
        text.AddText("Under last month's usage by"
        + str(abs((lastMonthGallons-userMonthGallons)/lastMonthGallons)) + "percent", 10, 10, Id= "Water2")
        waterScore += 1

def thrid(userMonthGallons, avgMonthGallons):
    if userMonthGallons > avgMonthGallons:
        text.AddText("Over the average by"
        + str(abs((userMonthGallons-avgMonthGallons)/avgMonthGallons)) + "percent", 10, 10, Id= "Water3")
        waterScore -= 1
    elif userMonthGallons < avgMonthGallons:
        text.AddText("Under the average by"
        + str(abs((userMonthGallons-avgMonthGallons)/avgMonthGallons)) + "percent", 10, 10, Id = "Water3")
        waterScore += 1

def fourth(userMonthElectricBtu):
    text.AddText(str(userMonthElectricBtu), 10, 10, Id = "Start1")

def fifth(userMonthElectricBtu, lastMonthElectricBtu):
    if userMonthElectricBtu > lastMonthElectricBtu:
        text.AddText("Over last month's usage by"
        + str(abs((lastMonthElectricBtu-userMonthElectricBtu)/lastMonthElectricBtu)) + "pecent", 10, 10, Id= "Electric2")
        electricScore -= 1
    elif userMonthElectricBtu<lastMonthElectricBtu:
        text.AddText("Under last month's usage by"
        + str(abs((lastMonthElectricBtu-userMonthElectricBtu)/lastMonthElectricBtu)) + "percent", 10, 10, Id= "Electric2")
        electricScore += 1

def sixth(userMonthElectricBtu, avgMonthEletricBtu):
    if userMonthElectricBtu > avgMonthEletricBtu:
        text.AddText("Over the average by"
        + str(abs((userMonthElectricBtu-avgMonthEletricBtu)/avgMonthEletricBtu)) + "percent", 10, 10, Id= "Electric3")
        electricScore -= 1
    elif userMonthElectricBtu < avgMonthEletricBtu:
        text.AddText("Under the average by"
        + str(abs((userMonthElectricBtu-avgMonthEletricBtu)/avgMonthEletricBtu)) + "percent", 10, 10, Id = "Electric3")
        electricScore += 1 

def seventh(userMonthGasBtu):
    text.AddText(str(userMonthGasBtu), 10, 10, Id = "Start2")

def eighth(userMonthGasBtu, lastMonthGasBtu):
    if userMonthGasBtu > lastMonthGasBtu:
        text.AddText("Over last month's usage by"
        + str(abs((lastMonthGasBtu-userMonthGasBtu)/lastMonthGasBtu)) + "pecent", 10, 10, Id= "Gas2")
        gasScore -= 1
    elif userMonthGasBtu<lastMonthGasBtu:
        text.AddText("Under last month's usage by"
        + str(abs((lastMonthGasBtu-userMonthGasBtu)/lastMonthGasBtu)) + "percent", 10, 10, Id= "Gas2")
        gasScore += 1

def ninth(userMonthGasBtu, avgMonthGasBtu):
    if userMonthGasBtu > avgMonthGasBtu:
        text.AddText("Over the average by"
        + str(abs((userMonthGasBtu-avgMonthGasBtu)/avgMonthGasBtu)) + "percent", 10, 10, Id= "Gas3")
        gasScore -= 1
    elif userMonthGasBtu < avgMonthGasBtu:
        text.AddText("Under the average by"
        + str(abs((userMonthGasBtu-avgMonthGasBtu)/avgMonthGasBtu)) + "percent", 10, 10, Id = "Gas3")
        gasScore += 1

def genSuggestions(water, electricity, gas):
    displayBuffer = ""
    if water > 0:
        displayBuffer += "Youre doing great on water--keep it up!" + "\n"
    elif water == 0:
        displayBuffer += "Youre doing ok on water... Consider taking shorter showers, turning off the faucet when brushing, etc." + "\n"
    elif water < 0:
        displayBuffer += "You could use some improvement on water on usage. Make sure to turn off water when youre not using it! Try shorter showers might and reducing time on watering the lawn." + "\n"

    if electricity > 0:
        displayBuffer += "Youre doing great on electricity--keep it up!" + "\n"
    elif electricity == 0:
       displayBuffer += "Youre doing ok on electricity... Consider unplugging chargers when not in use." + "\n"
    elif electricity < 0:
        displayBuffer += "You could use some improvement on electricity usage. Make sure to turn off lights when you dont need them!" + "\n"

    if gas > 0:
        displayBuffer += "Youre doing great on gas--keep it up!" + "\n"
    elif gas == 0:
        displayBuffer += "Youre doing ok on gas... Consider using colder water in showers and to wash dishes." + "\n"
    elif gas < 0:
        displayBuffer += "You could use some improvement on gas usage. Make sure to turn off the stove when youre done cooking! Use colder water in showers and to wash dishes/clothes." + "\n"

    text.AddText(displayBuffer)