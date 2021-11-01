from datetime import datetime
import time
import requests, json
import pvporcupine
#import speech_recognition as sr
import pyttsx3


keepRuning = True
currentFace = "None"
global output
output = "Error"
#handle = pvporcupine.create(keywords=['picovoice'])
#r = sr.Recognizer()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = "Kansas City"
global API_KEY 
#API_KEY = "82a239137d8704a9310012b355421da8"
API_KEY = "7016307649b684cba0afd346d3901f6c"
global URL 
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 140)

#Face code

def getFaceInfo():
  global output
  print("Get face name if avalible or set to none")
  printDataOut()

#Commands

def getWeather():
  global output
  global API_KEY
  global URL
  response = requests.get(URL)
  if response.status_code == 200:
    data = response.json()
    main = data['main']
    temperature = main['temp']
    temperature = int(temperature) - 273.15
    temperature = 1.8 * temperature + 32
    weather = data['weather']
    weather = weather[0]
    weather = weather['description']
    output = ("The weather is " + str(weather) + " with a temperture of " + str(int(temperature)) + " degrees.")
  elif response.status_code == 401:
    output = "Error getting the weather, check your openweathermap API code. Try again later. code = 401"
  else:
    output = "Error while getting weather! (Do you have a internet connection?) code = " + str(response.status_code)
  printDataOut()

def getTime():
  global output
  now = datetime.now()
  current_time = now.strftime("%H %M")
  output = ("The current time is, " + (str(current_time)))
  printDataOut()
  

  #testing purposes only!
def printDataOut():
  print(str(output))
  print("Sending to tts!")
  sayoutput()
  
def get_next_audio_frame():
  pass
  
def sayoutput():
  global output
  engine.say(str(output))
  engine.runAndWait()
  
  #Now for the fun stuff
while keepRuning == True:
  inputType = input("Would you like the (W)eather or the (T) time?")
  if inputType == "W":
    getWeather()
  elif inputType == "T":
    getTime()
  else:
    output = "Error, wrong command"
    printDataOut()
  # keyword_index = handle.process(get_next_audio_frame())
  # if keyword_index >=0:
  #   handel.delete()
  #   with sr.Microphone() as source:
  #     print("Talk")
  #     audio_text = r.listen(source)
  #     print("Time over, thanks")
  #     #inset get command stt here
  #     print("got hotword!")
  #     pass
  
