import time

keepRuning = True
currentFace = "None"
global output
output = "Error"

#Face code

def getFaceInfo():
  global output
  print("Get face name if avalible or set to none")
  printDataOut()

#Commands

def getWeather():
  global output
  print("Get weather for weather comand")
  printDataOut()

def getTime():
  global output
  print("getTime")
  printDataOut()
  
def printDataOut():
  print(str(output))
  
  #Now for the fun stuff
while keepRuning == True:
  print("Main loop goes here")
  getWeather()
  
