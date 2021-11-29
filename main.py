from PyDictionary import PyDictionary
from datetime import datetime
from threading import Thread
from pygame.locals import *
from gtts import gTTS
import speech_recognition as sr
import requests, json
import pvporcupine
import playsound
import requests
import pyaudio
import pyttsx3
import struct
import random
import pygame
import time
import os

pygame.init()

global output
global rawOut
global outCheckWarn
global bypassTTS
global bypassTTSValue
global API_KEY
global URL

keepRuning = True
currentFace = "None"
rawOut = ""
output = "System still starting!"
outCheckWarn = False
bypassTTS = False
bypassTTSValue = ""
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = "Kansas City"
API_KEY = "5dd8ff9a2f0e159dd83a44d2281a8e9d"
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 140)

#check for wake word

def getWake():
  try:
    porcupine = pvporcupine.create(keywords=["porcupine"])

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Hotword Detected")
            Thread(target = getSTT).start()
            time.sleep(2)

  finally:
      if porcupine is not None:
          porcupine.delete()

      if audio_stream is not None:
          audio_stream.close()

      if pa is not None:
              pa.terminate()

def get_next_audio_frame():
  pass

#create text from speach

def getSTT():
  global output
  global rawOut
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Talk")
    #pygame.mixer.init()
    #pygame.mixer.music.load('ding.mp3')
    #pygame.mixer.music.play()
    audio_text = r.listen(source)
    print("Time over, thanks")
    
    try:
        textdata = r.recognize_google(audio_text)
        rawOut = textdata
        getCom()
    except Exception as e:
         print(e)



#Face code

def getFaceInfo():
  global output
  print("Get face name if avalible or set to none")
  printDataOut()

#check if raw mic input text has command keywards

def getCom():
  global rawOut
  global output
  print(rawOut)
  if "time" in rawOut:
    getTime()
  elif "weather" in rawOut:
    getWeather()
  elif "dice" in rawOut:
    getDice()
  elif "coin" and "flip" in rawOut:
    getFlip()
  elif "bitcoin" and "price" in rawOut:
    getBitcoin()
  elif "definition" in rawOut:
    getDef()
  elif "stop" in rawOut:
    getStop()
  elif "help" in rawOut:
    getHelp()
  elif "joke" in rawOut:
    getJoke()
  else:
    print("Command not found!")

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
    output = "Error getting the weather, check your openweathermap API code. Try again later. code: 401"
  else:
    output = "Error while getting weather! (Do you have a internet connection?) code = " + str(response.status_code)
  printDataOut()

def getTime():
  global output
  global bypassTTS
  global bypassTTSValue
  bypassTTS = True
  now = datetime.now()
  fixedTime = now.strftime("%I:%M %p")
  output = ("The current time is, " + (str(fixedTime)))
  fixedTime = now.strftime("%I %M %p")
  bypassTTSValue = (str("The current time is " + (str(fixedTime))))
  printDataOut()
  
def getDice():
  global output
  output = str("The dice rolled on a " + str((random.randint(1, 6))))
  printDataOut()

def getFlip():
  global output
  flip = random.randint(1, 2)
  if flip == 1:
    output = "You got tails!"
    bypassTTSValue = "You got tails"
    bypassTTS = True
  else:
    output = "You got heads!"
    bypassTTSValue = "You got heads"
    bypassTTS = True
  printDataOut()

def getBitcoin():
  global output
  global bypassTTS
  global bypassTTSValue
  response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
  data = response.json()
  output = "The current price for bitcoin is, $" + str(int(data["bpi"]["USD"]["rate"]))
  bypassTTSValue = "The current price for bitcoin is " + str(int(data["bpi"]["USD"]["rate"])) + "dollars"
  bypassTTS = True
  printDataOut()
  
def getDef():
  global output
  global rawOut
  word = rawOut.split()
  word = (word[-1])
  dictionary=PyDictionary()
  definitionData = dictionary.meaning(word)
  output = "The definition of " + str(word) + " is: " + str(definitionData)
  printDataOut()
  
def getStop():
  global output
  output = " "
  printDataOut()

def getHelp():
  global output
  output = "The help command is not ready yet."
  printDataOut()
  
def getJoke():
  global output
  lines = open('jokes.txt').read().splitlines()
  output = random.choice(lines)
  printDataOut()
  
#testing purposes only!

def printDataOut():
  print(str(output))
  print("Sending to tts!")
  sayoutput()

#generate and output text to speach

def sayoutput():
  global output
  global outCheckWarn
  global bypassTTS
  global bypassTTSValue
  language = 'en'
  if bypassTTS == True:
    print("TTS Override! New Value = " + bypassTTSValue)
    myobj = gTTS(text=bypassTTSValue, lang=language, slow=False)
    myobj.save("temp.mp3")
    bypassTTS = False
  else:
    myobj = gTTS(text=output, lang=language, slow=False)
    myobj.save("temp.mp3")
  pygame.mixer.init()
  pygame.mixer.music.load('temp.mp3')
  pygame.mixer.music.play()
  clock = pygame.time.Clock()
  while pygame.mixer.music.get_busy() and not outCheckWarn:
      pygame.event.poll()
      clock.tick(10)
  pygame.mixer.quit()
  os.remove("temp.mp3")
  print("sayoutput finished")
  outCheckWarn = False

#ui

def uiRun():
  infoObject = pygame.display.Info()
  screen = pygame.display.set_mode((500, 500), RESIZABLE)
  # Run until the user asks to quit
  global output
  global outCheckWarn
  running = True
  font = pygame.font.Font('Amfallen.ttf', 32)
  th = 0
  a = 255
  ti = 0
  dim = 0
  carImg = pygame.image.load('aiui.gif')
  ih = carImg.get_height()
  iw = carImg.get_width()
  outCheck = ""
  fullMode = False
  while running:
    if not outCheck == output:
      if not outCheck == "":
        outCheckWarn = True
        a = 255
        dim = 0
        ti = 0
        th = 0
    outCheck = output
    if pygame.key.get_pressed()[K_f]:
      if fullMode == False:
        fullMode = True
        pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
        time.sleep(0.5)
      else:
        fullMode = False
        pygame.display.quit()
        screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
        pygame.display.init()
        time.sleep(0.5)
    w, h = pygame.display.get_surface().get_size()
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if event.type == pygame.MOUSEMOTION:
      pygame.mouse.set_visible(True)
    else:
      pygame.mouse.set_visible(False)
    # Fill the background
    screen.fill((5,1,23))
      
    if not output == "":
      text = font.render(str(output), True, (a,a,a))
      textRect = text.get_rect()
      th = th + 1
      if th >= 100:  #slide up
        th = 100
        if ti <= 50:
          if th >= 99:    #wait 5 sec
            ti = ti + 1
            time.sleep(0.1)
            if dim <= 255:
              if ti >= 49:     #dim away
                ti = 48
                a = a -5
                dim = dim + 5
                if a == 0:
                  a = 255
                  dim = 0
                  ti = 0
                  th = 0
                  output = ""
                  outCheck = "" 
    else:
      text = font.render(str(output), True, (a,a,a))
    textRect.center = (w // 2, h // 2 + ih/2 - th)
    screen.blit(carImg, ((w/2)-(iw/2),(h/2)-(ih/2)))
    screen.blit(text, textRect)
    # Flip the display
    pygame.display.flip()
  # Done! Time to quit.
  pygame.quit()

  
#run code
if __name__ == '__main__':
  Thread(target = uiRun).start()
  Thread(target = getWake).start()
  
